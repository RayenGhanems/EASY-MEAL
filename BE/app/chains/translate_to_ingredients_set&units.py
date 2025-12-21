from typing import Dict, Any, List, Tuple
import re
import json
import pandas as pd

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# Load ingredient data
# =========================================================

INGREDIENTS_CSV = "../DB/Recepies/ingredients.csv"
df_ing = pd.read_csv(INGREDIENTS_CSV)

ingredient_list: List[str] = df_ing["ingredient_name"].tolist()
ingredient_map = dict(zip(df_ing["ingredient_name"], df_ing["ingredient_id"]))
unit_map = dict(zip(df_ing["ingredient_id"], df_ing["measuring_unit"]))


# =========================================================
# Unit normalization (CRITICAL)
# =========================================================

UNIT_NORMALIZATION = {
    # volume
    "cups": "cup",
    "cup": "cup",
    "tablespoons": "tablespoon",
    "tablespoon": "tablespoon",
    "tbsp": "tablespoon",
    "teaspoons": "teaspoon",
    "teaspoon": "teaspoon",
    "tsp": "teaspoon",
    "ml": "ml",
    "l": "l",

    # mass
    "grams": "gram",
    "gram": "gram",
    "g": "gram",

    # discrete
    "cloves": "clove",
    "clove": "clove"
}

def normalize_unit(unit: str) -> str:
    return UNIT_NORMALIZATION.get(unit.lower(), unit.lower())


# =========================================================
# Quantity parsing
# =========================================================

def parse_quantity(text: str) -> Tuple[float | None, str | None]:
    """
    Extract numeric value and unit from strings like:
    '2 cups', '1 tbsp', '3 cloves'
    """
    pattern = re.compile(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)")
    m = pattern.search(text.lower())
    if not m:
        return None, None
    return float(m.group(1)), normalize_unit(m.group(2))


# =========================================================
# Deterministic unit conversion (FAST PATH)
# =========================================================

EASY_CONVERSION = {
    ("cup", "tablespoon"): 16,
    ("tablespoon", "teaspoon"): 3,

    ("teaspoon", "gram"): 5,
    ("tablespoon", "gram"): 15,
    ("cup", "gram"): 240,
    ("ml", "gram"): 1,
}

def convert_amount(val: float, frm: str, to: str) -> float | None:
    factor = EASY_CONVERSION.get((frm, to))
    if factor is None:
        return None
    return val * factor


# =========================================================
# LLM setup
# =========================================================

llm = ChatOpenAI(model="gpt-4", temperature=0)


def resolve_ingredient_llm(raw_name: str) -> dict:
    """
    Normalize noisy ingredient name
    """

    prompt = f"""
You are an ingredient normalizer.

Raw ingredient:
"{raw_name}"

Allowed ingredient list:
{json.dumps(ingredient_list)}

Return EXACTLY this JSON:

{{
  "status": "RESOLVED" | "AMBIGUOUS" | "UNKNOWN",
  "ingredient_name": string | null,
  "candidates": string[]
}}

Rules:
- ingredient_name MUST be from the allowed list
- Choose closest match even if imperfect
- Prefer general ingredients
- No explanations
"""

    response = llm.invoke(prompt).content
    return json.loads(response)


def estimate_conversion_llm(
    ingredient_name: str,
    amount: float,
    from_unit: str,
    to_unit: str
) -> float:
    """
    LLM-based ESTIMATION.
    ALWAYS returns a number.
    """

    prompt = f"""
        You are a cooking assistant.

        Estimate the conversion:

        Ingredient: {ingredient_name}
        Convert: {amount} {from_unit} → {to_unit}

        Return ONLY a number.
        No text. No explanation.
        Round to 2 decimals.
        """

    response = llm.invoke(prompt).content.strip()

    try:
        return float(response)
    except ValueError:
        # Absolute safety fallback
        return amount


# =========================================================
# Translate json output to more sql frendly one
# =========================================================

def to_sql_rows(agent_output: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transform run_agent output into SQL-ready rows.
    """

    rows = []

    for raw_name, data in agent_output.items():
        if data.get("status") != "RESOLVED":
            continue  # skip unresolved items

        rows.append({
            "ingredient_id": data["ingredient_id"],
            "amount": data["canonical"]["amount"],
            "unit": data["canonical"]["unit"]
        })

    return rows

# =========================================================
# Main pipeline
# =========================================================

def run_agent(user_input: Dict[str, str]) -> Dict[str, Any]:
    results = {}

    for raw_name, raw_qty in user_input.items():

        # -------------------------------------------------
        # 1. Resolve ingredient
        # -------------------------------------------------

        resolved = resolve_ingredient_llm(raw_name)

        if resolved["status"] != "RESOLVED":
            results[raw_name] = resolved
            continue

        ingredient_name = resolved["ingredient_name"]
        ingredient_id = ingredient_map[ingredient_name]
        canonical_unit = normalize_unit(unit_map[ingredient_id])

        # -------------------------------------------------
        # 2. Parse quantity
        # -------------------------------------------------

        qty_val, qty_unit = parse_quantity(raw_qty)
        if qty_val is None:
            results[raw_name] = {"status": "PARSE_ERROR"}
            continue

        # -------------------------------------------------
        # 3. Convert (deterministic → LLM estimate)
        # -------------------------------------------------

        if qty_unit == canonical_unit:
            final_amount = qty_val
            method = "identity"

        else:
            converted = convert_amount(qty_val, qty_unit, canonical_unit)
            if converted is not None:
                final_amount = converted
                method = "internal_map"
            else:
                final_amount = estimate_conversion_llm(
                    ingredient_name=ingredient_name,
                    amount=qty_val,
                    from_unit=qty_unit,
                    to_unit=canonical_unit
                )
                method = "llm_estimate"

        # -------------------------------------------------
        # 4. Final output (ALWAYS numeric)
        # -------------------------------------------------

        results[raw_name] = {
            "status": "RESOLVED",
            "ingredient_id": ingredient_id,
            "ingredient_name": ingredient_name,
            "input": {
                "amount": qty_val,
                "unit": qty_unit
            },
            "canonical": {
                "amount": round(final_amount, 2),
                "unit": canonical_unit
            },
            "conversion": {
                "method": method
            }
        }

    return to_sql_rows(results)


# =========================================================
# CLI test
# =========================================================

# if __name__ == "__main__":
#     sample = {
#         "brown suggar": "2 cups",
#         "olive oyl": "1 tbsp",
#         "garlec": "3 cloves",
#         "choclatr cake":"1 peace"
#     }

#     out = run_agent(sample)
#     print(out)

from typing import Dict, Any, List, Tuple
import re
import json

from sqlmodel import Session
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

from app.sql.sql_fxns import get_ingredient_table

load_dotenv()

# =========================================================
# --------------------- Data Models -----------------------
# =========================================================

class IngredientInput(BaseModel):
    ingredient: str
    quantity: str


# =========================================================
# ------------------- DB Preparation ----------------------
# =========================================================

def load_ingredients_from_db(session: Session):
    """
    Load ingredients from DB and prepare:
    - ingredient_list (sorted by length DESC for LLM resolution)
    - ingredient_map (case-insensitive lookup)
    - unit_map (DB presentation units)
    """
    ingredients = get_ingredient_table(session)

    ingredient_list = sorted(
        [ing.ingredient_name for ing in ingredients],
        key=len,
        reverse=True
    )

    ingredient_map = {
        ing.ingredient_name.lower(): ing.ingredient_id
        for ing in ingredients
    }

    unit_map = {
        ing.ingredient_id: ing.measuring_unit.lower()
        for ing in ingredients
    }

    return ingredient_list, ingredient_map, unit_map


# =========================================================
# ------------------- Unit Handling -----------------------
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
    "kilograms": "kg",
    "kilogram": "kg",
    "kg": "kg",
    "grams": "gram",
    "gram": "gram",
    "g": "gram",

    # discrete
    "cloves": "clove",
    "clove": "clove",
    "pcs": "pcs",
    "piece": "pcs",
    "pieces": "pcs",
}

def normalize_unit(unit: str | None) -> str | None:
    if not unit:
        return None
    return UNIT_NORMALIZATION.get(unit.lower(), unit.lower())


# =========================================================
# ---------------- Quantity Parsing -----------------------
# =========================================================

def parse_quantity(text: str) -> Tuple[float | None, str | None]:
    """
    Parses:
    - '5 kg'
    - '05 Kg'
    - '2cups'
    - '1 tbsp'
    """
    pattern = re.compile(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)")
    match = pattern.search(text.lower())

    if not match:
        return None, None

    value = float(match.group(1))
    unit = normalize_unit(match.group(2))
    return value, unit


# =========================================================
# ---------------- Deterministic Conversion ---------------
# =========================================================

EASY_CONVERSION = {
    ("kg", "gram"): 1000,
    ("gram", "kg"): 0.001,

    ("cup", "tablespoon"): 16,
    ("tablespoon", "teaspoon"): 3,

    ("teaspoon", "gram"): 5,
    ("tablespoon", "gram"): 15,
    ("cup", "gram"): 240,
    ("ml", "gram"): 1,
}

def convert_amount(value: float, from_unit: str, to_unit: str) -> float | None:
    factor = EASY_CONVERSION.get((from_unit, to_unit))
    if factor is None:
        return None
    return value * factor


# =========================================================
# -------------------- LLM Setup --------------------------
# =========================================================

llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)


# =========================================================
# ------------ INGREDIENT vs DISH Filter -----------------
# =========================================================

def classify_food_llm(text: str) -> str:
    prompt = f"""
Classify the following as either:

INGREDIENT → raw food item
DISH       → prepared meal or recipe

Text:
"{text}"

Return ONLY one word.
"""
    try:
        out = llm.invoke(prompt).content.strip().upper()
        return out if out in {"INGREDIENT", "DISH"} else "INGREDIENT"
    except Exception:
        return "INGREDIENT"


# =========================================================
# ------------ Ingredient Name Resolution ----------------
# =========================================================

def resolve_ingredient_llm(raw_name: str, ingredient_list: List[str]) -> dict:
    """
    Resolve noisy ingredient names to exact DB ingredient names.

    Critical rules:
    - Output MUST be from allowed list
    - If one name contains another, ALWAYS choose the LONGER one
      (e.g. honeydew → Honeydew, NOT Honey)
    """
    prompt = f"""
You are an ingredient normalizer.

Raw ingredient:
"{raw_name}"

Allowed ingredient list (sorted by specificity):
{json.dumps(ingredient_list)}

Return EXACTLY this JSON:
{{
  "status": "RESOLVED" | "AMBIGUOUS" | "UNKNOWN",
  "ingredient_name": string | null,
  "candidates": string[]
}}

Rules:
- ingredient_name MUST be from the allowed list
- If one ingredient name is a substring of another,
  ALWAYS choose the LONGER name
- Prefer exact matches over semantic ones
- Do NOT collapse ingredients into more generic ones
- No explanations
"""
    try:
        return json.loads(llm.invoke(prompt).content)
    except Exception:
        return {"status": "UNKNOWN", "ingredient_name": None, "candidates": []}


# =========================================================
# --------- LLM Conversion (GUARDED GUESSING) -------------
# =========================================================

def llm_convert_with_guardrails(
    ingredient_name: str,
    amount: float,
    from_unit: str,
    to_unit: str
) -> float:
    """
    LLM-based conversion with HARD safety bounds.
    Used only when deterministic conversion fails.
    """
    prompt = f"""
You are estimating ingredient quantities for a cooking inventory app.

IMPORTANT:
- Conversion may be physically ambiguous
- Make a reasonable culinary assumption
- Approximation is acceptable

Ingredient: {ingredient_name}
Convert: {amount} {from_unit} → {to_unit}

Rules:
- Return ONLY a number
- Round to 2 decimals
"""
    try:
        estimated = float(llm.invoke(prompt).content.strip())
    except Exception:
        return amount

    # -------- Guardrails --------
    if estimated <= 0:
        return amount

    if estimated > amount * 10_000:
        return amount * 1000

    if estimated < amount * 0.0001:
        return amount * 0.01

    print(
        f"[LLM-GUESS] {ingredient_name}: "
        f"{amount} {from_unit} → {estimated} {to_unit}"
    )

    return estimated


# =========================================================
# ------------------ MAIN PIPELINE ------------------------
# =========================================================

def verifying_ingredients_chain(
    session: Session,
    user_input: Dict[str, str]
) -> List[Dict[str, Any]]:

    rows = []
    ingredient_list, ingredient_map, unit_map = load_ingredients_from_db(session)

    for raw_name, raw_qty in user_input.items():

        # 0. Dish filter
        if classify_food_llm(raw_name) == "DISH":
            continue

        # 1. Resolve ingredient name
        resolved = resolve_ingredient_llm(raw_name, ingredient_list)
        if resolved["status"] != "RESOLVED":
            continue

        ingredient_name = resolved["ingredient_name"].lower().strip()
        ingredient_id = ingredient_map.get(ingredient_name)

        if ingredient_id is None:
            print(f"[WARN] Ingredient not in DB: {ingredient_name}")
            continue

        db_unit = normalize_unit(unit_map[ingredient_id])

        # 2. Parse quantity
        qty_value, qty_unit = parse_quantity(raw_qty)
        if qty_value is None or qty_unit is None:
            continue

        # 3. Convert quantity
        if qty_unit == db_unit:
            final_amount = qty_value
        else:
            converted = convert_amount(qty_value, qty_unit, db_unit)
            if converted is not None:
                final_amount = converted
            else:
                final_amount = llm_convert_with_guardrails(
                    ingredient_name,
                    qty_value,
                    qty_unit,
                    db_unit
                )

        # 4. Store result (never silently drop)
        rows.append({
            "ingredient_id": ingredient_id,
            "amount": round(final_amount, 2),
            "unit": db_unit
        })

    return rows


# =========================================================
# ---------------- SQLModel Cleaner -----------------------
# =========================================================

def clean_for_sqlmodel(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prepare output for SQLModel insertion.
    """
    return [
        {
            "ingredient_id": row["ingredient_id"],
            "amount": row["amount"]
        }
        for row in rows
    ]

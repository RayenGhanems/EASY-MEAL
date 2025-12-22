from typing import Dict, Any, List, Tuple
import re
import json
import pandas as pd
from sqlmodel import Session
 
from langchain_openai import ChatOpenAI
 
from dotenv import load_dotenv;load_dotenv()
<<<<<<< Updated upstream
 
from app.sql.sql_fxns import get_ingredient_table 
 
from pydantic import BaseModel
 
class IngredientInput(BaseModel):
    ingredient: str
    quantity: str
 
# =========================================================
# Load ingredient data
# =========================================================
 
def load_ingredients_from_db(session : Session):
=======

from app.sql.sql_fxns import get_ingredient_table
from app.DB import session


from pydantic import BaseModel

class IngredientInput(BaseModel):
    ingredient: str
    quantity: str
    unit: str

# =========================================================
# Load ingredient data
# =========================================================

def load_ingredients_from_db(session: session):
>>>>>>> Stashed changes
    ingredients = get_ingredient_table(session)
 
     # 1. List of ingredient names (for LLM resolution)
    ingredient_list = [
        ing.ingredient_name
        for ing in ingredients
    ]
 
    # 2. Map ingredient name -> ingredient_id
    ingredient_map = {
        ing.ingredient_name: ing.ingredient_id
        for ing in ingredients
    }
 
    # 3. Map ingredient_id -> measuring_unit
    unit_map = {
        ing.ingredient_id: ing.measuring_unit
        for ing in ingredients
    }
 
    return ingredient_list, ingredient_map, unit_map
 
# =========================================================
# Unit normalization
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
# Deterministic unit conversion
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
 
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)
 
 
# =========================================================
# LLM classification: INGREDIENT vs DISH
# =========================================================
 
def classify_food_llm(text: str) -> str:
    """
    Classify input as INGREDIENT or DISH.
    """
 
    prompt = f"""
Classify the following as either:
 
INGREDIENT → raw food item (sugar, garlic, milk, chocolate)
DISH       → prepared food or recipe (cake, pizza, lasagna, cookies)
 
Text:
"{text}"
 
Return ONLY one word:
INGREDIENT or DISH
"""
 
    response = llm.invoke(prompt).content.strip().upper()
 
    if response not in {"INGREDIENT", "DISH"}:
        return "INGREDIENT"  # safe fallback
 
    return response
 
 
# =========================================================
# LLM ingredient resolution
# =========================================================
 
def resolve_ingredient_llm(raw_name: str, ingredient_list: List) -> dict:
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
 
 
# =========================================================
# LLM conversion estimation
# =========================================================
 
def estimate_conversion_llm(
    ingredient_name: str,
    amount: float,
    from_unit: str,
    to_unit: str
) -> float:
    """
    LLM-based estimation.
    ALWAYS returns a number.
    """
 
    prompt = f"""
            You are a cooking assistant.
<<<<<<< Updated upstream
 
            Estimate the conversion:
 
            Ingredient: {ingredient_name}
            Convert: {amount} {from_unit} → {to_unit}
 
=======

            Estimate the conversion:

            Ingredient: {ingredient_name}
            Convert: {amount} {from_unit} → {to_unit}

>>>>>>> Stashed changes
            Return ONLY a number.
            No text. No explanation.
            Round to 2 decimals.
            """
<<<<<<< Updated upstream
 
=======

>>>>>>> Stashed changes
    response = llm.invoke(prompt).content.strip()
 
    try:
        return float(response)
    except ValueError:
        return amount  # ultimate fallback
 
 
# =========================================================
# Main pipeline (returns SQL-ready rows)
# =========================================================
 
def verifying_ingredients_chain(session: Session,user_input: Dict[str, str]) -> List[Dict[str, Any]]:
    rows = []
    ingredient_list, ingredient_map, unit_map = load_ingredients_from_db(session)
 
    for raw_name, raw_qty in user_input.items():
 
        # -------------------------------------------------
        # 0. Ingredient vs Dish classification
        # -------------------------------------------------
 
        if classify_food_llm(raw_name) == "DISH":
            continue  # skip dishes entirely
 
        # -------------------------------------------------
        # 1. Resolve ingredient
        # -------------------------------------------------
 
        resolved = resolve_ingredient_llm(raw_name, ingredient_list)
        if resolved["status"] != "RESOLVED":
            continue
 
        ingredient_name = resolved["ingredient_name"]
        ingredient_id = ingredient_map[ingredient_name]
        canonical_unit = normalize_unit(unit_map[ingredient_id])
 
        # -------------------------------------------------
        # 2. Parse quantity
        # -------------------------------------------------
 
        qty_val, qty_unit = parse_quantity(raw_qty)
        if qty_val is None:
            continue
 
        # -------------------------------------------------
        # 3. Convert amount
        # -------------------------------------------------
 
        if qty_unit == canonical_unit:
            final_amount = qty_val
 
        else:
            converted = convert_amount(qty_val, qty_unit, canonical_unit)
            if converted is not None:
                final_amount = converted
            else:
                final_amount = estimate_conversion_llm(
                    ingredient_name=ingredient_name,
                    amount=qty_val,
                    from_unit=qty_unit,
                    to_unit=canonical_unit
                )
 
        # -------------------------------------------------
        # 4. SQL-ready row
        # -------------------------------------------------
 
        rows.append({
            "ingredient_id": ingredient_id,
            "amount": round(final_amount, 2),
            "unit": canonical_unit
        })
    
    return rows
<<<<<<< Updated upstream
 
 
=======


>>>>>>> Stashed changes
def clean_for_sqlmodel(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prepare chain output for IngredientStored SQLModel.
    """
    cleaned = []
<<<<<<< Updated upstream
 
=======

>>>>>>> Stashed changes
    for row in rows:
        cleaned.append({
            "ingredient_id": row["ingredient_id"],
            "amount": row["amount"]
        })
<<<<<<< Updated upstream
 
    return cleaned
 
 
 
=======

    return cleaned



>>>>>>> Stashed changes
# =========================================================
# CLI test
# =========================================================
 
# if __name__ == "__main__":
#     sample = {
#         "brown suggar": "2 cups",
#         "olive oyl": "1 tbsp",
#         "garlec": "3 cloves",
#         "choclatr cake": "1 peace",
#         "pizza": "2 slices"
#     }
 
#     out = verifying_ingredients_chain(sample)
#     print(out)
from sqlmodel import Session
from typing import List

from app.sql.sql_fxns import get_all_recipes, get_user_ingredients, get_recipe_ingredients


def get_cookable_recipes(session: Session, user_id: int) -> List[int]:
    """
    Return recipes the user can cook with current stored ingredients.
    """

    # Load user stock
    user_ingredients = get_user_ingredients(session, user_id)
    user_stock = {
        ing.ingredient_id: ing.amount
        for ing in user_ingredients
    }

    cookable = []

    # Iterate over all recipes
    for recipe in get_all_recipes(session):
        requirements = get_recipe_ingredients(session, recipe.recipe_id)

        can_cook = True

        for req in requirements:
            available = user_stock.get(req.ingredient_id, 0)

            if available <= req.amount:
                can_cook = False
                break

        if can_cook:
            cookable.append(recipe.recipe_id)

    return cookable

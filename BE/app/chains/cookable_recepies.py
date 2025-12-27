from sqlmodel import Session
from typing import List

from app.sql.sql_fxns import get_all_recipes, get_user_ingredients, get_recipe_ingredients, get_cookable_recipes_sql, rmv_frm_cookable_sql


def get_cookable_recipes(session: Session, user_id: int) -> List[int]:
    """
    Return recipes the user can cook with current stored ingredients.
    """

    user_ingredients = get_user_ingredients(session, user_id)
    user_stock = {
        ing.ingredient_id: ing.amount
        for ing in user_ingredients
    }

    cookable = []

    for recipe in get_all_recipes(session):
        requirements = get_recipe_ingredients(session, recipe.recipe_id)

        can_cook = True

        for req in requirements:
            available = user_stock.get(req.ingredient_id, 0)

            if available < req.amount:
                can_cook = False
                break

        if can_cook:
            cookable.append(recipe.recipe_id)

    return cookable


def check_cookable_recipes(session: Session, user_id: int):
    """
    Remove recipes from Cookable_recipes if the user can no longer cook them.
    """
    user_ingredients = get_user_ingredients(session, user_id)
    user_stock = {
        ing.ingredient_id: ing.amount
        for ing in user_ingredients
    }
    for recipe in get_cookable_recipes_sql(session, user_id):
        requirements = get_recipe_ingredients(session, recipe.recipe_id)

        for req in requirements:
            available = user_stock.get(req.ingredient_id, 0)

            if available < req.amount:
                rmv_frm_cookable_sql( session=session, user_id=user_id, recipe_id=recipe.recipe_id)
                break  

    session.commit() 

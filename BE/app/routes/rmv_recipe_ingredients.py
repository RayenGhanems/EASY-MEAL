from fastapi import APIRouter, Depends
from app.DB import get_session
from app.chains.cookable_recepies import check_cookable_recipes
from sqlmodel import Session
from app.core.security import get_current_user
from app.sql.sql_fxns import get_recipe_ingredients, reduce_user_ingredient

 
router = APIRouter(tags=["eat_recipe"])
 
@router.get("/get_recipes")
async def eat_recipe(session: Session = Depends(get_session), user_id: int = Depends(get_current_user), recipe_id: int = -1):
    if recipe_id == -1 or recipe_id <= 70:
        return 
    
    for req in get_recipe_ingredients(session, recipe_id):
        reduce_user_ingredient(session, user_id, req.ingredient_id, req.amount)

    check_cookable_recipes(session, user_id)
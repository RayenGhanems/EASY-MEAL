from fastapi import APIRouter, Depends
from app.DB import get_session
from app.chains.cookable_recepies import check_cookable_recipes
from sqlmodel import Session
from app.core.security import get_current_user
from app.sql.sql_fxns import reduce_user_ingredient
from chains.translate_to_ingredients_set_units import verifying_ingredients_chain, clean_for_sqlmodel

 
router = APIRouter(tags=["eat_recipe"])
 
@router.get("/get_recipes")
async def eat_ingredients(session: Session = Depends(get_session), user_id: int = Depends(get_current_user), ingredient: list[str] = [], amount:list[int] = []):
    if ingredient == [] or amount == []:
        return 
    d ={}
    for i,ing in enumerate(ingredient):
        d[ing] = amount[i]

    rows = verifying_ingredients_chain(session, d)
    cleaned = clean_for_sqlmodel(rows)
 
    for row in cleaned:
        reduce_user_ingredient( session=session, user_id=user_id, ingredient_id=row["ingredient_id"], amount=row["amount"])

    check_cookable_recipes(session, user_id)
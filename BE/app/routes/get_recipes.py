from fastapi import APIRouter, Depends
from app.sql.sql_fxns import get_cookable_recipes
from app.DB import get_session
from app.chains.retreive_recipe import get_full_recipe_by_id
from sqlmodel import Session
from app.core.security import get_current_user
 
router = APIRouter(tags=["get_recipes"])
 
@router.get("/get_recipes")
async def get_recipes(session: Session = Depends(get_session), user_id: int = Depends(get_current_user), dish_preference: str = "ALL"):

    recipe_ids = get_cookable_recipes(session, user_id)

    out = []
    for recipe_id in recipe_ids:
        out.append(get_full_recipe_by_id(session, recipe_id))

    if dish_preference != "ALL":
        out = [ r   for r in out    if r["dish_type"] == dish_preference]

    return {
        "count": len(out),
        "recipes": out
    }
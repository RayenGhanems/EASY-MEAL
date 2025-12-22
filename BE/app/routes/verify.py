from fastapi import APIRouter, Depends
from typing import Dict
from app.chains.translate_to_ingredients_set_units import verifying_ingredients_chain, clean_for_sqlmodel, IngredientInput
from app.sql.sql_fxns import add_user_ingredient
from app.DB import get_session
from sqlmodel import Session
from app.core.security import get_current_user
 
router = APIRouter(tags=["verify"])
 
@router.post("/verify")
async def verify(items: list[IngredientInput], user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    
    result = {}
    for item in items:
        result[item.ingredient] = item.quantity
 
    # 1. Run chain
    rows = verifying_ingredients_chain(session, items)
 
    # 2. Clean output
    cleaned = clean_for_sqlmodel(rows)
 
    for row in cleaned:
        add_user_ingredient(
            session=get_session,
            user_id=user_id,
            ingredient_id=row["ingredient_id"],
            amount=row["amount"]
        )
    return {
        "status": "success",
        "added": cleaned
    }
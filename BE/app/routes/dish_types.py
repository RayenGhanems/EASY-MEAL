from fastapi import APIRouter, Depends

from app.DB import get_session
from sqlmodel import Session

from app.sql.sql_fxns import get_dish_types

router = APIRouter(tags=["dish_type"])

@router.post("/dish_type")
async def get_dish_types(session: Session = Depends(get_session)):
    return get_dish_types(session)

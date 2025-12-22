from fastapi import APIRouter, UploadFile, File, Depends
import base64
from BE.app.chains.translate_to_ingredients_set_units import verifying_ingredients_chain
from app.core.security import get_current_user

router = APIRouter(tags=["verify"])

@router.post("/verify")
async def verify(list :list):
    user_id: int = Depends(get_current_user)
    return[]

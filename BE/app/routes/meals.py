from fastapi import APIRouter, UploadFile, File, Depends
import base64
from BE.app.chains.img_to_ingredients import img_to_ingredients_chain
from app.core.security import get_current_user

router = APIRouter(tags=["meals"])

@router.post("/easy_meals")
async def analyze_fridge(images: list[UploadFile] = File(...),
    user_id: int = Depends(get_current_user)):
    imgs = []
    for image in images:
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        imgs.append({"image_base64": image_base64})

    results = img_to_ingredients_chain.batch(imgs)
    print("Authenticated user:", user_id)
    return [r.model_dump() for r in results]

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from app.DB import get_session
import base64 

from app.chain import chain
from app.sql.sql_fxns import *

app = FastAPI(title="EASY MEAL API")


# ⭐️ Configure CORS
origins = ["http://localhost:5173",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow these origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all methods (GET, POST, etc.)
    allow_headers=["*"],         # allow all headers
)


@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")

# ---------- Image upload endpoint ----------

@app.post("/easy_meals")
async def analyze_fridge(images: list[UploadFile] = File(...)):
    imgs = []

    for image in images:
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        imgs.append({"image_base64": image_base64})

    results = chain.batch(imgs)    ### batch is like map but map only changes it you need to re invoke it after while bathch is invoke each elemnt of the list

    return [r.model_dump() for r in results]

@app.post("/auth/signup")
async def signup_user(user: dict):
    email = user.get("email")
    password = user.get("password")
    username = user.get("username")
    phone_number = user.get("phone_number")

    # Check if user already exists
    existing_user = get_user_by_email(email,next(get_session()))
    if existing_user:
        return {"success": False, "message": "User already exists"}

    # Create new user
    create_user(email, password, username, phone_number, next(get_session()))

    return {"success": True, "message": "User created successfully"}

@app.post("/auth/signin")
async def signin_user(user: dict):
    email = user.get("email")
    password = user.get("password")

    # Retrieve user by email
    existing_user = get_user_by_email(email, next(get_session()))
    if not existing_user or existing_user.password != password:
        return {"success": False, "message": "Invalid email or password"}

    return {"success": True, "message": "User signed in successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

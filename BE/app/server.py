from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

import base64 

from app.chain import chain

app = FastAPI(title="EASY MEAL API")


# ⭐️ Configure CORS
origins = [
    "http://localhost:5173",  # your React dev origin
    # add other frontend URLs here if needed
]

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
async def analyze_fridge(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    result = chain.invoke({
        "image_base64": image_base64
    })

    return result.model_dump()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

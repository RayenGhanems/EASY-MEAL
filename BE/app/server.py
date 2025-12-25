from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.meals import router as meals_router
from app.routes.verify import router as verify_router
from app.routes.dish_types import router as dish_type_router
from app.routes.get_recipes import router as get_recipe_router

app = FastAPI(title="EASY MEAL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(meals_router)
app.include_router(verify_router)
app.include_router(dish_type_router)
app.include_router(get_recipe_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

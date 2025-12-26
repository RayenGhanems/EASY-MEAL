from sqlmodel import Session, select, delete
from  typing import List, Tuple

from app.sql.sql_models import *

def get_ingredient_table(session: Session):
    statement = select(Ingredient)
    return session.exec(statement).all()

def reduce_user_ingredient(session: Session, user_id: int, ingredient_id: int, amount: float):
    statement = select(StoredIngredients).where(StoredIngredients.user_id == user_id, StoredIngredients.ingredient_id == ingredient_id)
    existing = session.exec(statement).first()
    if not existing:
        return
    existing.amount -= amount
    if existing.amount <= 0:
        session.delete(existing)

def add_user_ingredient(session: Session, user_id: int, ingredient_id: int, amount: float):
    statement = select(StoredIngredients).where( StoredIngredients.user_id == user_id, StoredIngredients.ingredient_id == ingredient_id)
    existing = session.exec(statement).first()
    if existing:
        existing.amount += amount   # So if a user already has ingredient a with an amount of 2 and he brought another 2 then the total will be 4
    else:
        new_row = StoredIngredients(user_id=user_id,ingredient_id=ingredient_id,amount=amount)
        session.add(new_row)
    session.commit()

def set_user_ingredient(session: Session, user_id: int, ingredient_id: int, amount: float):
    statement = select(StoredIngredients).where( StoredIngredients.user_id == user_id, StoredIngredients.ingredient_id == ingredient_id)
    existing = session.exec(statement).first()
    if existing:
        existing.amount = amount   
    else:
        new_row = StoredIngredients(user_id=user_id,ingredient_id=ingredient_id,amount=amount)
        session.add(new_row)
    session.commit()

def get_user_by_email(session: Session, user_email: str):
    statement = select(User).where(User.username == user_email)
    return session.exec(statement).first()

def create_user(session: Session, user_email: str, hashed_password: str):
    new_user = User(username=user_email, password=hashed_password)
    session.add(new_user)
    session.commit()


def get_user_ingredients(session: Session, user_id: int):
    stmt = select(StoredIngredients).where(StoredIngredients.user_id == user_id)
    return session.exec(stmt).all()

def get_recipe_ingredients(session: Session, recipe_id: int):
    stmt = select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)
    return session.exec(stmt).all()

def get_all_recipes(session: Session):
    return session.exec(select(Recipe).where(Recipe.recipe_id <= 70)).all()

def get_dish_types(session: Session):
    return session.exec(select(DishType)).all()

def delete_from_cookable_recipes(session: Session, user_id:int):
    session.exec(delete(Cookable_recipes).where(Cookable_recipes.user_id == user_id))
    session.commit()

def store_cookable_recipes(session : Session, user_id:int, recipe_ids:List[int]):
    delete_from_cookable_recipes(session, user_id)
    rows = [Cookable_recipes(user_id=user_id, recipe_id=recipe_id) for recipe_id in recipe_ids]
    session.add_all(rows)
    session.commit()

def get_cookable_recipes_sql(session: Session, user_id: int):
    return session.exec(select(Cookable_recipes.recipe_id).where(Cookable_recipes.user_id == user_id)).all()

def rmv_frm_cookable_sql(session: Session, user_id: int, recipe_id: int):
    session.exec(delete(Cookable_recipes).where(Cookable_recipes.user_id == user_id, Cookable_recipes.recipe_id == recipe_id))

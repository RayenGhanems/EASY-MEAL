from sqlmodel import Session, select

from app.sql.sql_models import *

def get_ingredient_table(session: Session):
    statement = select(Ingredient)
    return session.exec(statement).all()


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
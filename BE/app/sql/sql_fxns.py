from sqlmodel import Session, select

from sql_models import *

def get_all_ingredients(session: Session):
    statement = select(Ingredient)
    return session.exec(statement).all()
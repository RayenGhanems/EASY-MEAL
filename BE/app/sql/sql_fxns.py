from sqlmodel import Session, select

from app.sql.sql_models import *

def get_ingredient_table(session: Session):
    statement = select(Ingredient)
    return session.exec(statement).all()

def get_user_by_email(username: str, session: Session):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(username: str, password: str, session: Session):
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
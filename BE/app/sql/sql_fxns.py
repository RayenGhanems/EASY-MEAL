from sqlmodel import Session, select

from app.sql.sql_models import *

def get_all_ingredients(session: Session):
    statement = select(Ingredient)
    return session.exec(statement).all()

def get_user_by_email(email: str, session: Session):
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(email: str, password: str, username: str, phone_number: str, session: Session):
    user = User(email=email, password=password, username=username, phone_number=phone_number)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
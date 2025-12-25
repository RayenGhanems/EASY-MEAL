import os
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:123@localhost:5432/DB")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

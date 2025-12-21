from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql://postgres:123@postgres:5432/DB"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


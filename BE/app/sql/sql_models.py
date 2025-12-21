from sqlmodel import SQLModel, Field

class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"

    ingredient: str = Field(primary_key=True, max_length=225)
    quantity: int
    threshold: int

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(primary_key=True, index=True)
    username: str = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=255)
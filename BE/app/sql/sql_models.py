from sqlmodel import SQLModel, Field

class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"

    ingredient: str = Field(primary_key=True, max_length=225)
    quantity: int
    threshold: int

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=255)
    username: str = Field(max_length=100)
    phone_number: str = Field(max_length=15)
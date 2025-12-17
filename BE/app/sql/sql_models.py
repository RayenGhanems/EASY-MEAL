from sqlmodel import SQLModel, Field

class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"

    ingredient: str = Field(primary_key=True, max_length=225)
    quantity: int
    threshold: int
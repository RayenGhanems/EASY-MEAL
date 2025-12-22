from sqlmodel import SQLModel, Field

class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"

    ingredient_id: int = Field(primary_key=True)
    ingredient_name: str = Field(nullable=False, index=True)
    measuring_unit: str = Field(nullable=False)

class StoredIngredients(SQLModel, table=True):
    __tablename__ = "ingredients_stored"

    user_id: int = Field(foreign_key="user.user_id")
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id")
    amount: float
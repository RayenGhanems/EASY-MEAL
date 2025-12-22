from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(primary_key=True)
    username: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
    
class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"

    ingredient_id: int = Field(primary_key=True)
    ingredient_name: str = Field(nullable=False, index=True)
    measuring_unit: str = Field(nullable=False)

class StoredIngredients(SQLModel, table=True):
    __tablename__ = "ingredients_stored"

    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id", primary_key=True)
    amount: float

class RecipeIngredient(SQLModel, table=True):
    __tablename__ = "recipe_ingredients"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id", primary_key=True)
    amount: float

class Recipe(SQLModel, table=True):
    __tablename__ = "recipes"

    recipe_id: int = Field(primary_key=True)
    recipe_name: str = Field(nullable=False, index=True)
    dish_type_id: int = Field(foreign_key="dish_types.dish_type_id",default=None)
    calories: int

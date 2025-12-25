from sqlmodel import SQLModel, Field

from typing import Optional
from datetime import datetime

# =========================================================
# User
# =========================================================

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(primary_key=True)
    username: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)

class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    full_name: Optional[str] = None
    email: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None

# =========================================================
# INGREDIENTS
# =========================================================

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

# =========================================================
# Cookable recipes
# =========================================================

class Cookable_recipes(SQLModel, table=True):
    __tablename__ = "cookable_recipes"

    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)

# =========================================================
# DISH TYPES
# =========================================================

class DishType(SQLModel, table=True):
    __tablename__ = "dish_types"

    dish_type_id: int = Field(primary_key=True)
    dish_type_name: str = Field(nullable=False, index=True)


# =========================================================
# RECIPES
# =========================================================

class Recipe(SQLModel, table=True):
    __tablename__ = "recipes"

    recipe_id: int = Field(primary_key=True)
    recipe_name: str = Field(nullable=False, index=True)
    dish_type_id: int = Field(foreign_key="dish_types.dish_type_id",default=None)
    calories: int

class RecipeIngredient(SQLModel, table=True):
    __tablename__ = "recipe_ingredients"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id", primary_key=True)
    amount: float

class Instruction(SQLModel, table=True):
    __tablename__ = "instructions"

    instruction_id: int = Field(primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.recipe_id")
    step_number: int
    instruction_text: str


class RecipePrepTime(SQLModel, table=True):
    __tablename__ = "recipe_prep_times"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    prep_time: int
    cook_time: int
    total_time: int


class RecipeServing(SQLModel, table=True):
    __tablename__ = "recipe_servings"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    servings: int
    serving_size: Optional[str] = None


class RecipeDietaryLabel(SQLModel, table=True):
    __tablename__ = "recipe_dietary_labels"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    dietary_label: str = Field(primary_key=True)


class RecipeVideo(SQLModel, table=True):
    __tablename__ = "recipe_videos"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    video_url: str = Field(primary_key=True)


class RecipeSource(SQLModel, table=True):
    __tablename__ = "recipe_sources"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    source_name: str
    source_url: Optional[str] = None


class RecipeNote(SQLModel, table=True):
    __tablename__ = "recipe_notes"

    note_id: int = Field(primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.recipe_id")
    note_text: Optional[str] = None


class RecipeTag(SQLModel, table=True):
    __tablename__ = "recipe_tags"

    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    tag_name: str = Field(primary_key=True)


class RecipeComment(SQLModel, table=True):
    __tablename__ = "recipe_comments"

    comment_id: int = Field(primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.recipe_id")
    user_id: int = Field(foreign_key="users.user_id")
    comment_text: str
    comment_date: Optional[datetime] = None


# =========================================================
# USER ↔ RECIPE RELATIONS
# =========================================================

class UserFavorite(SQLModel, table=True):
    __tablename__ = "user_favorites"

    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)


class UserRating(SQLModel, table=True):
    __tablename__ = "user_ratings"

    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    recipe_id: int = Field(foreign_key="recipes.recipe_id", primary_key=True)
    rating: int

class UserDietaryPreference(SQLModel, table=True):
    __tablename__ = "user_dietary_preferences"

    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    dietary_preference: str = Field(primary_key=True)
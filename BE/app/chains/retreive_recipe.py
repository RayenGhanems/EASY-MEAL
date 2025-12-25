from sqlmodel import Session, select
from app.sql.sql_models import *


def get_full_recipe_by_id(session: Session, recipe_id: int) -> dict:
    # --------------------------------------------------
    # 1. Recipe
    # --------------------------------------------------
    recipe = session.exec(
        select(Recipe).where(Recipe.recipe_id == recipe_id)
    ).first()

    if not recipe:
        raise ValueError("Recipe not found")

    # --------------------------------------------------
    # 2. Dish type
    # --------------------------------------------------
    dish_type = None
    if recipe.dish_type_id:
        dish_type = session.exec(
            select(DishType.dish_type_name)
            .where(DishType.dish_type_id == recipe.dish_type_id)
        ).first()

    # --------------------------------------------------
    # 3. Ingredients
    # --------------------------------------------------
    ingredients = session.exec(
        select(
            Ingredient.ingredient_id,
            Ingredient.ingredient_name,
            Ingredient.measuring_unit,
            RecipeIngredient.amount,
            RecipeIngredient.quantity,
        )
        .join(
            RecipeIngredient,
            RecipeIngredient.ingredient_id == Ingredient.ingredient_id,
        )
        .where(RecipeIngredient.recipe_id == recipe_id)
    ).all()

    ingredient_list = [
        {
            "ingredient_id": row.ingredient_id,
            "ingredient_name": row.ingredient_name,
            "amount": row.amount,
            "quantity": row.quantity,
            "unit": row.measuring_unit,
        }
        for row in ingredients
    ]

    # --------------------------------------------------
    # 4. Instructions
    # --------------------------------------------------
    instructions = session.exec(
        select(Instruction)
        .where(Instruction.recipe_id == recipe_id)
        .order_by(Instruction.step_number)
    ).all()

    instruction_list = [
        {
            "step": inst.step_number,
            "text": inst.instruction_text,
        }
        for inst in instructions
    ]

    # --------------------------------------------------
    # 5. Videos
    # --------------------------------------------------
    video = session.exec(
        select(RecipeVideo.video_url)
        .where(RecipeVideo.recipe_id == recipe_id)
    ).first()

    # --------------------------------------------------
    # 6. Ratings
    # --------------------------------------------------
    ratings = session.exec(
        select(
            User.username,
            UserRating.rating,
        )
        .join(User, User.user_id == UserRating.user_id)
        .where(UserRating.recipe_id == recipe_id)
    ).all()

    rating_list = [
        {
            "username": r.username,
            "rating": r.rating,
        }
        for r in ratings
    ]

    # --------------------------------------------------
    # 7. Comments
    # --------------------------------------------------
    comments = session.exec(
        select(
            RecipeComment.comment_text,
            RecipeComment.comment_date,
            User.username,
        )
        .join(User, User.user_id == RecipeComment.user_id)
        .where(RecipeComment.recipe_id == recipe_id)
        .order_by(RecipeComment.comment_date.desc())
    ).all()

    comment_list = [
        {
            "username": c.username,
            "comment": c.comment_text,
            "date": c.comment_date,
        }
        for c in comments
    ]

    # --------------------------------------------------
    # 8. Meta
    # --------------------------------------------------
    prep_time = session.exec(
        select(RecipePrepTime)
        .where(RecipePrepTime.recipe_id == recipe_id)
    ).first()

    serving = session.exec(
        select(RecipeServing)
        .where(RecipeServing.recipe_id == recipe_id)
    ).first()

    labels = session.exec(
        select(RecipeDietaryLabel.dietary_label)
        .where(RecipeDietaryLabel.recipe_id == recipe_id)
    ).all()

    tags = session.exec(
        select(RecipeTag.tag_name)
        .where(RecipeTag.recipe_id == recipe_id)
    ).all()

    # --------------------------------------------------
    # 9. Final response
    # --------------------------------------------------
    return {
        "recipe": {
            "recipe_id": recipe.recipe_id,
            "recipe_name": recipe.recipe_name,
            "calories": recipe.calories,
        },
        "dish_type": dish_type,
        "ingredients": ingredient_list,
        "instructions": instruction_list,
        "videos": video,
        "ratings": rating_list,
        "comments": comment_list,
        "meta": {
            "prep_time": prep_time.dict() if prep_time else None,
            "servings": serving.dict() if serving else None,
            "dietary_labels": [l for l in labels],
            "tags": [t for t in tags],
        },
    }

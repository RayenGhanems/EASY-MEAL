import csv

# define which CSV maps to which table and columns
MAPPINGS = {
    "DB/Recepies/dish_types.csv": ("dish_types", ["dish_type_name"]),
    "DB/Recepies/ingredients.csv": ("ingredients", ["ingredient_name","measuring_unit"]),
    "DB/Recepies/recipes.csv": ("recipes", ["recipe_name","dish_type_id","calories"]),
    "DB/Recepies/recipe_ingredients.csv": ("recipe_ingredients", ["recipe_id","ingredient_id","amount","quantity"]),
    "DB/Recepies/instructions.csv": ("instructions", ["recipe_id","step_number","instruction_text"]),
    "DB/Recepies/users.csv": ("users", ["username","password"]),
    "DB/Recepies/user_favorites.csv": ("user_favorites", ["user_id","recipe_id"]),
    "DB/Recepies/user_ratings.csv": ("user_ratings", ["user_id","recipe_id","rating"]),
    "DB/Recepies/recipe_prep_times.csv": ("recipe_prep_times", ["recipe_id","prep_time","cook_time","total_time"]),
    "DB/Recepies/recipe_servings.csv": ("recipe_servings", ["recipe_id","servings","serving_size"]),
    "DB/Recepies/recipe_dietary_labels.csv": ("recipe_dietary_labels", ["recipe_id","dietary_label"]),
    "recipe_videos.csv": ("recipe_videos", ["recipe_id","video_url"]),
    "DB/Recepies/recipe_sources.csv": ("recipe_sources", ["recipe_id","source_name","source_url"]),
    "DB/Recepies/recipe_notes.csv": ("recipe_notes", ["recipe_id","note_text"]),
    "DB/Recepies/user_dietary_preferences.csv": ("user_dietary_preferences", ["user_id","dietary_preference"]),
    "DB/Recepies/user_profiles.csv": ("user_profiles", ["user_id","full_name","email","profile_picture_url","bio"]),
    "DB/Recepies/recipe_comments.csv": ("recipe_comments", ["recipe_id","user_id","comment_text","comment_date"]),
    "DB/Recepies/recipe_tags.csv": ("recipe_tags", ["recipe_id","tag_name"])
}
print(MAPPINGS["DB/Recepies/dish_types.csv"])
def escape(val):
    """escape single quotes in SQL"""
    return val.replace("'", "''")

with open("DB/seed.sql", "w", encoding="utf-8") as out:
    for csv_file, (table, cols) in MAPPINGS.items():
        print(f"\n📂 Opening CSV: {csv_file} → table `{table}`")

        try:
            with open(csv_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                row_count = 0

                for row in reader:
                    row_count += 1
                    values = []

                    for col in cols:
                        v = row.get(col, "")
                        v = escape(v) if isinstance(v, str) else v
                        values.append("NULL" if v in ("", None) else f"'{v}'")

                    out.write(
                        f"INSERT INTO {table} ({', '.join(cols)}) "
                        f"VALUES ({', '.join(values)});\n"
                    )

                print(f"   ✅ {row_count} rows loaded")

        except FileNotFoundError:
            print(f"   ⚠️ NOT FOUND — skipped")


print("✅ seed.sql generated!")

// Recipes.tsx
import { useEffect, useState } from "react";
import "../style/recipes.css";

type DishType = {
  dish_type_name: string;
  dish_type_id: number;
};

type RecipeDTO = {
  recipe: { recipe_id: number; recipe_name: string; calories: number };
  dish_type: string | null;
  ingredients: {
    ingredient_id: number;
    ingredient_name: string;
    amount: any;
    quantity: any;
    unit: string;
  }[];
  instructions: { step: number; text: string }[];
  videos: string | null;
  ratings: { username: string; rating: number }[];
  comments: { username: string; comment: string; date: string }[];
  meta: {
    prep_time: any;
    servings: any;
    dietary_labels: any[];
    tags: any[];
  };
};

export default function Recipes() {
  const [recipes, setRecipes] = useState<RecipeDTO[]>([]);
  const [dishTypes, setDishTypes] = useState<DishType[]>([]);
  const [dishInput, setDishInput] = useState("ALL");
  const [selectedDishType, setSelectedDishType] = useState("ALL");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string>("");

  useEffect(() => {
    async function fetchDishTypes() {
      try {
        const response = await fetch("http://localhost:8000/dish_type", {
          method: "GET",
          credentials: "include",
        });

        const data = await response.json();
        const types = Array.isArray(data) ? data : [];

        // Ensure ALL exists in suggestions
        const hasAll = types.some(
          (t: DishType) => (t.dish_type_name || "").toUpperCase() === "ALL"
        );
        const withAll = hasAll
          ? types
          : [{ dish_type_name: "ALL", dish_type_id: 0 }, ...types];

        setDishTypes(withAll);
      } catch (error) {
        console.error("Error fetching dish types:", error);
        setErrorMsg("Failed to load dish types.");
      }
    }
    fetchDishTypes();
  }, []);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      setErrorMsg("");

      const pref = selectedDishType || "ALL";
      const res = await fetch(
        `http://localhost:8000/get_recipes?dish_preference=${encodeURIComponent(
          pref
        )}`,
        { credentials: "include" }
      );

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();
      setRecipes(Array.isArray(data?.recipes) ? data.recipes : []);
    } catch (e) {
      console.error(e);
      setErrorMsg("Failed to load recipes.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="recipesPage">
      <div className="recipesHeader">
        <div className="recipesTitle">Recipes Page</div>

        <div className="recipesControls">
          <input
            className="dishInput"
            placeholder="Choose a type (e.g. ALL)"
            list="dish_types"
            value={dishInput}
            onChange={(e) => {
              const value = e.target.value;
              setDishInput(value);

              const match = dishTypes.find((t) => t.dish_type_name === value);

              // Store the backend expected string (dish_type_name)
              setSelectedDishType(match ? match.dish_type_name : value);
            }}
          />

          <datalist id="dish_types">
            {dishTypes.map((t) => (
              <option key={t.dish_type_id} value={t.dish_type_name} />
            ))}
          </datalist>

          <button
            className="getRecipesBtn"
            onClick={fetchRecipes}
            disabled={loading}
          >
            {loading ? "Loading..." : "Get recipes"}
          </button>
        </div>

        {errorMsg ? <div className="errorMsg">{errorMsg}</div> : null}
      </div>

      <div className="recipesGrid">
        {recipes.map((r) => (
          <div className="recipeCard" key={r.recipe.recipe_id}>
            <div className="recipeCardHeader">
              <div className="recipeName">{r.recipe.recipe_name}</div>
              <div className="recipeMetaRow">
                <div className="recipeType">Type: {r.dish_type ?? "ALL"}</div>
                <div className="recipeCalories">
                  Calories: {r.recipe.calories}
                </div>
              </div>
            </div>

            <div className="recipeSection">
              <div className="sectionTitle">Ingredients</div>
              <div className="ingredientsList">
                {r.ingredients.map((ing) => (
                  <div className="ingredientRow" key={ing.ingredient_id}>
                    <div className="ingredientName">{ing.ingredient_name}</div>
                    <div className="ingredientQty">
                      {ing.quantity} {ing.unit}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="recipeSection">
              <div className="sectionTitle">Instructions</div>
              <div className="stepsList">
                {r.instructions.map((s) => (
                  <div className="stepRow" key={s.step}>
                    <div className="stepNumber">{s.step}</div>
                    <div className="stepText">{s.text}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

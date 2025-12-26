import { useEffect, useState } from "react";
import "../style/recipes.css";

export default function Recipes() {
  type DishType = {
    dish_type_name: string;
    dish_type_id: number;
  };
  const [dish_types, setDishTypes] = useState<DishType[]>([]);
  const [dishInput, setDishInput] = useState("");
  const [SelectedDishType, setSelectedDishType] = useState<number | "">("");

  useEffect(() => {
    async function fetchDishTypes() {
      try {
        const response = await fetch("http://localhost:8000/dish_type", {
          method: "GET",
          credentials: "include",
        });

        const data = await response.json();
        const types = Array.isArray(data) ? data : [];
        setDishTypes(types);
      } catch (error) {
        console.error("Error fetching dish types:", error);
      }
    }
    fetchDishTypes();
  }, []);

  const handleGetRecipes = async () => {
    try {
      const response = await fetch("http://localhost:8000/get_recipes", {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      console.log("Fetched recipes:", data);
    } catch (error) {
      console.error("Error fetching recipes:", error);
    }
  };
  return (
    <div className="recipe_page">
      <h1>Recipes Page</h1>
      <div>
        <input
          placeholder="choose a type"
          list="dish_types"
          value={dishInput}
          onChange={(e) => {
            const value = e.target.value;
            setDishInput(value);
            const selectedType = dish_types.find(
              (type) => type.dish_type_name === value
            );
            setSelectedDishType(selectedType ? selectedType.dish_type_id : "");
            console.log("Selected Dish Type ID:", SelectedDishType);
          }}
        />
        <datalist id="dish_types">
          {dish_types.map((type) => (
            <option key={type.dish_type_id} value={type.dish_type_name}>
              {type.dish_type_name}
            </option>
          ))}
        </datalist>
        <button onClick={() => handleGetRecipes()}>get recipes</button>
      </div>
    </div>
  );
}

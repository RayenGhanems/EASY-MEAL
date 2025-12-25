import { useEffect, useState } from "react";

export default function Recipes() {
  type DishType = {
    dish_type_name: string;
    dish_type_id: number;
  };
  const [dish_types, setDishTypes] = useState<DishType[]>([]);
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

  return (
    <div>
      <h1>Recipes Page</h1>
      <div>
        Select a dish type:
        <select
          value={SelectedDishType}
          onChange={(e) => {
            setSelectedDishType(Number(e.target.value));
          }}
        >
          {dish_types.map((type) => (
            <option key={type.dish_type_id} value={type.dish_type_id}>
              {type.dish_type_name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

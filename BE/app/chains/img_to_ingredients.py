from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from typing import Literal

from dotenv import load_dotenv; load_dotenv()

# ---------- Pydantic schema ----------

class Item(BaseModel):
    ingredient: str = Field(
        ..., description="single-word name of the item (e.g. milk, cheese, apple)"
    )
    quantity: int = Field(
        ..., description="number of this item visible in the image"
    )
    unit: Literal["kg", "g", "ml", "l", "pcs"] = Field(
        "kg", description="discribes the unit of mesurment (e.g. kg, g, ml, l, pcs)"
    )


class StructuredOutput(BaseModel):
    ingredients: list[Item]


# ---------- Output parser ----------

parser = PydanticOutputParser(pydantic_object=StructuredOutput)
format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")



# --------------Task Discription ------------
Task_Discription = "Analyze the fridge image and count each ingredient."
# ---------- Prompt (VISION-AWARE) ----------

prompt = ChatPromptTemplate.from_messages([
    ("system",  "You are a helpful assistant. "
                "You will be given an image of a fridge, and you must name each ingredient you see and count how many of each ingredient appears. "
                "You MUST follow the output format exactly as instructed."
                "You MUST output units from: kg, g, ml, l, pcs."
                "If the real-world unit is something else (cans, bottles, packs) translate them to:"
                "- Liquids → l"
                "- Solids → pcs"
                "- Cans → kg"
                "- Never output other unit strings"),
    ("human", [ {"type": "text", "text": "{task_description}"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,{image_base64}"}},
                {"type": "text", "text": "{format_output_instructions}"}])
]).partial(format_output_instructions=format_instructions, task_description = Task_Discription)


# ---------- Vision model ----------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ---------- Runnable chain ----------

img_to_ingredients_chain = prompt | llm | parser
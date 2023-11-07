import gradio as gr
import os
import numpy as np
from openai_interface import OpenAIInterface
from parse_ingredients import parse_ingredients
from test import workflow
from doordash import order

def get_ingredients_recipe(text, fridge_image:np.ndarray=None):
    openai_interface = OpenAIInterface(api_key='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')
    ingredients_prompt = f"""
    You are helping me make the food I want to eat. I want to cook {text} today.
    Please give me an itemized list of ingredients in numbered list format, where each item is in the format of 'Item:Quantity'. Then, after the heading recipe, give 
    me a step by step recipe.
    """
    numbered_ingredients = openai_interface.predict_text(ingredients_prompt, temp=1)
    numbered_ingredients, recipe = numbered_ingredients.split("Recipe:", 1)
    ingredients = parse_ingredients(numbered_ingredients)
    # TODO: swap out example_ingredients for GPT-V4 output
    to_purchase, fridge_contents = workflow(ingredients, example_ingredients="""
    1. Hot sauce (looks like Sriracha)
    2. Two takeout containers with brown lids
    3. Bottle of white wine
    4. Creamer (possibly a non-dairy type based on the label)
    5. Pack of mushrooms
    6. Carbonated drink (White Claw)
    7. Butter or margarine tub (blue lid)
    8. Yogurt tubs (different flavors)
    9. Plastic container with wrapped items (possibly cheese or deli meat)
    10. A container with leafy greens (possibly spinach or mixed greens)
    11. Small red container with a lid
    12. Takeout container with a clear lid (contents not fully visible)
    13. A container of pasta sauce

    *Door Section:*
    1. Starbucks iced coffee bottle
    2. Mozzarella cheese with water content (jar with red and white checkered lid)
    3. Various bottles and jars of condiments including:
    - Sweet hot mustard
    - Pickle jar
    - Olive oil (or similar)
    - Red bottle that might be hot sauce
    - Few other assorted bottles and jars with labels not clearly visible
    4. Carbonated drink (looks like another White Claw)
    5. Chobani Oat Milk Creamer
    """)

    print('to_purchase', to_purchase)
    print('fridge_contents', fridge_contents)
    print('Recipe', recipe)

    items_only = [tp.split(':')[0] for tp in to_purchase]
    order(items_only)
    return recipe.strip(), fridge_contents, '\n'.join(items_only)


with gr.Blocks() as demo:

    txt = gr.Textbox(label="What dish do you want to make today?", lines=2)
    # TODO: Call UI interaction for this
    with gr.Row():
        im = gr.Image(label="What's in your fridge?")

    btn = gr.Button(value="Ask Cartesan for a recipe!")
    fridge_contents = gr.Textbox(value="", label="Current Fridge Contents")
    purchase = gr.Textbox(value="", label="Ingredients Being Purchased")
    output_txt = gr.Textbox(value="", label="Recipe")
    btn.click(get_ingredients_recipe, inputs=[txt, im], outputs=[output_txt, fridge_contents, purchase])

if __name__ == "__main__":
    demo.launch()

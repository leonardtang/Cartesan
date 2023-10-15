import gradio as gr
import os
import numpy as np
from openai_interface import OpenAIInterface
from parse_ingredients import parse_ingredients
from test import workflow

def get_ingredients_recipe(text, fridge_image:np.ndarray=None):
    print("fridge Image", fridge_image)
    openai_interface = OpenAIInterface(api_key='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')
    ingredients_prompt = f"""
    You are helping me make the food I want to eat. I want to cook {text} today.
    Please give me an itemized list of ingredients in numbered list format. Then, after the heading recipe, give 
    me a step by step recipe.
    """
    numbered_ingredients = openai_interface.predict_text(ingredients_prompt, temp=1)
    print('numbered_ingredients', numbered_ingredients)
    numbered_ingredients, recipe = numbered_ingredients.split("Recipe:", 1)
    ingredients = parse_ingredients(numbered_ingredients)
    # TODO: swap out example_ingredients for GPT-V4 output
    to_purchase, fridge_contents = workflow(ingredients, example_ingredients="""
    1. Beef
    2. Peppers
    3. Beans
    4. Salsa
    """)

    print('to_purchase', to_purchase)
    print('fridge_contents', fridge_contents)
    print('Recipe', recipe)
    return recipe.strip()

def mirror(x):
    return x


with gr.Blocks() as demo:

    txt = gr.Textbox(label="What dish do you want to make today?", lines=2)

    # TODO: Call UI interaction for this
    with gr.Row():
        im = gr.Image()
    # btn = gr.Button(value="Upload a Picture of your Fridge")
    # btn.click(mirror, inputs=[im])

    btn = gr.Button(value="Ask Cartesan!")
    output_txt = gr.Textbox(value="", label="Recipe")
    btn.click(get_ingredients_recipe, inputs=[txt, im], outputs=[output_txt])

if __name__ == "__main__":
    demo.launch()

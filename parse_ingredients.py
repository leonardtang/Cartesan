import re

from openai.embeddings_utils import cosine_similarity

import openai_api


model = 'gpt-4'

agent = openai_api.OpenAI_API(model=model)

def get_required_ingredients(food_name:str):
    prompt = f"""
    List the ingredients required to make {food_name} (Just create a numbered list of items with no other text or information)
    
    <Example Format>
    1. Hot sauce
    2. Potatoes
    3. Water
    
    <Ingredients to make {food_name}>
    """
    response = agent.chatgpt(prompt)
    return response
    

def get_ingredients_to_buy_embedding(ingredients_we_need, ingredients_we_have, threshold=0.5):
    ingredients = [i for i in range(len(ingredients_we_need))]
    for index, ingredient in enumerate(ingredients_we_need):
        for ingredient_in_fridge in ingredients_we_have:
            if cosine_similarity(ingredient, ingredient_in_fridge) > threshold:
                ingredients.remove(index)
                break
    return ingredients

def get_ingredients_to_buy(food_name, ingredients_we_need, ingredients_we_have):
    prompt = f"""
    We are trying to make {food_name} and we need the following ingredients:
    {ingredients_we_need}
    
    But we only have the following ingredients at home:
    {ingredients_we_have}
    
    List all of the ingredients we need to buy in this format, don't include the items we have at home or can be used to make the ingredients required for making the food (Just output the list of ingredients with no other information or text):
    <Example Format>
    1. Hot sauce
    2. Brown containers
    3. Water
    
    <Ingredients to buy to make {food_name}>
    """
    response = agent.chatgpt(prompt)
    return parse_ingredients(response)

def parse_ingredients(response_str):
    # pattern = re.compile(r'(?<=\d\.\s)([^\n]+)', re.MULTILINE)
    items = re.findall(r'(?<=\d\.\s)([^\n]+)', response_str)
    items = [item.strip() for item in items]
    return items

# ----- Example -----
# prompt = """
# List all of the ingredients inside this image in this format (Just the list of ingredients with no other information/text): 

# 1. A bottle of hot sauce (with a rooster label)
# 2. Two brown containers (possibly leftovers or some kind of takeout)
# 3. A bottle of white liquid, labeled "CREAMER" (presumably a coffee creamer)
# 4. Three mushrooms on a shelf
# 5. A can of sparkling water or drink (with a bird design)
# """

# # response = openai.gpt4v(prompt, image)
# response = """
# 1. Starbucks Iced Coffee bottle
# 2. White Claw hard seltzer can
# 3. Blue container (brand or content not visible)
# 4. Nando's Peri-Peri sauce bottle
# 5. 365 Everyday Value product (specific content not visible)
# 6. Strawberry jam jar
# """

# parse_ingredients(response)
# ['Starbucks Iced Coffee bottle',
#  'White Claw hard seltzer can',
#  'Blue container (brand or content not visible)',
#  "Nando's Peri-Peri sauce bottle",
#  '365 Everyday Value product (specific content not visible)',
#  'Strawberry jam jar']
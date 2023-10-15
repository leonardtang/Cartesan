import json
from datetime import datetime

import parse_ingredients
import openai_api

# Ingredients in the fridge
example_ingredients = """
1. Beef
2. Peppers
3. Beans
4. Salsa
"""

def test_parse_ingredients(str, desired_output=None):
    if desired_output is not None:
        assert(parse_ingredients.parse_ingredients(str) == desired_output)
    else:
        print(parse_ingredients.parse_ingredients(str))

def test_required_ingredients(food_name, desired_output=None):
    if desired_output is not None:
        assert(parse_ingredients.get_required_ingredients(food_name) == desired_output)
    else:
        print(parse_ingredients.get_required_ingredients(food_name))

def check_ingredients(required_ingredients, ingredients_to_buy):
    for ingredient in ingredients_to_buy:
        if ingredient not in required_ingredients:
            ingredients_to_buy.remove(ingredient)
    return ingredients_to_buy

def update_db(data, ingredients_in_fridge):
    new_fridge_json = {
        "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "ingredients in fridge": ingredients_in_fridge
    }
    data.append(new_fridge_json)
    json.dump(data, open(f'ingredients.json', 'w'))

def get_ingredients_in_fridge():
    return example_ingredients

def workflow(required_ingredients, example_ingredients):
    data = json.load(open(f'ingredients.json'))
    
    # food_name = input("What food do you want to make?\n")
    # required_ingredients = parse_ingredients.parse_ingredients((parse_ingredients.get_required_ingredients(food_name)))
    # required_ingredients = parse_ingredients.parse_ingredients((required_ingredients_raw))
    # print(f"\nRequired ingredients for {food_name}:\n{required_ingredients}")
    ingredients_in_fridge = parse_ingredients.parse_ingredients(example_ingredients)
    print(f"\nIngredients in fridge:\n{ingredients_in_fridge}")
    update_db(data, ingredients_in_fridge)
    
    required_ingredients_embeddings = [openai_api.get_embedding(ingredient) for ingredient in required_ingredients]
    ingredients_in_fridge_embeddings = [openai_api.get_embedding(ingredient) for ingredient in ingredients_in_fridge]
    ingredients_to_buy = parse_ingredients.get_ingredients_to_buy_embedding(required_ingredients_embeddings, ingredients_in_fridge_embeddings, threshold=0.85)
    ingredients_to_buy = [required_ingredients[ingredient_index] for ingredient_index in ingredients_to_buy]
    
    # print("\n----------\n")
    # print(f"\nIngredients to buy (indexes):\n{ingredients_to_buy}")
    # print(f"\nIngredients to buy (Embedding Search):\n{ingredients_to_buy}")
    # print("\n----------\n")
    # ingredients_to_buy = check_ingredients(required_ingredients, parse_ingredients.get_ingredients_to_buy(food_name, required_ingredients, ingredients_in_fridge))
    print(f"\nIngredients to buy (LLM Search):\n{ingredients_to_buy}")
    
    return ingredients_to_buy, data

if __name__ == "__main__":
    workflow()
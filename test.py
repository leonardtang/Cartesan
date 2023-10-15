import parse_ingredients

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

def get_ingredients_in_fridge():
    return example_ingredients

def workflow():
    food_name = input("What food do you want to make?\n")
    required_ingredients = parse_ingredients.get_required_ingredients(food_name)
    print(f"Required ingredients for {food_name}:\n{required_ingredients}")
    ingredients_in_fridge = parse_ingredients.parse_ingredients(get_ingredients_in_fridge())
    print(f"Ingredients in fridge:\n{ingredients_in_fridge}")
    ingredients_to_buy = parse_ingredients.get_ingredients_to_buy(food_name, required_ingredients, ingredients_in_fridge)
    print(f"Ingredients to buy:\n{ingredients_to_buy}")
    

if __name__ == "__main__":
    workflow()
import re

def parse_ingredients(response_str):
    pattern = re.compile(r'^\d+\.\s+(.+)$', re.MULTILINE)
    items = re.findall(pattern, response_str)
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
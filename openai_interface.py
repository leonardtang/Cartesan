import openai
from openai.error import RateLimitError
import logging
import os
from parse_ingredients import parse_ingredients
from tqdm import tqdm

class OpenAIInterface:
    def __init__(self, api_key=None):
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")

        if not openai.api_key:
            logging.getLogger('sys').warning(f'No OpenAI API key given!')

    def predict_text(self, prompt, max_tokens=100, temp=0.8, mode='chat', prompt_as_chat=False):
        try:
            if mode == 'chat':
                if prompt_as_chat:
                    message = prompt
                else:
                    message = [{"role": "user", "content": prompt}]

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=message,
                    temperature=temp
                )
                return response['choices'][0]['message']['content']
            elif mode == 'chat-gpt4':
                if prompt_as_chat:
                    message = prompt
                else:
                    message = [{"role": "user", "content": prompt}]

                response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=message,
                temperature=temp
                )
                return response['choices'][0]['message']['content']
            else:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    temperature=temp,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                return response.choices[0].text
        except RateLimitError as e:
            logging.getLogger('sys').error(f'[WARN] OpenAIInterface: Rate Limit Exceeded! {e}')
            return '0'
        except Exception as e:
            logging.getLogger('sys').error(f'[ERROR] OpenAIInterface: Unexpected exception- {e}')
            return '-1'

if __name__ == '__main__':
    openai_interface = OpenAIInterface()
    ingredients_prompt = """
    You are helping me make the food I want to eat. I want to cook spaghetti with tomato sauce for 2 people today.
    Please give me an itemized list of ingredients in numbered list format. Then, after the heading recipe, give 
    me a step by step recipe.
    """
    numbered_ingredients = openai_interface.predict_text(ingredients_prompt, temp=1)
    numbered_ingredients, recipe = numbered_ingredients.split("Recipe:", 1)
    ingredients = parse_ingredients(numbered_ingredients)
    print(ingredients)
    print(recipe)
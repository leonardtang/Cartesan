import os
import numpy as np

import openai
# import tiktoken
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API Key
openai.api_key = os.environ.get('OPENAI_KEY')

model = "gpt-3.5-turbo"
system_message = "You are a helpful assistant"
query = "Explain self-attention"

class OpenAI_API:
    def __init__(self, model=model, system_message=system_message):
        self.model = model
        self.system_message = system_message

    def chatgpt(self, query):
        messages = [
            {"role":"system", "content":self.system_message},
            {"role":"user", "content":query}
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages).choices[0].message.content
        return response
    # def token_count(self, text):
    #     encoding = tiktoken.encoding_for_model(self.model)
    #     num_tokens = len(encoding.encode(text))
    #     return num_tokens

def get_embedding(query):
    # if isinstance(query, list):
    #     query = "\n".join(query)
    if isinstance(query, str):
        query = query.replace("\n", " ")
    return openai.Embedding.create(input = [query], model="text-embedding-ada-002")['data'][0]['embedding']

def cosine_similarity(embedding1, embedding2):
    """
    Compute the cosine similarity between two normalized sentence embeddings.

    Parameters:
    - embedding1: 1D numpy array representing the first normalized sentence embedding
    - embedding2: 1D numpy array representing the second normalized sentence embedding

    Returns:
    - similarity: cosine similarity between the two embeddings
    """
    # Since the vectors are normalized, cosine similarity is simply the dot product of the vectors.
    similarity = np.dot(embedding1, embedding2)
    return similarity
    
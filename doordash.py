from os import access
from pprint import pprint
from random import randint
from typing import List, Dict
import jwt.utils
import time
import math
import openai
import requests

openai.api_key = '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'
openai.Model.list()

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def format_items(items) -> List[Dict]:
    end_items = []
    for item in items:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at describing grocery store items."},
                {"role": "user", "content": f"Can you describe in one brief sentence the following grocery item: {item}"},
            ]
        )
        end_item = {
            'name': item,
            'description': response['choices'][0]['message']['content'],
            'quantity': 1, # TODO: handle quantity in ingredient parsing as well
        }
        end_items.append(end_item)
    return end_items

def order(items: List[Dict]):
    accessKey = {
        "developer_id": "a1dbb931-27bf-4a52-8559-997def384ff9",
        "key_id": "6aa131a7-567a-491a-b8ad-04e7034d7142",
        "signing_secret": "UIRceqEVOLuUe8l0lfx_jg0gQNwzy3UkSHE2RZ_cqQw"
    }

    token = jwt.encode(
        {
            "aud": "doordash",
            "iss": accessKey["developer_id"],
            "kid": accessKey["key_id"],
            "exp": str(math.floor(time.time() + 300)),
            "iat": str(math.floor(time.time())),
        },
        jwt.utils.base64url_decode(accessKey["signing_secret"]),
        algorithm="HS256",
        headers={"dd-ver": "DD-JWT-V1"})

    endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"
    headers = {"Accept-Encoding": "application/json",
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"}

    deliv_id = f"D-{random_with_N_digits(12)}"
    request_body = {
        "external_delivery_id": deliv_id,
        "pickup_address": "1450 Howard Ave, Burlingame, CA 94010",
        "pickup_business_name": "Wells Fargo SF Downtown",
        "pickup_phone_number": "+18603578008",
        "pickup_instructions": "",
        "dropoff_address": "1868 Floribunda Ave, Hillsborough, CA 94010",
        "dropoff_business_name": "Wells Fargo SF Downtown",
        "dropoff_phone_number": "+18603578008",
        "dropoff_instructions": "Call Leonard Tang at dropoff phone number",
        "order_value": 1999,
        # "items": [
        #     {
        #         "name": "Mega Bean and Cheese Burrito",
        #         "description": "Mega Burrito contains the biggest beans of the land with extra cheese.",
        #         "quantity": 1,
        #         # "external_id": "123-123443434b",
        #         # "external_instance_id": 12,
        #         # "volume": 5.3,
        #         # "weight": 2.8,
        #         # "length": 2.8,
        #         # "width": 2.8,
        #         # "height": 2.8,
        #         # "price": 1000,
        #         # "barcode": 12342830041,
        #         # "item_options": {}
        #     }
        # ]
        "items": format_items(items)
        # TODO: include list of DeliveryItems
    }

    create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request
    pprint(create_delivery.text)

    time.sleep(2)
    cancel_endpoint = f"https://openapi.doordash.com/drive/v2/deliveries/{request_body['external_delivery_id']}/cancel"
    cancel_request = requests.put(cancel_endpoint, headers=headers, json=request_body["external_delivery_id"])
    pprint(cancel_request.text)

if __name__ == "__main__":
    order(items=['Apple'])
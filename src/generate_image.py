import http.client
import json
import os
import pprint
import time

from dotenv import load_dotenv
from util.custom_logger import CustomLogger

# set logger
logger = CustomLogger()

 # load OpenAI credentials
load_dotenv()

if os.getenv("IMAGINE_TOKEN", default="False"):
    IMAGINE_TOKEN = os.getenv("IMAGINE_TOKEN")
    logger.info("successfully loaded API Token")
else:
    raise ValueError("no API Token found")

prompts = ['A vibrant, affordable housing complex in Singapore with pet-friendly areas, giant cats sculptures, colourful family parks, and lush green spaces', 'A lush, well-shaded recreational area in Singapore with running tracks, sheltered walkways, rest areas, and vibrant play spaces promoting work-life balance', 'An open park in Singapore with shaded areas for exercise, cycling paths, and facilities for various outdoor activities, promoting a healthy lifestyle']

data = {
    "prompt": prompts[0]
}
 
headers = {
    'Authorization': f"Bearer {IMAGINE_TOKEN}", 
    'Content-Type': 'application/json'
}


# send data to imagine API
def send_request(method, path, body=None, headers={}):
    conn = http.client.HTTPSConnection("cl.imagineapi.dev")
    conn.request(method, path, body=json.dumps(body) if body else None, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode('utf-8'))
    pprint.pp(data)
    conn.close()
    return data
 

prompt_response_data = send_request('POST', '/items/images/', data, headers) 


# retrieve the generated images
def check_image_status():
    response_data = send_request('GET', f"/items/images/{prompt_response_data['data']['id']}", headers=headers)
    if response_data['data']['status'] in ['completed', 'failed']:
        print('Completed image details',)
        pprint.pp(response_data['data'])
        return True
    else:
        print(f"Image is not finished generation. Status: {response_data['data']['status']}")
        return False
 

while not check_image_status():
    time.sleep(5)  # wait for 5 seconds
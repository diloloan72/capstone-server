import io
import sys
import base64

from flask import Flask
from flask import request
from google.cloud import vision

BASE_64_TAG = ';base64,'

app = Flask(__name__)

@app.route('/detect_logos', methods=['POST'])
def detect_logos():
    data = request.json
    image_base_64 = preprocess_image_str(data['image_base_64'])
    logos = detect_logos_from_google(image_base_64)
    return {'logos': logos}

def preprocess_image_str(image_str):
    i = image_str.find(BASE_64_TAG) + len(BASE_64_TAG)
    return image_str[i:]

def detect_logos_from_google(content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    response = client.logo_detection(image=image)

    if check_for_error(response): 
        return []

    logos = response.logo_annotations

    logo_names = [] 
    for logo in logos:
        logo_names.append(logo.description)
    print('Logos:', logo_names)

    return logo_names

def check_for_error(response): 
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))
        return True    
    return False

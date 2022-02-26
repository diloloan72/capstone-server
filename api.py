import io
import os
import sys
import base64

from flask import Flask, send_from_directory
from flask import request
from google.cloud import vision

PROD = os.environ['FLASK_ENV'] == 'prod'
BASE_64_TAG = ';base64,'

if PROD:
    app = Flask(__name__, static_folder='../public_html', static_url_path='')
else:
    app = Flask(__name__)

@app.route('/secret')
def secret():
    return "nguoi yeu cua loan yeu loan lam co biet ko"
    
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

@app.route('/')
def serve():
    if PROD:
        return send_from_directory(app.static_folder, 'index.html')
    return 'Not in production'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
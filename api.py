import io
import sys

from flask import Flask
from flask import request
from google.cloud import vision


app = Flask(__name__)

@app.route('/detect_logos', methods=['POST'])
def detect_logos():
    image = request.json
    print(image)
    return {'logos': 'fb'}

def detect_logos_from_google(path):
    """Detects logos in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))
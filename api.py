import io
import os
import sys
import base64


from flask import Flask, send_from_directory
from flask import request
from google.cloud import vision


# Define constants 
BASE_64_TAG = ';base64,' 


# Set up app based on prod vs dev environment 
PROD = os.environ['FLASK_ENV'] == 'prod'
if PROD:
    app = Flask(__name__, static_folder='frontend', static_url_path='')
else:
    app = Flask(__name__)
    

@app.route('/detect_logos', methods=['POST'])
def detect_logos():
    '''
    Detects logos in the provided image string 

    Parameters
    ----------
    None, but an image string is expected in the request

    Returns
    -------
    dict: Dictionary with a single key 'logos' mapping to a list of logos detected
    '''

    data = request.json
    image_base_64 = preprocess_image_str(data['image_base_64'])
    logos = detect_logos_from_google(image_base_64)
    return {'logos': logos}


def preprocess_image_str(image_str):
    '''
    Helper function to sanitize the image string to base64

    Parameters
    ----------
    image_str: str
        The image string before sanitization 

    Returns
    -------
    str: The processed image string that represents the image in base64
    '''

    i = image_str.find(BASE_64_TAG) + len(BASE_64_TAG)
    return image_str[i:]


def detect_logos_from_google(content):
    '''
    Helper function to detect logos using Google API 

    Parameters
    ----------
    content: str
        The image in base64

    Returns
    -------
    logo_names: list of str 
        Name(s) of the logo(s) detected in the image 
    '''

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
    '''
    Helper function to check if there are any errors in the API response.
    If there is an error, then raise an exception 

    Parameters
    ----------
    response: The response from Google API

    Returns
    -------
    bool: True if error is detected. False otherwise.  
    '''

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))
        return True    
    return False


@app.route('/')
def serve():
    '''
    Serves the frontend in production. Does nothing if not in production
    '''
    if PROD:
        return send_from_directory(app.static_folder, 'index.html')
    return 'Not in production'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
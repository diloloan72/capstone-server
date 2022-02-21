from flask import Flask

app = Flask(__name__)

@app.route('/detect_logos')
def detect_logos():
    return {'logos': 'fb'}
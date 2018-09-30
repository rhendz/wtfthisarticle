## Runs the Flask API protocols
from flask import Flask, jsonify
import json
import os
app = Flask(__name__)

from main import getInitJSON

@app.route("/")
def someJSON():
    return jsonify('modules/json/init.json')

if __name__ == '__main__':
    try:
        os.remove('modules/json/relatedLinks.json') # Special appended file
    except Exception as e:
        pass # This is fine, that means the links were already deleted
    getInitJSON(input('Enter a Url: \n'))
    app.run(debug=True)

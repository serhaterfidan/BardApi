from flask import Flask, request, jsonify
from bardapi import Bard
import os

app = Flask(__name__)

# If running locally, set your local API token here
# API_TOKEN = 'xxxxxxx'

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        # Retrieve the API token from the request header
        API_TOKEN = request.headers.get('Authorization')
        if not API_TOKEN:
            return jsonify({'error': 'No API token provided in the request header.'}), 401

        # Initialize Bard API with the token from the header
        bard = Bard(token=API_TOKEN)

        # Extract the input text from the incoming JSON request
        data = request.get_json()
        input_text = data.get('input_text', '')

        # Send the input text to the Bard API and get a response
        response = bard.get_answer(input_text)

        answer = response['content']

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': 'Failed to process the request.', 'details': str(e)}), 500

if __name__ == '__main__':
    # For cyclic.sh deployment, use the environment variable for the port
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

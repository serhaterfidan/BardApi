from flask import Flask, request, jsonify
from bardapi import Bard
import os

app = Flask(__name__)

# If running locally, set your local API token here
# API_TOKEN = 'xxxxxxx'

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        # Extract the input text and authentication token from the incoming JSON request
        data = request.get_json()
        
        # Extract the input text and authentication token from the query parameters
        auth_token = request.args.get('Secure_1PSID', '')

        # Authenticate the user based on the provided token
        if not auth_token:
            return jsonify({'error': 'Unauthorized. Invalid or missing Secure_1PSID.'}), 401

        bard = Bard(token=auth_token, timeout=30)

        input_text = data.get('input_text', '')

        # Send the input text to the Bard API and get a response
        response = bard.get_answer(input_text)

        answer = response['content']

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': 'Failed to process the request.', 'details': str(e)}), 500

if __name__ == '__main__':
    # For cyclic.sh deployment, use the environment variable for the port
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

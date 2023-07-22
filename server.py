from flask import Flask, request, jsonify
from bardapi import Bard
import os

app = Flask(__name__)

bard = Bard(token='ZAgZafeVB6EsbfaMkjmhxjM3XgAETXIk-5uqqbZo8vYvO0b0glmprjnYkdI-iUQKn7yi3g.')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        # Extract the input text from the incoming JSON request
        data = request.get_json()
        input_text = data.get('input_text', '')

        print("Input Text:", input_text)

        # Send the input text to the Bard API and get a response
        response = bard.get_answer(input_text)

        print("API Response:", response)

        answer = response['content']

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': 'Failed to process the request.', 'details': str(e)}), 500
if __name__ == '__main__':
    # For local development, run the server on localhost
    app.run(host='0.0.0.0', port=8000)

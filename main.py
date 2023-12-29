from flask import Flask, request, jsonify
from extractor import get_data
import base64
import io
import requests
import tempfile
import os

app = Flask(__name__)

def download_image(url, temp_image_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(temp_image_path, 'wb') as temp_image:
            temp_image.write(response.content)
        return True
    else:
        return False

@app.route('/process_passport', methods=['POST'])
def process_passport():
    try:
        # Assuming you are receiving the image URL in the 'img_url' field
        img_url = request.json.get('img_url', '')

        # Generate a temporary file path
        temp_image_path = tempfile.mktemp(suffix=".png")

        # Download and save the image locally
        if download_image(img_url, temp_image_path):
            # Process the passport image
            user_info = get_data(temp_image_path)

            # Respond with the extracted information
            return jsonify(user_info)
        else:
            return jsonify({'error': 'Failed to download the image'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
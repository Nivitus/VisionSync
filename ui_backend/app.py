from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static')

AI_SERVICE_URL = "http://localhost:5000/detect"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    files = {'image': (image.filename, image.read(), image.content_type)}

    try:
        response = requests.post(AI_SERVICE_URL, files=files, timeout=30)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.RequestException as e:
        app.logger.error("Error connecting to AI service: {}".format(str(e)))
        return jsonify({'error': 'AI service error. Please try again later.'}), 500

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory('../ai_backend/outputs', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
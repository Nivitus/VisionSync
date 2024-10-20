from flask import Flask, request, jsonify
from model.model_utils import load_model, process_image
import os
import uuid
import json
import random

app = Flask(__name__)

model = load_model()

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    
    # unique filenames
    unique_id = random.randint(1, 999)
    output_image_filename = "output_image_{}.jpg".format(unique_id)
    output_json_filename = "output_results_{}.json".format(unique_id)

    results = process_image(model, image, output_image_filename)

    # write the JSON files
    with open(os.path.join('outputs', output_json_filename), 'w') as f:
        json.dump(results['detections'], f, indent=2)

    return jsonify({
        'detections': results['detections'],
        'output_image': output_image_filename,
        'output_json': output_json_filename
    }), 200

if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
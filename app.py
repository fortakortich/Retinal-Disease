from flask import Flask, request, jsonify
from predict_utils import load_model, predict_image
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
model = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    try:
        predictions = predict_image(image_bytes, model)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return 'Prediction API is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)

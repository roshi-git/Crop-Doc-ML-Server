from flask import Flask, request, jsonify
from diseases_predictor import DiseasePredictor


app = Flask(__name__)

@app.route('/')
def index():
    return "Crop-Doc Disease Prediction and Plotting Server"

@app.route('/predict_disease', methods = ['GET', 'POST'])
def predict_disease():

    if request.method == 'GET':
        return "PREDICTION SERVER"

    if request.method == 'POST':
        image_URL = request.json['image_URL']
        disease_predictor = DiseasePredictor(image_URL)
        result = disease_predictor.predict_disease()

        return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=42069, debug=True, use_reloader=True)
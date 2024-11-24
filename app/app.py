from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import tensorflow as tf
from io import BytesIO

# Get the absolute base directory of the current file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app with absolute static folder path
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
app = Flask(__name__, static_folder=STATIC_FOLDER)

# Load the TensorFlow model using an absolute path
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'my_tomato_model')  # Ensure correct file name and extension
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = load_model(MODEL_PATH)

# Define class labels
class_labels = [
    'Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
    'Septoria_leaf_spot', 'Spider_mites_Two-spotted_spider_mite',
    'Target_Spot', 'Tomato_healthy', 'Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato_mosaic_virus'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction."""
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Convert the uploaded file to a file-like object
        img = load_img(BytesIO(file.read()), target_size=(150, 150))  # Match model input size
        img_array = img_to_array(img) / 255.0
        img_array = tf.expand_dims(img_array, 0)

        # Make prediction
        predictions = model.predict(img_array)
        predicted_index = tf.argmax(predictions[0]).numpy()
        predicted_label = class_labels[predicted_index]

        return jsonify({'class': predicted_label, 'confidence': float(tf.reduce_max(predictions[0]) * 100)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

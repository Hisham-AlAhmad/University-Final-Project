from flask import Flask, render_template, request, send_from_directory, jsonify, Blueprint
from PIL import Image, ImageFilter, ImageEnhance
from werkzeug.utils import secure_filename
# Keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os


app_Model = Blueprint('Model', __name__, url_prefix='/Model',
                      template_folder='templates', static_folder='static')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images/Model_images'

# Model saved with Keras model.save()
MODEL_PATH = './Model/model.h5'

# Load your trained model
model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    # function for processing the input image abd prediction
    # Preprocessing the image
    img = image.load_img(img_path, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    y = np.vstack([x])
    result = model.predict(y, batch_size=1)
    return result


@app_Model.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('model.html')


@app_Model.route('/upload_image', methods=['POST'])
def upload_image():
    img = request.files['image']
    filename = secure_filename(img.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img.save(input_path)
    return jsonify({'filename': filename})


@app_Model.route('/predict', methods=['GET', 'POST'])
def predict():
    data = request.get_json()
    filename = data['filename']
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Make prediction
    prediction = model_predict(path, model)
    print(prediction, type(prediction))

    # Process your result for human
    if prediction[0] < 0.5:
        print("This is a male")
        prediction_class = "Male"
    else:
        print("This is a female")
        prediction_class = "Female"

    # return the result
    return jsonify({'result': prediction_class})


@app_Model.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

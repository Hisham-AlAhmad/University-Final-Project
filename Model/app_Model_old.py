import os
import numpy as np

# Keras
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

# Model saved with Keras model.save()
MODEL_PATH = 'model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
# print('Model loaded. Start serving...')

print('------------------------------------------')
print('Model loaded. Check http://127.0.0.1:5001/')
print('------------------------------------------')


def model_predict(img_path, model):
    # function for processing the input image abd prediction
    # Preprocessing the image
    img = image.load_img(img_path, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    y = np.vstack([x])
    result = model.predict(y, batch_size=1)
    return result


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the file from post request
        file = request.files['file']

        # Save the file to ./uploads
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Make prediction
        preds = model_predict(os.path.join(app.config['UPLOAD_FOLDER'], filename), model)
        print(preds, type(preds))

        # Process your result for human
        if preds[0] > 0.5:
            print("This is a male")
            pred_class = "Male"
        else:
            print("This is a female")
            pred_class = "Female"
        # return the result
        return pred_class
    return None


if __name__ == '__main__':
    app.run(debug=True, port=5001)

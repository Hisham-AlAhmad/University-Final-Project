from flask import Flask, render_template, request, send_from_directory, Blueprint, jsonify
from PIL import Image, ImageFilter, ImageEnhance
from werkzeug.utils import secure_filename
import numpy as np
import os
import cv2

app_Filters = Blueprint('Filters_btn', __name__, url_prefix='/Filters_btn',
                        template_folder='templates', static_folder='static')

app = Flask(__name__)
folder_name = 'Filters_btn'
app.config['UPLOAD_FOLDER'] = './images'
app.config['OUTPUT_FOLDER'] = folder_name + '/uploads/output'


def change_extension(filename):
    """
    Changes the file extension from .jpg to .png.
    Args:
        filename (str): The name of the file with the .jpg extension.
    Returns:
        str: The name of the file with the .png extension.
    """
    if filename.endswith(".jpg"):
        filename = filename[:-4] + ".png"
    elif filename.endswith(".JPG"):
        filename = filename[:-4] + ".png"
    return filename


@app_Filters.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('filters.html')


@app_Filters.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    return jsonify({'filename': filename})


@app_Filters.route('/black_white', methods=['POST'])
def black_white():
    data = request.get_json()
    filename = data['filename']

    # Define the output filename
    output_filename = 'black_white_' + filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        # Load the image
        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Convert the image to grayscale
        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Save the grayscale image
        cv2.imwrite(output_path, bw_image)

    print("output filename :", output_filename)
    return jsonify({'filename': output_filename})


@app_Filters.route('/vivid', methods=['POST'])
def vivid():
    data = request.get_json()
    filename = data['filename']

    # Define the output filename
    output_filename = 'vivid_' + filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    # Check if the file does not exist
    if not os.path.isfile(output_path):
        # Load the image
        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Increase the saturation of the image
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] * 1.5, 0, 255)
        vivid_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

        # Save the grayscale image
        cv2.imwrite(output_path, vivid_img)

    print("output filename :", output_filename)
    return jsonify({'filename': output_filename})


@app_Filters.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app_Filters.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    print("sending the output image back to the client")
    print("get_image :", filename)
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

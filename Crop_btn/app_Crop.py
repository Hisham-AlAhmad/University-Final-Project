from flask import Flask, render_template, request, send_from_directory, jsonify, Blueprint
from PIL import Image
from werkzeug.utils import secure_filename
import os

app_Crop = Blueprint('Crop_btn', __name__, url_prefix='/Crop_btn',
                     template_folder='templates', static_folder='static')

app = Flask(__name__)
folder_name = 'Crop_btn'
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


@app_Crop.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('crop.html')


@app_Crop.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    return jsonify({'filename': filename})


@app_Crop.route('/crop_image', methods=['POST'])
def crop_image():
    # Getting the filename and the coordinates
    data = request.get_json()
    filename = data['filename']
    x1, y1, x2, y2 = data['x1'], data['y1'], data['x2'], data['y2']

    # Opening the image
    image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    cropped_image = image.crop((x1, y1, x2, y2))

    # Saving the image
    cropped_filename = 'cropped_' + filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], cropped_filename)
    cropped_image.save(output_path, 'png')
    return jsonify({'filename': cropped_filename})


@app_Crop.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app_Crop.route('/get_image/<filename>', methods=['GET'])
def get_cropped_image(filename):
    print("sending the output image back to the client")
    print("get_image :", filename)
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

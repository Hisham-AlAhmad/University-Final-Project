from flask import Flask, render_template, request, send_from_directory, Blueprint, jsonify
from PIL import Image, ImageFilter, ImageEnhance
from werkzeug.utils import secure_filename
import os

app_Enhance = Blueprint('Enhance_btn', __name__, url_prefix='/Enhance_btn',
                        template_folder='templates', static_folder='static')

app = Flask(__name__)
folder_name = 'Enhance_btn'
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


@app_Enhance.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('enhance.html')


@app_Enhance.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    return jsonify({'filename': filename})


@app_Enhance.route('/enhance_image', methods=['POST'])
def enhance_image():
    data = request.get_json()
    filename = data['filename']

    # Define the output filename
    output_filename = 'enhanced_' + filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    # Check if the file does not exist
    if not os.path.isfile(output_path):
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Sharpen the image
        image = image.filter(ImageFilter.SHARPEN)  # sharpen by x1
        # Detailing the image
        image = image.filter(ImageFilter.DETAIL)  # detail by x1
        # Smooth the image
        image = image.filter(ImageFilter.SMOOTH)  # smooth by x1

        # Adjust contrast, brightness, saturation
        contrast_factor = 1.3  # Increase contrast by 30%
        brightness_factor = 1.5  # Increase brightness by 50%
        saturation_factor = 1.2  # Increase saturation by 20%
        # Create an ImageEnhance object for the image and enhance it
        enhancer = ImageEnhance.Contrast(image)
        enhancer.enhance(contrast_factor)
        enhancer = ImageEnhance.Brightness(image)
        enhancer.enhance(brightness_factor)
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation_factor)  # This one is for saturation

        # save the image
        image.save(output_path, 'png')

    print("output name:", output_filename)
    return jsonify({'filename': output_filename})


@app_Enhance.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app_Enhance.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    print("sending the output image back to the client")
    print("get_image :", filename)
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

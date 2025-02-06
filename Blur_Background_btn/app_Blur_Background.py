"""
This code takes the image file from the web form (img1),
then remove the background (img2),
then blur the background from 'img1' (img3),
finally combine the person image 'img2' & the blured background 'img3'.
To get the background blured in the image.
And it saves every 'img' in a separate folder
"""
from flask import Flask, render_template, request, send_from_directory, jsonify, Blueprint
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove
from werkzeug.utils import secure_filename
import os

app_Blur_Background = Blueprint('Blur_Background_btn', __name__, url_prefix='/Blur_Background_btn',
                                template_folder='templates', static_folder='static')

app = Flask(__name__)
folder_name = 'Blur_Background_btn'
app.config['UPLOAD_FOLDER'] = './images'
app.config['OUTPUT_FOLDER'] = folder_name + '/uploads/output'
app.config['REMOVED_BACKGROUND_FOLDER'] = folder_name + '/uploads/removedBackground'
app.config['BLURED_FOLDER'] = folder_name + '/uploads/blured'


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


def blur_more(image, amount):
    blured_image = image.filter(ImageFilter.BLUR)
    for i in range(amount):
        x = blured_image
        blured_image = x.filter(ImageFilter.BLUR)
        print(i, end=" ")
    print("Done!!")
    return blured_image


@app_Blur_Background.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('blurBackground.html')


@app_Blur_Background.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)  # original image (img1)
    return jsonify({'filename': filename})


# Blurring Background
@app_Blur_Background.route('/blur', methods=['GET', 'POST'])
def upload_file():
    data = request.get_json()
    blur_amount = int(data['blur_ratio'])
    filename = data['filename']

    # Define the output filename
    output_filename = 'blurBackground_' + str(blur_amount) + "_" + filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        # Remove background (img2)
        input_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        removed_image = remove(input_image)
        enhancer = ImageEnhance.Sharpness(removed_image)
        removed_image = enhancer.enhance(0)
        removed_image.save(os.path.join(app.config['REMOVED_BACKGROUND_FOLDER'], 'background_removed_' + filename), 'png')

        # Blur the original image (img3)
        background_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        enhancer = ImageEnhance.Sharpness(background_image)
        background_image = enhancer.enhance(0)
        blurred_background = blur_more(background_image, blur_amount)  # blurring with the given blur_amount
        blurred_background.save(os.path.join(app.config['BLURED_FOLDER'], 'blurred_background_' + filename), 'png')

        # Combine the original image and the blurred background
        human_cropped = Image.open(
            os.path.join(app.config['REMOVED_BACKGROUND_FOLDER'], 'background_removed_' + filename)).convert('RGBA')
        blurred_background = Image.open(
            os.path.join(app.config['BLURED_FOLDER'], 'blurred_background_' + filename)).convert('RGBA')
        combined_image = Image.alpha_composite(blurred_background, human_cropped)
        # Save the image
        combined_image.save(output_path, 'png')

    print("output name:", output_filename)
    # return send_from_directory('uploads/output/', filename)
    # return send_file('uploads/output/combined_' + str(blur_amount) + "_" + filename)
    return jsonify({'filename': output_filename})


@app_Blur_Background.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app_Blur_Background.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    print("sending the output image back to the client")
    print("get_image :", filename)
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

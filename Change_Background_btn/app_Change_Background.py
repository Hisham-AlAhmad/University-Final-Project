from flask import Flask, render_template, request, send_from_directory, jsonify, Blueprint
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove
from werkzeug.utils import secure_filename
import os

app_Change_Background = Blueprint('Change_Background_btn', __name__, url_prefix='/Change_Background_btn',
                                  template_folder='templates', static_folder='static')
app = Flask(__name__)
folder_name = 'Change_Background_btn'
app.config['REMOVED_BACKGROUND_FOLDER'] = folder_name + '/uploads/removedBackground'
app.config['USER_BACKGROUND_FOLDER'] = folder_name + '/static/user_background'
app.config['BACKGROUND_FOLDER'] = folder_name + '/static/background'
app.config['OUTPUT_FOLDER'] = folder_name + '/uploads/output'
app.config['UPLOAD_FOLDER'] = './images'
# global variables
user_background = ''


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


def enhancing_img(image):
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
    return image


@app_Change_Background.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('changeBackground.html')


@app_Change_Background.route('/user_upload_image', methods=['POST'])
def user_upload_image():
    image = request.files['user_image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)
    print("user_upload_image: ", filename)
    input_path = os.path.join(app.config['USER_BACKGROUND_FOLDER'], filename)
    image.save(input_path)
    return jsonify({'filename': filename})


@app_Change_Background.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)  # original image (img1)
    return jsonify({'filename': filename})


# Changing Background
@app_Change_Background.route('/change_background', methods=['GET', 'POST'])
def change_background():
    data = request.get_json()
    filename = data['filename']
    is_user = data['is_user']  # True if the user uploaded the background image else False
    image_background = data['image_background']
    print("image_background :", image_background)
    if is_user:
        # If the user uploaded the background image
        app_config = app.config['USER_BACKGROUND_FOLDER']
        # image_background = user_background
        print("user_background :", user_background)  # this is the Fucking problem that stopped a whole feature
    else:
        # If the user selected the background image from the provided images
        app_config = app.config['BACKGROUND_FOLDER']

    # Define the output filename
    image_no_extension = image_background.split('.')[0]
    output_filename = 'changedBackground_' + image_no_extension + "_" + filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        # If the file doesn't exist, proceed with the image processing
        # Remove background (img2)
        input_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        removed_image = remove(input_image)
        enhancing_img(removed_image)

        # getting the background to be changed
        changed_background = Image.open(os.path.join(app_config, image_background))
        # Resize the removed_image to the same size as changed_background
        removed_image = removed_image.resize(changed_background.size)

        # Save the new image with new size
        removed_bg_path = os.path.join(app.config['REMOVED_BACKGROUND_FOLDER'], 'background_removed_' + filename)
        removed_image.save(removed_bg_path, 'png')

        # Combine the cropped human and the new background
        human_cropped = Image.open(
            os.path.join(app.config['REMOVED_BACKGROUND_FOLDER'], 'background_removed_' + filename)).convert('RGBA')
        changed_background = Image.open(
            os.path.join(app_config, image_background)).convert('RGBA')
        combined_image = Image.alpha_composite(changed_background, human_cropped)

        # Save the image
        combined_image.save(output_path, 'png')

    print("output name:", output_filename)
    return jsonify({'filename': output_filename})


@app_Change_Background.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client:")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app_Change_Background.route('/get_user_background/<filename>', methods=['GET'])
def get_user_background(filename):
    print("get_user_background :", filename)
    global user_background
    user_background = filename
    return send_from_directory(app.config['USER_BACKGROUND_FOLDER'], filename)


@app_Change_Background.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    print("sending the output image back to the client:")
    print("get_image :", filename)
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

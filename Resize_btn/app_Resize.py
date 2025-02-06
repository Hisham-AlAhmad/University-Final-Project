from flask import Flask, render_template, request, send_from_directory, Blueprint, jsonify
from PIL import Image, ImageFilter, ImageEnhance
from werkzeug.utils import secure_filename
import os
# from Resize_btn.profile_pic import profile_pic
app_Resize = Blueprint('Resize_btn', __name__, url_prefix='/Resize_btn',
                       template_folder='templates', static_folder='static')

app = Flask(__name__)
folder_name = 'Resize_btn'
app.config['UPLOAD_FOLDER'] = './images'
app.config['PROFILE_PICTURES_FOLDER'] = folder_name + '/uploads/profile_pictures'
app.config['PHONE_WALLPAPER_FOLDER'] = folder_name + '/uploads/phone_wallpaper'
app.config['LAPTOP_WALLPAPER_FOLDER'] = folder_name + '/uploads/laptop_wallpaper'
app.config['RESIZE_BY_X_FOLDER'] = folder_name + '/uploads/resize_by_x'
# global variables
original_name = ''
num = 0


def enhancing_image(image):  # This function is used to enhance the image
    # Sharpen the image
    image = image.filter(ImageFilter.SHARPEN)  # sharpen by x1
    # Detailing the image
    image = image.filter(ImageFilter.DETAIL)  # detail by x1
    # Smooth the image
    image = image.filter(ImageFilter.SMOOTH)  # smooth by x1
    # Adjust contrast and brightness
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


@app_Resize.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('resize.html')


@app_Resize.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filename = change_extension(filename)

    global original_name
    original_name = filename
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(input_path)
    return jsonify({'filename': filename})


# output size : 360x360
@app_Resize.route('/profile_pic', methods=['POST'])
def profile_pic():
    data = request.get_json()
    filename = data['filename']

    # Define the output filename
    output_filename = 'profile_picture_' + filename
    output_path = os.path.join(app.config['PROFILE_PICTURES_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = enhancing_image(img)
        # Calculate the new dimensions while maintaining the aspect ratio
        width, height = img.size
        new_width = 360
        new_height = int(new_width * height / width)
        # Resize the image
        img = img.resize((new_width, new_height))
        # Calculate the crop box
        left = (new_width - 360) // 2
        top = (new_height - 360) // 2
        right = (new_width + 360) // 2
        bottom = (new_height + 360) // 2
        # Crop the image to a 360x360 square
        img = img.crop((left, top, right, bottom))
        # Add black padding to the image
        new_img = Image.new('RGB', (360, 360), color='black')
        new_img.paste(img, (0, 0))

        # save the image
        img.save(output_path, 'png')

    print("output filename (profile picture) :", output_filename)
    return jsonify({'filename': output_filename})


# output size : 1080x2400
@app_Resize.route('/phone_wallpaper', methods=['POST'])
def phone_wallpaper():
    data = request.get_json()
    filename = data['filename']

    # Define the output filename
    output_filename = 'phone_wallpaper_' + filename
    output_path = os.path.join(app.config['PHONE_WALLPAPER_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = enhancing_image(image)
        # Calculate the new dimensions while maintaining the aspect ratio
        width, height = image.size
        new_width = 1080
        new_height = int(new_width * height / width)
        # Resize the image
        image = image.resize((new_width, new_height))
        # Calculate the crop box
        left = (new_width - 1080) // 2
        top = (new_height - 2400) // 2
        right = (new_width + 1080) // 2
        bottom = (new_height + 2400) // 2
        # Crop the image to a 1080x2400 rectangle
        image = image.crop((left, top, right, bottom))
        # Add black padding to the image
        new_img = Image.new('RGB', (1080, 2400), color='black')
        y = (2400 - new_height) // 2
        # Paste the cropped image onto the new black image
        new_img.paste(image, (0, y))

        # save the image
        image.save(output_path, 'png')

    print("output filename (phone wallpaper):", output_filename)
    return jsonify({'filename': output_filename})


# output size : 1920x1080
@app_Resize.route('/laptop_wallpaper', methods=['POST'])
def laptop_wallpaper():
    data = request.get_json()
    filename = data['filename']

    # Define the output filename
    output_filename = 'laptop_wallpaper_' + filename
    output_path = os.path.join(app.config['LAPTOP_WALLPAPER_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = enhancing_image(image)
        # Calculate the new dimensions while maintaining the aspect ratio
        width, height = image.size
        new_width = 1920
        new_height = int(new_width * height / width)
        # Resize the image
        image = image.resize((new_width, new_height))
        # Calculate the crop box
        left = (new_width - 1920) // 2
        top = (new_height - 1080) // 2
        right = (new_width + 1920) // 2
        bottom = (new_height + 1080) // 2
        # Crop the image to a 1920x1080 rectangle
        image = image.crop((left, top, right, bottom))
        # Add black padding to the image
        new_img = Image.new('RGB', (1920, 1080), color='black')
        y = (1080 - new_height) // 2
        # Paste the cropped image onto the new black image
        new_img.paste(image, (0, y))

        # save the image
        image.save(output_path, 'png')

    print("output filename (laptop wallpaper) :", output_filename)
    return jsonify({'filename': output_filename})


# custom size : num x num
@app_Resize.route('/resize_by_x', methods=['POST'])
def resize_by_x():
    data = request.get_json()
    global num
    num = int(data['number'])
    filename = data['filename']

    # Define the output filename
    output_filename = 'resized_by_' + str(num) + '_' + filename
    output_path = os.path.join(app.config['RESIZE_BY_X_FOLDER'], output_filename)

    # Check if the file does not exist
    if not os.path.isfile(output_path):
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = enhancing_image(image)
        # Calculate the new dimensions while maintaining the aspect ratio
        width, height = image.size
        new_width = width * num
        new_height = height * num
        # Resize the image
        image = image.resize((new_width, new_height))

        # Save the resized image
        image.save(output_path, 'png')

    print("output filename (resize by x) :", output_filename)
    return jsonify({'filename': output_filename})


@app_Resize.route('/get_original_image/<filename>', methods=['GET'])
def get_original_image(filename):
    print("sending the original image back to the client")
    print("get_original_image :", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def file_path(filename):
    global original_name
    if filename == 'profile_picture_' + original_name:
        return app.config['PROFILE_PICTURES_FOLDER']
    elif filename == 'phone_wallpaper_' + original_name:
        return app.config['PHONE_WALLPAPER_FOLDER']
    elif filename == 'laptop_wallpaper_' + original_name:
        return app.config['LAPTOP_WALLPAPER_FOLDER']
    elif filename == 'resized_by_' + str(num) + '_' + original_name:
        return app.config['RESIZE_BY_X_FOLDER']
    else:
        return app.config['UPLOAD_FOLDER']  # scenario where the filename is not found


@app_Resize.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    print("sending the output image back to the client")
    print("get_image :", filename)
    print("original_name :", original_name)
    path = file_path(filename)
    return send_from_directory(path, filename)


if __name__ == '__main__':
    app.run(debug=True)

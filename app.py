from flask import Flask, render_template, redirect
from Change_Background_btn.app_Change_Background import app_Change_Background
from Blur_Background_btn.app_Blur_Background import app_Blur_Background
from Blur_Humans_btn.app_Blur_Humans import app_Blur_Humans
from Enhance_btn.app_Enhance import app_Enhance
from Filters_btn.app_Filters import app_Filters
from Resize_btn.app_Resize import app_Resize
from Crop_btn.app_Crop import app_Crop
from Model.app_Model import app_Model

app = Flask(__name__)

# Blueprints
app.register_blueprint(app_Change_Background, url_prefix='/Change_Background_btn',
                       template_folder='Change_Background_btn/templates', static_folder='Change_Background_btn/static')
app.register_blueprint(app_Blur_Background, url_prefix='/Blur_Background_btn',
                       template_folder='Blur_Background_btn/templates', static_folder='Blur_Background_btn/static')
app.register_blueprint(app_Blur_Humans, url_prefix='/Blur_Humans_btn',
                       template_folder='Blur_Humans_btn/templates', static_folder='Blur_Humans_btn/static')
app.register_blueprint(app_Enhance, url_prefix='/Enhance_btn',
                       template_folder='Enhance_btn/templates', static_folder='Enhance_btn/static')
app.register_blueprint(app_Filters, url_prefix='/Filters_btn',
                       template_folder='Filters_btn/templates', static_folder='Filters_btn/static')
app.register_blueprint(app_Resize, url_prefix='/Resize_btn',
                       template_folder='Resize_btn/templates', static_folder='Resize_btn/static')
app.register_blueprint(app_Crop, url_prefix='/Crop_btn',
                       template_folder='Crop_btn/templates', static_folder='Crop_btn/static')
app.register_blueprint(app_Model, url_prefix='/Model',
                       template_folder='Model/templates', static_folder='Model/static')


# index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# old main page
@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


# about page
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# edit page
@app.route('/edit', methods=['GET'])
def edit():
    return render_template('edit.html')


# services page
@app.route('/services', methods=['GET'])
def services():
    return render_template('services.html')


# team page
@app.route('/team', methods=['GET'])
def team():
    return render_template('team.html')


# projects page
@app.route('/projects', methods=['GET'])
def projects():
    return render_template('projects.html')


# instagram page
@app.route('/instagram', methods=['GET'])
def instagram():
    return redirect('https://www.instagram.com')


if __name__ == '__main__':
    app.run(debug=True)

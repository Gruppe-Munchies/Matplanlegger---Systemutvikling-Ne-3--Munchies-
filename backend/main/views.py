from flask import Blueprint, render_template

routes = Blueprint('mainpage', __name__, static_folder="static", template_folder="templates")

@routes.route('/')
def index():
    return "Test"
    #return render_template('index.html')


from flask import Blueprint, render_template

mainpage = Blueprint('mainpage', __name__, static_folder="static", template_folder="templates")

@mainpage.route('/')
def index():
    return "Test"
    #return render_template('index.html')


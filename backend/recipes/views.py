from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import backend.recipes.queries as ingr_queries
import backend.recipes.queries as recipes
from backend import recipes

#from backend.recipes.forms import RegisterForm
#from backend.recipes.queries import *

#recipes = Blueprint('recipes', __name__, template_folder='templates', url_prefix='/oppskrift')
recipes = Blueprint('recipes', __name__, template_folder='templates')

@recipes.route('/oppskrifter')
def oppskrifter():

    recipes = ingr_queries.fetch_all_recipes()

    return render_template('oppskrifter.html', recipes=recipes)


@recipes.route('/oppskrift')
def oppskrift():
    recipes = ingr_queries.fetch_all_recipes()

    return render_template('oppskrift.html', recipes=recipes)





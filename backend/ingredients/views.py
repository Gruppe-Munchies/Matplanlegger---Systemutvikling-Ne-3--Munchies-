from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

import local_db.insert_to_db as db

from backend.ingredients.forms import RegisterForm

ingredient = Blueprint('ingredient', __name__, template_folder='templates', url_prefix='/ingredient')


@ingredient.route('/new', methods=['GET', 'POST'])
def new():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        ingreientName = form.ingredientname.data #TODO Check if ingredient already exists
        usergroup = form.usergroup.data
        ingredientID = form.ingredientID.data #TODO Fetch ingredientID from new or existing
        price = form.price.data
        unit = form.unit.data

        db.insert_to_ingredients(ingreientName)
        db.insert_to_usergroup_has_ingredient(usergroup, ingredientID, price, unit)

        flash('Ingrediensen er registrert!!')
        return redirect(url_for("ingredient.new"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('newingredient.html', form=form)

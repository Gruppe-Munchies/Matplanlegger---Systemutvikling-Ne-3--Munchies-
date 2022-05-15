import flask
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

import backend.auth.queries as auth_queries
import backend.ingredients.queries as ingr_queries
from backend.ingredients.forms import RegisterForm
from backend.ingredients.queries import *

ingredient = Blueprint('ingredient', __name__, template_folder='templates', url_prefix='/ingredient')


@ingredient.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    group_to_use = flask.session.get('group_to_use')

    group_ingredients = fetch_all_ingredients_where_usergroup_equals(flask.session.get('group_to_use'))
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        ingredientName = form.ingredientName.data

        usergroup = auth_queries.fetchUserGroupById(group_to_use).groupName  # form.usergroup.data var det før
        price = form.price.data
        unit = form.unit.data

        check_ingredient = ingr_queries.fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(
            ingredientName)

        fetchedusergroup = auth_queries.fetchUserGroup(usergroup)
        fetchedusergroup_ID = fetchedusergroup.iduserGroup
        check_ingredient_in_userGroup = fetch_ingredients_where_usergroup_and_ingredientName_equals(group_to_use,
                                                                                                    ingredientName)
        if check_ingredient_in_userGroup:
            flash("Ingrediens er allerede registrert i din gruppe", "danger")

        elif check_ingredient:

            fetchedingredientID = ingr_queries.fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(
                ingredientName)
            ingredientID = fetchedingredientID.idingredient

            ingr_queries.insert_to_usergroup_has_ingredient(fetchedusergroup_ID, ingredientID, price, unit)
            flash('Ingrediensen er registrert!!', "success")

        else:
            ingr_queries.insert_to_ingredients(ingredientName)
            fetchedingredientID = ingr_queries.fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(
                ingredientName)
            ingredientID = fetchedingredientID.idingredient

            ingr_queries.insert_to_usergroup_has_ingredient(fetchedusergroup_ID, ingredientID, price, unit)
            flash('Ingrediensen er registrert!!', "success")


        return redirect(url_for("ingredient.new"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('newingredient.html', form=form, ingredients=group_ingredients)


@ingredient.route('/<ingrediens_id>/<quantity>/<price>/update', methods=["GET", "POST"])
def updateIngredient(ingrediens_id: str, quantity: str, price: str):
    group = flask.session.get('group_to_use')
    editIngredient(group, ingrediens_id, quantity, price)
    return redirect('/ingredient/new')

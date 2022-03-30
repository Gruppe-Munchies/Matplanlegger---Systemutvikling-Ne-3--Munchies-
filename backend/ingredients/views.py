from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import flask
from flask_login import login_required, login_user, logout_user

import backend.ingredients.queries as ingr_queries
import backend.auth.queries as auth_queries

from backend.ingredients.forms import RegisterForm
from backend.ingredients.queries import *


ingredient = Blueprint('ingredient', __name__, template_folder='templates', url_prefix='/ingredient')


@ingredient.route('/new', methods=['GET', 'POST'])
@login_required
#     ingredienser = fetch_all_ingredients_where_usergroup_equals(1)
#     for ap in ingredienser:
#         print(f"{ap[0].ingredientName} {round(ap[1].quantity, 2)} {ap[1].unit} {round(ap[1].price, 2)}")
def new():
    print(flask.session.get('group_to_use'))
    group_ingredients = fetch_all_ingredients_where_usergroup_equals(1)

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        ingredientName = form.ingredientName.data
        usergroup = form.usergroup.data
        price = form.price.data
        unit = form.unit.data

        check_ingredient = ingr_queries.fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(
            ingredientName)

        fetchedusergroup = auth_queries.fetchUserGroup(usergroup)  # TODO bør være en dropdown der brukeren kan velge
        fetchedusergroup_ID = fetchedusergroup.iduserGroup

        check_ingredient_in_userGroup = fetch_ingredients_where_usergroup_and_ingredientName_equals(1,
                                                                                                    ingredientName)  # First input: usergroupID

        if check_ingredient_in_userGroup:
            flash("Ingrediens er allerede registrert", "danger")
            if check_ingredient:
                    flash("Ingrediens er allerede registrert i din gruppe", "danger")
            else:
                # legg til ingrediens i Usergroup, ikke ingrediens
                fetchedingredientID = ingr_queries.fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(
                    ingredientName)  # TODO Fetch ingredientID from new or existing
                ingredientID = fetchedingredientID.idingredient

                ingr_queries.insert_to_usergroup_has_ingredient(fetchedusergroup_ID, ingredientID, price, unit)
                ingr_queries.insert_to_ingredients(ingredientName)
                flash('Ingrediensen er registrert!!')

                # return render_template('newingredient.html', form=form,
                                       # heading="Registrer ny ingrediens")  # vet ikke om heading trengs?
        else:
            ingr_queries.insert_to_ingredients(ingredientName)
            fetchedingredientID = ingr_queries.fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(
                ingredientName)  # TODO Fetch ingredientID from new or existing
            ingredientID = fetchedingredientID.idingredient

            ingr_queries.insert_to_usergroup_has_ingredient(fetchedusergroup_ID, ingredientID, price, unit)
            flash('Ingrediensen er registrert!!')

            # TODO Render with new ingredient

        return redirect(url_for("ingredient.new"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('newingredient.html', form=form, ingredients=group_ingredients)

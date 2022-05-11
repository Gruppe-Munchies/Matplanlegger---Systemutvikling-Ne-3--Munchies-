from flask import Blueprint, render_template, session, request, redirect, url_for
from backend.reports.queries import *
import pandas as pd
from flask_alchemy_db_creation.local_db_create import engine
from flask_login import login_required

reports = Blueprint('reports', __name__, template_folder='templates')


def test():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    res2 = pd.read_sql(ingredients_used_per_week_total(3, 2022, 19).statement, engine)
    print(res2[['Ukemeny', 'Gruppe', 'Ingrediens', 'SumMengde', 'Enhet', 'SumBelop']])

    print("")
    print("")

    res = pd.read_sql(ingredients_used_per_week_per_dish(3, 2022, 19, 4).statement, engine)
    print(res[['Ukemeny', 'Gruppe', 'Oppskrift', 'Ingrediens', 'Mengde', 'Prognose', 'SumMengde', 'Enhet']])

    print("")
    print("")

    res3 = pd.read_sql(fetch_weekly_menus_for_group(3).statement, engine)
    print(res3)


if __name__ == '__main__':
    test()


@reports.route('/rapporter', methods=['GET', 'POST'])
@login_required
def ingredients_used_per_week():
    groupId = session.get('group_to_use')
    menuId = session.get('menuId')

    if 'menu' in request.args:
        session['menuId'] = request.args["menu"]
        menuId = session.get('menuId')

    totalcost = 0
    recipes = []
    perRecipe = False

    menus = fetch_weekly_menus_for_group(groupId)

    # If recipe specification
    if 'recipe' in request.args:
        recipeId = request.args["recipe"]
        res = ingredients_used_per_week_per_dish(menuId, recipeId, groupId)
        perRecipe = True

    # Else if menu selected
    elif 'menu' in request.args:
        res = ingredients_used_per_week_total(menuId, groupId)

    else:
        res = ingredients_used_per_week_total(0, groupId)

    if 'weeknum' in request.args:
        recipes = fetch_recipes_in_weekly_menu(menuId)
        for i in res:
            totalcost += i.SumBelop

    return render_template('report.html', report=res, menus=menus, recipes=recipes, totalcost=totalcost,
                           perRecipe=perRecipe)

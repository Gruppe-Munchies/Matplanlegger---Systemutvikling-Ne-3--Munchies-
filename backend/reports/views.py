from flask import Blueprint, render_template, session, request, redirect, url_for
from backend.reports.queries import *
import pandas as pd
from flask_alchemy_db_creation.local_db_create import engine
from flask_login import login_required

reports = Blueprint('reports', __name__, template_folder='templates')

def test():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    res2 = pd.read_sql(ingredients_used_per_week_total(1,2022,16).statement, engine)
    print(res2[['Ukemeny','Gruppe', 'Ingrediens', 'SumMengde', 'Enhet', 'SumBelop']])

    print("")
    print("")

    res = pd.read_sql(ingredients_used_per_week_per_dish(1,2022,16,2).statement, engine)
    print(res[['Ukemeny','Gruppe', 'Oppskrift', 'Ingrediens', 'Mengde', 'Prognose', 'SumMengde', 'Enhet']])

    print("")
    print("")

    res3 = pd.read_sql(fetch_weekly_menus_for_group(1).statement, engine)
    print(res3)

if __name__ == '__main__':
    test()


@reports.route('/rapporter', methods=['GET', 'POST'])
@login_required
def ingredients_used_per_week():

    groupId = session.get('group_to_use')

    weeknum = 0
    year = 0
    recipes = []

    menus = fetch_weekly_menus_for_group(groupId)

    # If recipe specification
    if 'recipe' in request.args:
        weeknum = request.args["weeknum"]
        year = request.args["year"]
        recipe = request.args["recipe"]
        res = ingredients_used_per_week_per_dish(groupId, year, weeknum, recipe)

    # Else if menu selected
    elif 'weeknum' in request.args:
        weeknum = request.args["weeknum"]
        year = request.args["year"]
        res = ingredients_used_per_week_total(groupId, year, weeknum)

    else:
        res = ingredients_used_per_week_total(groupId, year, weeknum)
        totalcost = 0

    if 'weeknum' in request.args:
        menu = fetch_menu_id(year, weeknum, groupId)
        for i in menu:
            print(i)
        menuId = menu[0].weeklyMenu_id
        recipes = fetch_recipes_in_weekly_menu(menuId)
        for i in recipes:
            print(i)

        totalcost = 0
        for i in res:
           totalcost += res[0].SumBelop

    return render_template('report.html', report=res, menus=menus, recipes=recipes, totalcost=totalcost)
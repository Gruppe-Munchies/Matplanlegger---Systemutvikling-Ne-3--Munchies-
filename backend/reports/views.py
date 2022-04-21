from flask import Blueprint, render_template, session, request, redirect, url_for
from backend.reports.queries import *
import pandas as pd
from flask_alchemy_db_creation.local_db_create import engine

reports = Blueprint('reports', __name__, template_folder='templates')

def test():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    res = pd.read_sql(ingredients_used_per_week_per_dish(1,2022,16).statement, engine)
    print(res[['Ukemeny','Gruppe', 'Oppskrift','Prognose', 'Ingrediens', 'Mengde', 'SumMengde', 'Enhet']])

    print("")
    print("")

    res2 = pd.read_sql(ingredients_used_per_week_total(1,2022,16).statement, engine)
    print(res2[['Ukemeny','Gruppe', 'Antall retter', 'Ingrediens', 'SumMengde', 'Enhet', 'SumBelop']])

    print("")
    print("")

    res3 = pd.read_sql(fetch_weekly_menus_for_group(1).statement, engine)
    print(res3)

if __name__ == '__main__':
    test()


@reports.route('/rapporter', methods=['GET', 'POST'])
def ingredients_used_per_week():

    #groupId = session.get('group_to_use')
    groupId = 1
    year = 2022

    if 'weeknum' in request.args:
        weeknum = request.args["weeknum"]
    else:
        weeknum = 0

    res = ingredients_used_per_week_total(groupId, year, weeknum)
    menus = fetch_weekly_menus_for_group(groupId)

    return render_template('report.html', report=res, menus=menus)
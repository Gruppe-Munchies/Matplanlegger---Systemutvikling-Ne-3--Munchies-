from flask import Blueprint, render_template
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


if __name__ == '__main__':
    test()


@reports.route('/report', methods=['GET', 'POST'])
def ingredients_used_per_week():

    groupId = 1
    year = 2022
    weeknum = 16

    res = ingredients_used_per_week_total(groupId, year, weeknum)

    #for i in res:
    #    print(i.Ingrediens)

    return render_template('report.html', report=res)
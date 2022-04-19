from flask import Blueprint
from backend.reports.queries import *

reports = Blueprint('reports', __name__, template_folder='templates')

def test():
    res = ingredients_used_per_week_total(1,2022,16)

    for i in res:
        print(i)

if __name__ == '__main__':
    test()

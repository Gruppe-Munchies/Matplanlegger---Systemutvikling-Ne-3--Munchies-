import flask
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
import backend.weekly_menu.queries as menu_queries
from backend.weekly_menu.forms import RegisterWeeklymenuForm, WeeklyMenuSelector, WeeklyMenuToDateForm, \
    WeeklyMenuWeekSelector

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/ukesmeny', methods=['POST', 'GET'])
def ukesmeny():
    if menu_queries.check_first_weeklymenu_where_groupId(session.get('group_to_use')) != None:
        # if not flask.session.get('menuID'):
        #    session['menuID'] = menu_queries.fetch_first_weeklymenu_where_groupId(session.get('group_to_use'))

        # Basic data collection
        weeklymenu_to_date_form = WeeklyMenuToDateForm(request.form)
        group_id = flask.session.get('group_to_use', 'not set')
        weekly_menus = menu_queries.fetch_all_weeklymenu_where_groupId(session['group_to_use'])
        weekly_menus_with_date = menu_queries.fetch_menus_with_dates_by_group_id(group_id)

        for i in weekly_menus:
            print(i.idWeeklyMenu)
        recipes_weeklymenu = menu_queries.fetch_recipesNameQyantity_where_weeklymenu_id(weekly_menus[0].idWeeklyMenu)

        # hent ut i liste alle recepies i den gitte ukesmenyen.  hardkod ukesmenyen først.
        group_recipes = menu_queries.fetch_recipes_where_usergroupid(flask.session.get('group_to_use'))

        weeklyMenuRecepies = menu_queries.fetch_weeklymenu_recipes_where_name_usergroupid(flask.session.get('menuID'))
        activeMenu = menu_queries.fetch_weeklymenu_where_usergroupid(flask.session.get('group_to_use'))
        dishes = [i.name for i in weeklyMenuRecepies]

        form = RegisterWeeklymenuForm(request.form)
        formSelector = WeeklyMenuSelector(request.form)
        choice = []

        for i in weekly_menus:
            choice.append((i.idWeeklyMenu, i.name))
        for i in choice:
            if i[0] == int(flask.session.get('menuID')):
                choice.remove(i)
                choice.insert(0, i)


        formSelector.weeklyIdName.choices = choice

        if request.method == 'POST':
            # HENT DATA FRA MENY UKE-FORM
            if formSelector.weeklyIdName.data is not None:
                session['menuID'] = formSelector.weeklyIdName.data
                formSelector.weeklyIdName.data = session['menuID']
                return redirect(request.referrer)

            # HENT DATA FRA KNYTT-TIL-UKE-FORM
            if weeklymenu_to_date_form.week.data is not None and weeklymenu_to_date_form.year is not None:
                week = weeklymenu_to_date_form.week.data
                year = weeklymenu_to_date_form.year.data
                menu_queries.insert_to_weekly_menu_date(session['menuID'], week, year)
                flash(f"Meny knyttet til uke {week}!", "success")
                return redirect(request.referrer)

            if form.weekly_name.data is not None:
                weeklymanu_name = form.weekly_name.data
                weeklymenu_desc = form.weekly_desc.data

                # Do group already have menu with same name?
                if not menu_queries.fetch_weeklymenu_where_name_and_usergroupid(group_id, weeklymanu_name):

                    menu_queries.insert_to_weeklymenu(weeklymanu_name, weeklymenu_desc, group_id)

                    # TODO: Legg til oppskrifter ---RECIPES

                    flash("Meny lagt til!", "success")
                    return redirect(url_for("weeklyMenu.ukesmeny"))
                else:
                    flash("Dere har allerede en meny med dette navnet", "warning")

        weeklyMenuRecepies = menu_queries.fetch_weeklymenu_recipes_where_name_usergroupid(flask.session.get('menuID'))
        weeklyMenus = menu_queries.fetch_menus_with_dates_by_group_id(group_id)
        selectedMenuName = menu_queries.fetch_menu_name_where_menu_id(session['menuID'])

        return render_template('ukesmeny.html', selectedMenuName=selectedMenuName,
                               weeklymenu_to_date_form=weeklymenu_to_date_form, recipes=group_recipes,
                               weeklyMenusWithDate=weekly_menus_with_date,
                               weeklyMenuRecepies=weeklyMenuRecepies,
                               activeMenu=activeMenu,
                               dishes=dishes, form=form, formSelect=formSelector, menuID=flask.session.get('menuID'))
    else:
        return redirect('/legg_til_ukesmeny')

@weeklyMenu.route('/legg_til_ukesmeny', methods=['POST', 'GET'])
def legg_til_ukesmeny():
    form = RegisterWeeklymenuForm(request.form)

    if request.method == 'POST':
        weeklymanu_name = form.weekly_name.data
        weeklymenu_desc = form.weekly_desc.data

        # Do group already have menu with same name?
        if not menu_queries.fetch_weeklymenu_where_name_and_usergroupid(flask.session.get('group_to_use'),
                                                                        weeklymanu_name):

            menu_queries.insert_to_weeklymenu(weeklymanu_name, weeklymenu_desc, flask.session.get('group_to_use'))

            # TODO: Legg til oppskrifter ---RECIPES

            flash("Meny lagt til!", "success")
            return redirect(url_for("index"))
        else:
            flash("Dere har allerede en meny med dette navnet", "warning")

    return render_template('newWeeklyMenu.html', form=form)


@weeklyMenu.route('/weekly_menu/<array>/update', methods=["GET", "POST"])
def updateRecipeHasIngrediens(array: str):
    return redirect(url_for("recipes.oppskrifter"))


@weeklyMenu.route('/weekly_menu/<recipe_id>/<quantity>/add', methods=["GET", "POST"])
def addRecipeToWeeklyMenu(recipe_id: int, quantity: int):
    menuID = flask.session.get('menuID')
    menu_queries.insert_to_recipe_has_weeklymenu(menuID, recipe_id, quantity)
    return redirect('/ukesmeny')


@weeklyMenu.route('/weekly_menu/<recipe_id>/<menu_ID>/delete', methods=["GET", "POST"])
def RemoveRecipeFromWeeklyMenu(recipe_id: int, menu_ID: int):
    menu_queries.remove_from_RecipeHasWeeklyMenu(recipe_id, menu_ID)
    return redirect('/ukesmeny')


@weeklyMenu.route('/handleliste', methods=["GET", "POST"])
def handleliste():
    # TODO: Instead of weekly menus it should show weekly menus that are sat to a week
    weekly_menu_w_dates = menu_queries.fetch_all_weeklymenu_where_groupId(session['group_to_use'])

    formSelector = WeeklyMenuWeekSelector(request.form)
    choice = []
    form = RegisterWeeklymenuForm(request.form)

    for i in weekly_menu_w_dates:
        choice.append((i.idWeeklyMenu, i.name))
    for i in choice:
        if i[0] == int(flask.session.get('menuID')):
            choice.remove(i)
            choice.insert(0, i)

    formSelector.weeklyMenuWeekId.choices = choice
    # id = formSelector.weeklyMenuWeekId
    # print(id.data)

    if request.method == 'POST':
        print("1")
        if formSelector.weeklyMenuWeekId.data is not None:
            print("2")
            session['menuID'] = formSelector.weeklyMenuWeekId.data
            formSelector.weeklyMenuWeekId.data = session['menuID']
            print(formSelector.data)

            return redirect(request.referrer)
        # TODO: number passed in to method ikke hardkoda
    allIngredientsFromWeekly = menu_queries.get_all_ingredients_and_quantities_cost_etc_shopping_in_weeklymenu(session['menuID'])
    totalsum = 0
    for ingredient in allIngredientsFromWeekly:
        totalsum += ingredient[4]
    weekly_menu_name = "***"

    return render_template('handleliste.html', weekly_menu_name=weekly_menu_name, form=form, totalsum=totalsum,
                           ingredients=allIngredientsFromWeekly, formSelect=formSelector)


@weeklyMenu.route('/<ingrediens_id>/<quantity>/update', methods=["GET", "POST"])
def updateIngredient(ingrediens_id: str, quantity: str):
    group = flask.session.get('group_to_use')
    menu_queries.editIngredientShopping(group, ingrediens_id, quantity)
    return redirect('/handleliste')

# import local_db.insert_to_db as db
import backend.ingredients.queries as ingredient_queries
import backend.recipies.queries as recipe_queries
import backend.auth.queries as auth_queries
import backend.weekly_menu.queries as menu_queries

def test_data():
    #Default values
    auth_queries.insert_to_usertype()
    recipe_queries.insert_to_recipeavalilability()

    #Add some ingredients
    ingredient_queries.insert_to_ingredients("Agurk")
    ingredient_queries.insert_to_ingredients("Tomat")
    ingredient_queries.insert_to_ingredients("Egg")
    ingredient_queries.insert_to_ingredients("Mel")
    ingredient_queries.insert_to_ingredients("Fløte")

    #Add to a usergroup
    auth_queries.insert_to_usergroup("MatMons")
    auth_queries.insert_to_usergroup("Familien Hansen")

    #Add users
    auth_queries.insert_to_user("Bob", "bob@burger.no", "Bob", "Bobsen", "passord")
    auth_queries.insert_to_user("testebruker", "test@test.no", "Test", "Bruker", "hemmeligegreier")

    #Add to user has user_group
    auth_queries.insert_to_user_has_userGroup("1", "1", "1")
    auth_queries.insert_to_user_has_userGroup("2", "2", "1")

    #Add to weeklyMenu
    menu_queries.insert_to_weeklymenu("2022", "9", "1", "Rulleuke", "En uke full av ruller", "1")

    #Add recipe
    recipe_queries.insert_to_recipe("Vårruller", "Digge ruller", "Ikke så mye å skrive her", "test", "1", "1", "1")

    #Add to recipe has ingredient
    recipe_queries.insert_to_recipe_has_ingredient("1", "1", "2.00") #Should be 2 agurker for vårruller
    recipe_queries.insert_to_recipe_has_ingredient("1", "3", "4.00") #Should be 4 egg for vårruller
    recipe_queries.insert_to_recipe_has_ingredient("1", "4", "1.00") #Should be 1 mel for vårruller

    #Add tp recipe has weekly menu
    recipe_queries.insert_to_recipe_has_weeklymenu("1", "2022", "9", "20", "50")

    #Add to usergrup has ingredient
    auth_queries.insert_to_usergroup_has_ingredient("1", "1", "15", "stk" )
    auth_queries.insert_to_usergroup_has_ingredient("1", "4", "30", "kg")



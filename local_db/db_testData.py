import local_db.insert_to_db as db

def test_data():
    #Default values
    db.insert_to_usertype()
    db.insert_to_recipeavalilability()

    #Add some ingredients
    db.insert_to_ingredients("Agurk")
    db.insert_to_ingredients("Tomat")
    db.insert_to_ingredients("Egg")
    db.insert_to_ingredients("Mel")
    db.insert_to_ingredients("Fløte")

    #Add to a usergroup
    db.insert_to_usergroup("MatMons")
    db.insert_to_usergroup("Familien Hansen")

    #Add users
    db.insert_to_user("Bob", "bob@burger.no", "Bob", "Bobsen", "passord")
    db.insert_to_user("testebruker", "test@test.no", "Test", "Bruker", "hemmeligegreier")

    #Add to user has user_group
    db.insert_to_user_has_userGroup("1", "1", "1")
    db.insert_to_user_has_userGroup("2", "2", "1")

    #Add to weeklyMenu
    db.insert_to_weeklymenu("2022", "9", "1", "Rulleuke", "En uke full av ruller", "1")

    #Add recipe
    db.insert_to_recipe("Vårruller", "Digge ruller", "Ikke så mye å skrive her", "test", "1", "1", "1")

    #Add to recipe has ingredient
    db.insert_to_recipe_has_ingredient("1", "1", "2.00") #Should be 2 agurker for vårruller
    db.insert_to_recipe_has_ingredient("1", "3", "4.00") #Should be 4 egg for vårruller
    db.insert_to_recipe_has_ingredient("1", "4", "1.00") #Should be 1 mel for vårruller

    #Add tp recipe has weekly menu
    db.insert_to_recipe_has_weeklymenu("1", "2022", "9", "20", "50")

    #Add to usergrup has ingredient
    db.insert_to_usergroup_has_ingredient("1", "1", "15", "stk" )
    db.insert_to_usergroup_has_ingredient("1", "4", "30", "kg")



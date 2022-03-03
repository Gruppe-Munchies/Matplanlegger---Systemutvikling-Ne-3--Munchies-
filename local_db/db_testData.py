import local_db.test_queries as db

def test_data():
    #Default values
    db.insert_to_usergroup()
    db.insert_to_usertype()
    db.insert_to_recipeavalilability()

    #Add some ingredients
    db.insert_to_ingredients("Agurk")
    db.insert_to_ingredients("Tomat")
    db.insert_to_ingredients("Egg")
    db.insert_to_ingredients("Mel")
    db.insert_to_ingredients("Fløte")

    #Add users
    db.insert_to_user("jebisseh", "bisseth@online.no", "Jan Erik", "Bisseth", "passord", "1", "1")
    db.insert_to_user("testebruker", "test@test.no", "Test", "Bruker", "hemmeligegreier", "2", "2")

    #Add to weeklyMenu
    db.insert_to_weeklymenu("9", "1", "Rulleuke", "Em uke full av ruller")

    #Add recipe
    db.insert_to_recipe("Vårruller", "Digge ruller", "Ikke så mye å skrive her", "test", "1", "1", "1")

    #Add to recipe has ingredient
    db.insert_to_recipe_has_ingredient("1", "1", "2") #Should be 2 agurker for vårruller
    db.insert_to_recipe_has_ingredient("1", "3", "4") #Should be 4 egg for vårruller
    db.insert_to_recipe_has_ingredient("1", "4", "1") #Should be 1 mel for vårruller

    #Add tp recipe has weekly menu
    db.insert_to_recipe_has_weeklymenu("1", "2022", "9", "20", "test")

    #Add to usergrup has ingredient
    db.insert_to_usergroup_has_ingredient("1", "1", "15", "stk" )
    db.insert_to_usergroup_has_ingredient("1", "4", "30", "kg")



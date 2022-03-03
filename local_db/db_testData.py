import local_db.test_queries

def test_data():
    #Default values
    local_db.test_queries.insert_to_usergroup()
    local_db.test_queries.insert_to_usertype()
    local_db.test_queries.insert_to_recipeavalilability()

    #Add some ingredients
    local_db.test_queries.insert_to_ingredients("Agurk")
    local_db.test_queries.insert_to_ingredients("Tomat")
    local_db.test_queries.insert_to_ingredients("Egg")
    local_db.test_queries.insert_to_ingredients("Mel")
    local_db.test_queries.insert_to_ingredients("Fløte")

    #Add users
    local_db.test_queries.insert_to_user("jebisseh", "bisseth@online.no", "Jan Erik", "Bisseth", "passord", "1", "1")
    local_db.test_queries.insert_to_user("testebruker", "test@test.no", "Test", "Bruker", "hemmeligegreier", "2", "2")

    #Add recipe
    local_db.test_queries.insert_to_recipe("Vårruller", "Digge ruller", "Ikke så mye å skrive her", "NULL", "1", "1", "1")

    #Add to weeklyMenu
    local_db.test_queries.insert_to_weeklymenu("9", "1", "Rulleuke", "Em uke full av ruller")

    #Add to recipe has ingredient
    local_db.test_queries.insert_to_recipe_has_ingredient("1", "1", "2") #Should be 2 agurker for vårruller
    local_db.test_queries.insert_to_recipe_has_ingredient("1", "3", "4") #Should be 4 egg for vårruller
    local_db.test_queries.insert_to_recipe_has_ingredient("1", "4", "1") #Should be 1 mel for vårruller

    #Add tp recipe has weekly menu
    local_db.test_queries.insert_to_recipe_has_weeklymenu("1", "2022", "9", "20", "NULL")

    #Add to usergrup has ingredient
    local_db.test_queries.insert_to_usergroup_has_ingredient("1", "1", "15", "stk" )
    local_db.test_queries.insert_to_usergroup_has_ingredient("1", "4", "30", "kg")



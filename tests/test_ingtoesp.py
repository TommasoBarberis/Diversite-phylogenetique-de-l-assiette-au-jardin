from lib.ing_to_esp import db_to_dicto

path = "../data/filtered_scientific_name_db.txt"
def test_db_to_dicto(path):
    assert test_db_to_dicto(path)
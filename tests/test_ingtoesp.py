import lib.ing_to_esp as ite

path = "../data/filtered_scientific_name_db.txt"
def test_add():
    assert isinstance(ite.db_to_dicto(path), dict)
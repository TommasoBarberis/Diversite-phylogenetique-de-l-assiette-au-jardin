import lib.get_dp as gdp
import os


def test_length_root_to_knot():
    file_path = (os.path.dirname(__file__))+"/Tree_test.txt"
    dict_lengths = gdp.length_root_to_knot(file_path)
    f = open(file_path, "r", encoding="utf8")
    tree = f.read()
    tree = tree.replace('[', '').replace(']', '').replace("'", "").replace(';', '')
    tree_length = tree.count(",") + tree.count("(")
    dict_size = len(dict_lengths)
    assert dict_size == tree_length

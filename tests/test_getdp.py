import lib.get_dp as gdp


def test_length_root_to_knot():
    tree = "Tree_test.txt"
    dict_lengths = gdp.length_root_to_knot(tree)
    f = open(tree, "r", encoding="utf8")
    tree = f.read()
    tree = tree.replace('[', '').replace(']', '').replace("'", "").replace(';', '')
    tree_length = tree.count(",") + tree.count("(")
    dict_size = len(dict_lengths)
    assert dict_size == tree_length

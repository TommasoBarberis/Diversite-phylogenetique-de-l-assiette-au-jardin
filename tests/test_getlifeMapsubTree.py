import lib.get_lifeMap_subTree as lm
import urllib


def test_getTaxid():
    species = {'mâche': 'Valerianella locusta', 'genièvre': 'Juniperus communis'}
    species = lm.get_taxid(species)
    assert isinstance(species, list)
    for sp in species:
        assert isinstance(sp, int)
        assert len(str(sp)) == 5


def test_getDriver():
    driver = lm.get_driver()
    assert driver is None

    
def test_buildTree():
    species = {'mâche': 'Valerianella locusta', 'genièvre': 'Juniperus communis'}
    tree = lm.build_tree(species)
    assert isinstance(tree, str)
    assert ";" in tree

import lib.get_lifeMap_subTree as lm
import urllib


def test_getTaxid():
    species = {'mâche': 'Valerianella locusta', 'genièvre': 'Juniperus communis'}
    species = lm.get_taxid(species)
    assert isinstance(species, list)
    for sp in species:
        assert isinstance(sp, int)
        assert len(str(sp)) == 5
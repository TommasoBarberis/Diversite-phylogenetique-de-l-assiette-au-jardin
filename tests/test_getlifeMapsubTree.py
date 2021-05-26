import lib.get_lifeMap_subTree as lm
import urllib


def test_getTaxid():
    species = {'mâche': 'Valerianella locusta', 'genièvre': 'Juniperus communis'}
    species = lm.get_taxid(species)
    assert isinstance(species, list)
    for sp in species:
        assert isinstance(sp, int)
        assert len(str(sp)) == 5


def test_getSubTree():
    species = {'poivre': 'Piper nigrum', "huile d'olive": 'Olea europaea', 'ail': 'Allium sativum', 'oignon': 'Allium cepa'}
    driver = lm.get_subTree(species)
    status_code = urllib.request.urlopen("http://lifemap-ncbi.univ-lyon1.fr/").getcode()
    website_is_up = status_code == 200
    assert website_is_up is True
    driver.close()
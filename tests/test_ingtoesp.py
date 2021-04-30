import lib.ing_to_esp as ite


def test_rechercheGlobale():
    ingredients = {'liqueur': [['liqueur', 'liqueur'], '1.5', ['cl', 'cl']], 'sucre vanillé': [['sucre vanillé', 'sucre vanillé'], '1', ['paquet', 'paquets']], 'levure': [['levure', 'levure'], '0.5', ['paquet', 'paquets']], 'jus de citron': [['jus de citron', 'jus de citron'], '0.5', ['', '']], 'farine': [['farine', 'farine'], '150', ['g', 'g']], 'sucre': [['sucre', 'sucre'], '140', ['g', 'g']], 'oeuf': [['oeuf', 'oeufs'], '3', ['', '']]}
    species = ite.recherche_globale(ingredients)
    assert len(species) == len(ingredients)

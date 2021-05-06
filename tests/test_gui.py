import GUI as gui 


def test_missing_species():
    ingredients = {'lardons': [['lardons', 'lardons'], '1', ['paquet', 'paquets']], 'pomme de terre': [['pomme de terre', 'pommes de terre'], '3', ['', '']], 'brick': [['brick', 'brick'], '8', ['feuille', 'feuilles']], 'raclette': [['raclette', 'raclette'], '1', ['paquet', 'paquets']], 'oignon': [['oignon', 'oignons'], '1', ['', '']]}
    species = {'lardons': 'Sus scrofa domesticus', 'pomme de terre': 'Solanum tuberosum', 'oignon': 'Allium cepa', 'raclette': 'Bos taurus'}
    resultats = gui.missing_species(ingredients, species)
    assert resultats[1] == False


def test_missing_nutrition():
    ingredients = {'lardons': [['lardons', 'lardons'], '1', ['paquet', 'paquets']], 'pomme de terre': [['pomme de terre', 'pommes de terre'], '3', ['', '']], 'brick': [['brick', 'brick'], '8', ['feuille', 'feuilles']], 'raclette': [['raclette', 'raclette'], '1', ['paquet', 'paquets']], 'oignon': [['oignon', 'oignons'], '1', ['', '']]}
    resultats = gui.missing_nutrition(ingredients)
    if resultats[0] == []:
        assert resultats[1] == True
    else:
        assert resultats[1] == False

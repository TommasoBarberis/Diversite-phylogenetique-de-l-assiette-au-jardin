import GUI as gui 


def test_missing_species():
    ingredients = {'lardons': [['lardons', 'lardons'], '1', ['paquet', 'paquets']], 'pomme de terre': [['pomme de terre', 'pommes de terre'], '3', ['', '']], 'brick': [['brick', 'brick'], '8', ['feuille', 'feuilles']], 'raclette': [['raclette', 'raclette'], '1', ['paquet', 'paquets']], 'oignon': [['oignon', 'oignons'], '1', ['', '']]}
    species = {'lardons': 'Sus scrofa domesticus', 'pomme de terre': 'Solanum tuberosum', 'oignon': 'Allium cepa', 'raclette': 'Bos taurus'}
    resultats = gui.missing_species(ingredients, species)
    assert resultats[1] == False


def test_missing_nutrition():
    ingredients = {'sel': [['sel', 'sel'], '', ['', '']], 'poivre': [['poivre', 'poivre'], '', ['', '']], 'jus de citron': [['jus de citron', 'jus de citron'], '', ['', '']], 'aneth': [['aneth', 'aneth'], '', ['', '']], 'pâte feuilletée': [['pâte feuilletée', 'pâtes feuilletées'], '1', ['', '']], 'saumon': [['saumon', 'saumon'], '2', ['pavé', 'pavés']], 'crème fraîche épaisse': [['crème fraîche épaisse', 'crème fraîche épaisse'], '', ['', '']]}
    dict_nut = {'Sel': ['Sel blanc alimentaire, non iodé, non fluoré (marin, ignigène ou gemme)', '0,027', '0', '0', '0'], 'Poivre': ['Poivre noir, poudre', '9', '39,5', '7,5', '13,3'], 'Jus de citron': ['Jus de citron, maison', '91,5', '2,41', '0,24', '0,49'], 'Aneth': ['Aneth, frais', '86', '3,9', '1,1', '3,93'], 'Pâte feuilletée': ['Pâte feuilletée, matière grasse végétale, crue', '29,5', '41,4', '20,4', '5,41'], 'Saumon': ['Saumon, cuit, sans précision (aliment moyen)', '62,6', '0', '12,5', '23'], 'Crème fraîche épaisse': ['Crème anglaise, préemballée', '77,7', '16,7', '2,5', '3,44']}
    resultats = gui.missing_nutrition(ingredients, dict_nut)
    if resultats[0] == []:
        assert resultats[1] == True
    else:
        assert resultats[1] == False

import GUI as gui 
import os


def test_buildTable():
    ingredients = {'vinaigre balsamique': [['vinaigre balsamique', 'vinaigre balsamique'], '', ['', '']], 'miel': [['miel', 'miel'], '3', ['cuillère à soupe', 'cuillères à soupe']], 'camembert': [['camembert', 'camemberts'], '2', ['', '']], 'pain de campagne': [['pain de campagne', 'pains de campagne'], '2', ['', '']], 'mâche': [['mâche', 'mâche'], '2', ['poignée', 'poignées']], 'genièvre': [['genièvre', 'genièvre'], '', ['', '']]}
    species = {'mâche': 'Valerianella locusta', 'genièvre': 'Juniperus communis'}
    dict_nut = {'Vinaigre balsamique': ['Vinaigre balsamique', '70,3', '25,8', '< 0,6', '0,69'], 'Miel': ['Miel', '17,6', '81,7', '0', '0,56'], 'Camembert': ['Camembert, sans précision', '54,8', 'traces', '22,5', '19,5'], 'Mâche': ['Mâche, crue', '93,7', '0,5', '< 0,5', '2']}
    drym = {'vinaigre balsamique': '-', 'miel': '-', 'camembert': '-', 'pain de campagne': '-', 'mâche': '-', 'genièvre': '-'}
    recipe_title = "Camembert rôti au miel"
    var = gui.build_table(ingredients, species, dict_nut, drym, recipe_title)
    assert var is None
    img_path = "assets/figures/" + recipe_title + ".png"
    assert os.path.exists(img_path)
    os.remove(img_path)


def test_urlProcess():
    mainwin = gui.MainWindow()
    recipes_dict = {'https://www.marmiton.org/recettes/recette_camembert-roti-au-miel_45038.aspx': []}
    var = mainwin.url_process(recipes_dict)
    assert var is None

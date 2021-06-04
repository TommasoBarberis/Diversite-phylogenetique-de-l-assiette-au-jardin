import lib.get_dp as gdp


def test_phylogeneticDiversity():
    tree = "((((((((((((((((((((((((((((Bos taurus)Bos)Bovinae)Bovidae)Pecora)Ruminantia)Artiodactyla)Laurasiatheria)Boreoeutheria)Eutheria)Theria)Mammalia,(((((((((((((((Gallus gallus)Gallus)Phasianinae)Phasianidae)Galliformes)Galloanserae)Neognathae)Aves)Coelurosauria)Theropoda)Saurischia)Dinosauria)Archosauria)Archelosauria)Sauria)Sauropsida)Amniota)Tetrapoda)Dipnotetrapodomorpha)Sarcopterygii)Euteleostomi)Teleostomi)Gnathostomata)Vertebrata)Craniata)Chordata)Deuterostomia)Bilateria)Eumetazoa)Metazoa)Opisthokonta,(((((((((((((((((((Prunus domestica)Prunus)Amygdaleae)Amygdaloideae)Rosaceae)Rosales)fabids)rosids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae)Eukaryota);"
    species = {'Mirabelle': 'Prunus domestica', 'Beurre': 'Bos taurus', 'Oeuf': 'Gallus gallus'}

    pd = gdp.phylogenetic_diversity(tree, species)
    assert type(pd) is float
    assert pd != 0


def test_weightedPhylogeneticDiversity():
    tree = "((((((((((((((((((((((((((((Bos taurus)Bos)Bovinae)Bovidae)Pecora)Ruminantia)Artiodactyla)Laurasiatheria)Boreoeutheria)Eutheria)Theria)Mammalia,(((((((((((((((Gallus gallus)Gallus)Phasianinae)Phasianidae)Galliformes)Galloanserae)Neognathae)Aves)Coelurosauria)Theropoda)Saurischia)Dinosauria)Archosauria)Archelosauria)Sauria)Sauropsida)Amniota)Tetrapoda)Dipnotetrapodomorpha)Sarcopterygii)Euteleostomi)Teleostomi)Gnathostomata)Vertebrata)Craniata)Chordata)Deuterostomia)Bilateria)Eumetazoa)Metazoa)Opisthokonta,(((((((((((((((((((Prunus domestica)Prunus)Amygdaleae)Amygdaloideae)Rosaceae)Rosales)fabids)rosids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae)Eukaryota);"
    species = {'Mirabelle': 'Prunus domestica', 'Beurre': 'Bos taurus', 'Oeuf': 'Gallus gallus'}
    dict_sp_drym = {'Prunus domestica': [164.25, 'g'], 'Bos taurus': [42.3, 'g'], 'Gallus gallus': [13.03, 'g']}

    wpd = gdp.weighted_phylogenetic_diversity(tree, species, dict_sp_drym)
    assert type(wpd) is float
    assert wpd != 0 


def test_shannon():
    species = {'Mirabelle': 'Prunus domestica', 'Beurre': 'Bos taurus', 'Oeuf': 'Gallus gallus'}
    dict_sp_drym = {'Prunus domestica': [164.25, 'g'], 'Bos taurus': [42.3, 'g'], 'Gallus gallus': [13.03, 'g']}
    ind = gdp.shannon(species, dict_sp_drym)
    assert isinstance(ind, float)

    species = {}
    ind = gdp.shannon(species, dict_sp_drym)
    assert ind == "NA"

def test_simpson():
    species = {'Mirabelle': 'Prunus domestica', 'Beurre': 'Bos taurus', 'Oeuf': 'Gallus gallus'}
    dict_sp_drym = {'Prunus domestica': [164.25, 'g'], 'Bos taurus': [42.3, 'g'], 'Gallus gallus': [13.03, 'g']}
    ind = gdp.simpson(species, dict_sp_drym)
    assert isinstance(ind, float)

    species = {}
    ind = gdp.simpson(species, dict_sp_drym)
    assert ind == "NA"

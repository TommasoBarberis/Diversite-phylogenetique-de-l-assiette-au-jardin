import lib.get_dp as gdp


def test_phylogeneticDiversity():
    tree = "((((((((((((((((((((((((((((Bos taurus)Bos)Bovinae)Bovidae)Pecora)Ruminantia)Artiodactyla)Laurasiatheria)Boreoeutheria)Eutheria)Theria)Mammalia,(((((((((((((((Gallus gallus)Gallus)Phasianinae)Phasianidae)Galliformes)Galloanserae)Neognathae)Aves)Coelurosauria)Theropoda)Saurischia)Dinosauria)Archosauria)Archelosauria)Sauria)Sauropsida)Amniota)Tetrapoda)Dipnotetrapodomorpha)Sarcopterygii)Euteleostomi)Teleostomi)Gnathostomata)Vertebrata)Craniata)Chordata)Deuterostomia)Bilateria)Eumetazoa)Metazoa)Opisthokonta,(((((((((((((((((((Prunus domestica)Prunus)Amygdaleae)Amygdaloideae)Rosaceae)Rosales)fabids)rosids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae)Eukaryota);"
    species = {'Mirabelle': 'Prunus domestica', 'Beurre': 'Bos taurus', 'Oeuf': 'Gallus gallus'}

    pd = gdp.phylogenetic_diversity(tree, species)
    assert type(pd) is float
    assert pd != 0
import lib.get_dp as gdp
import os


def test_length_root_to_knot():
    tree = "(((((((((((((((Piper nigrum)Piper)Piperaceae)Piperales)Magnoliidae,((((((((((((Anethum graveolens)Anethum)Apieae)apioid superclade)Apioideae)Apiaceae)Apiineae)Apiales)campanulids)asterids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae,(((((((((((((((((((((((Salmo salar)Salmo)Salmoninae)Salmonidae)Salmoniformes)Protacanthopterygii)Euteleosteomorpha)Clupeocephala)Osteoglossocephalai)Teleostei)Neopterygii)Actinopteri)Actinopterygii)Euteleostomi)Teleostomi)Gnathostomata)Vertebrata)Craniata)Chordata)Deuterostomia)Bilateria)Eumetazoa)Metazoa)Opisthokonta)Eukaryota);"
    dict_lengths = gdp.length_root_to_knot(tree)
    tree_length = tree.count(",") + tree.count("(")
    dict_size = len(dict_lengths)
    assert dict_size == tree_length

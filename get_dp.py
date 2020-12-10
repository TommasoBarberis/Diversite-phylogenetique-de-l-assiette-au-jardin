from collections import Counter


def calculation (path):
    """Permet de calculer la diversité phylogénétique d'une recette. Cela est calculée en comptant le nb de branches
    qui constituent le sous-arbre le plus petit possible correspondant aux espèces des ingrédients. Les branches sont
    comptes à partir de l'arbre au format Newick (format texte qui permet la représentation des arbres) en comptant 
    la fréquence de certains caractères, tels que '(' et ')'.
    """
    try:
        f=open(path, "r", encoding="utf8")
        tree=f.read()
        lines=tree.split(",")
        dp=0
        for line in lines:
            if line == lines[-1]:
                frequency=Counter(line)
                nb=frequency['(']
                dp+=nb
            else:
                frequency=Counter(line)
                nb=frequency[')']+1
                dp+=nb
        dp+=1
        f.close()
        return dp
    except:
        pass
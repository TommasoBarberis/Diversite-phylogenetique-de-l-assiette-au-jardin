#import sys
from collections import Counter

def calculation (path):
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

#print(calculation(sys.argv[1]))
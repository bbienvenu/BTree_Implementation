# Implémentation de B-Arbres
Programmation de B-Arbres en python

Cette implémentation est basée sur l'approche utilisée dans le livre :

*Introduction à l'Algorithmique, 2e édition - Cormen, 2004*

Méthodes implémentées : 
- Création d'un arbre
- Recherche
- Insertion
- Suppression
- Affichage

**Recherche :**

On commence à partir de la racine et on compare les valeurs de ses clés avec la valeur qu'on recherche. Si on ne trouve pas la valeur parmi les clés de la racine, on descend dans l'arbre en suivant le bon enfant. On répète l'algorithme jusqu'à ce qu'une feuille ne contenant pas l'élément soit atteinte ou que l'élément soit trouvé.

**Insertion :**

Lorsqu'un élément est inséré dans une feuille qui est pleine, avant de l'insérer, on vérifie en descendant l'arbre si les nœuds précédents sont également complets. Et si oui, ils sont divisés, ce qui garantit que lorsqu'une feuille pleine est atteinte et qu'une division est appliquée sur cette feuille, le nœud parent est capable de recevoir la clé qui sera promue.

**Suppression :**

La suppression d'un élément dans un B-arbre consiste en trois tâches principales : la recherche du nœud où se trouve la clé à supprimer, la suppression de la clé et l'équilibrage de l'arbre si nécessaire. Il faut veiller à ce qu'après la suppression, tous les nœuds respectent les critères d'un B-arbre (notamment le nombre minimum de clés).


## Installations et usage

# Installations

Le script requiert l'installation de la bibliothèque graphviz qui gère l'affichage des B-arbres.
Les détails de l'installation sont expliqués ici https://pypi.org/project/graphviz/

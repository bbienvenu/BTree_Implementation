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

### Installations

Le script requiert l'installation de la bibliothèque graphviz qui gère l'affichage des B-arbres.

Les détails de l'installation sont expliqués ici https://pypi.org/project/graphviz/.


### Usage

IL existe deux modes pour ce projet : un mode "batch" et un mode intéractif.

#### <ins>**Mode batch** :</ins>

Ce mode permet d’exécuter un ensemble d’opérations décrites dans un fichier txt et de produire un fichier txt “*log_batch*” qui permet d’afficher les opérations réalisées (et leur résultat).

Les opérations doivent être notées comme suit :

- a : pour insérer un élément dans l'arbre. On écrira *a20* pour insérer la valeur **20**
- s : pour rechercher une valeur dans l'arbre. On écrira *s20* pour rechercher la valeur **20**
- r : pour supprimer une valeur de l'arbre. On écrira *r20* pour supprimer la valeur **20**

On noterait par exemple la liste d'opérations suivante (dans un fichier .txt) : 

```
3
a1
a3
a7
a10
a11
a13
a14
a13
a15
a18
s11
a16
s12
a19
a24
r19
```

Notez que la première valeur n'est précédée par aucun préfixe ; il s'agit du degré de l'arbre. De plus chaque opération doit être écrite sur une ligne (attention à ne pas mettre d'espace mais uniquement un retour à la ligne après chaque opération). Enfin, le fichier txt contenant les opérations doit être placé dans le même dossier (répertoire) que le script Python.
#### <ins>**Mode intéractif** :</ins> 

Ce mode permet à l’utilisateur d'entrer une opération ou une séquence d’opérations à réaliser. 

Les opérations seront notées comme dans le mode batch, et une séquence d'opérations devra être notée : ```a10 a4 s5 a32 r10 a12 a1 a9```, les opérations étant séparées par des espaces.

Dans ce mode, un fichier “*log_iter*” est produit afin d'afficher les opérations réalisées et leurs résultats.

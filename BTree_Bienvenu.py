# --------------------------------------- Projet Final : Btrees --------------------------------------------------


# Noeud d'un BArbre.
# Attributs : est_feuille (determine si un noeud est une feuille ou non) ; cle (liste des cles d'un noeud) ;
# fils (liste, liste des enfants d'un noeud)

class BTreeNode:
    def __init__(self):
        self.cle = list()
        self.fils = list()
        self.est_feuille = True

    def __str__(self):
        if self.est_feuille:
            return "Noeud feuille avec {0} cles\n\tcles : {1}\n\n".format(len(self.cle), self.cle)
        else:
            return "Noeud interne avec {0} cles, {1} fils\n\tcles : {2}\n\n".format(len(self.cle), len(self.fils),
                                                                                    self.cle, self.fils)

    # Rajouter un enfant a un noeud

    def ajouter_fils(self, nouveau_noeud):
        i = len(self.fils) - 1
        while i >= 0 and self.fils[i].cle[0] > nouveau_noeud.cle[0]:
            i -= 1
        return self.fils[:i + 1] + [nouveau_noeud] + self.fils[i + 1:]

    # Diviser un noeud (non racine)

    def diviser(self, parent):
        nouveau_noeud = BTreeNode()
        indice_milieu = len(self.cle) // 2
        valeur_milieu = self.cle[indice_milieu]
        # On fait remonter la valeur "centrale" dans le noeud parent
        parent.cle.append(valeur_milieu)
        parent.cle.sort()
        # Il ne reste plus qu'a attribuer les cles et les enfants aux bons noeuds
        nouveau_noeud.fils = self.fils[indice_milieu + 1:]
        self.fils = self.fils[:indice_milieu + 1]
        nouveau_noeud.cle = self.cle[indice_milieu + 1:]
        self.cle = self.cle[:indice_milieu]
        # On verifie si le nouveau noeud est une feuille
        if len(nouveau_noeud.fils) > 0:
            nouveau_noeud.est_feuille = False
        # On rajoute le nouveau noeud à la liste des enfants de parent
        parent.fils = parent.ajouter_fils(nouveau_noeud)
        # On recupere les indices des noeuds divises dans la liste des enfants (de parent)
        i, j = parent.fils.index(self), parent.fils.index(nouveau_noeud)
        # On retourne ces trois valeurs pour pouvoir decider ou effectuer la recherche/insertion apres le split
        return valeur_milieu, i, j


class BTree:
    def __init__(self, t):
        self.racine = BTreeNode()
        # t est le degre minimal de l'arbre (t >= 2)
        self.t = t
        if self.t < 2:
            raise ValueError("Un B-Arbre doit etre de degre au moins egal a 2")

    # Verifie si un noeud du BArbre est complet (ou non)

    def is_full(self, noeud):
        return len(noeud.cle) == 2 * self.t - 1

    # # Print the tree
    # def print_tree(self, x, level=0):
    #     print("Level ", level, " ", len(x.cle), end=":")
    #     for i in x.cle:
    #         print(i, end=" ")
    #     print()
    #     level += 1
    #     if len(x.fils) > 0:
    #         for i in x.fils:
    #             self.print_tree(i, l)
    #     return

    # Recherche une valeur parmi les cles d'un BArbre

    def recherche(self, valeur, noeud=None):
        # Si on ne precise pas a partir de quel noeud effectuer la recherche, on commence a la racine
        if noeud is None:
            noeud = self.racine
        # On cherche parmi les enfants (on trouve le bon intervalle de recherche en comparant la valeur aux cles)
        indice = 0
        n = len(noeud.cle)
        while indice < n and valeur > noeud.cle[indice]:
            indice += 1
        # Si la valeur recherchee se trouve dans les cles du noeud courant, on s'arrete et on renvoie True
        if indice < n and valeur == noeud.cle[indice]:
            return True
        # On s'arrete si la valeur n'est pas dans les cles et on a atteint une feuille (on renvoie False)
        elif noeud.est_feuille:
            return False
        return self.recherche(valeur, noeud.fils[indice])

    # Inserer une valeur dans un BArbre (algorithme proactif, cf. Cormen)

    def insertion(self, valeur):
        noeud = self.racine
        # On traite la racine a part puisque sa division est differente de celle des noeuds internes de l'arbre
        if self.is_full(noeud):
            nouvelle_racine = BTreeNode()
            nouvelle_racine.fils.append(self.racine)
            nouvelle_racine.est_feuille = False
            valeur_milieu_root, i, j = noeud.diviser(nouvelle_racine)
            # On choisit de quel cote continuer l'insertion
            if valeur < valeur_milieu_root:
                noeud = nouvelle_racine.fils[i]
            else:
                noeud = nouvelle_racine.fils[j]
            self.racine = nouvelle_racine
        # Tant qu'on n'a pas atteint une feuille (on insere uniquement dans une feuille)
        while not noeud.est_feuille:
            indice = len(noeud.cle) - 1
            # On cherche dans quel intervalle (avec quel enfant) poursuivre l'insertion (jusqu'a une feuille)
            while indice > 0 and valeur < noeud.cle[indice]:
                indice -= 1
            prochain_noeud = noeud.fils[indice + 1]
            if self.is_full(prochain_noeud):
                valeur_milieu, k, m = prochain_noeud.diviser(noeud)
                if valeur < valeur_milieu:
                    noeud = noeud.fils[k]
                else:
                    noeud = noeud.fils[m]
            else:
                noeud = prochain_noeud
        # Vu qu'on divise tous les noeuds complets dans la descente, on peut inserer la valeur dans la feuille
        noeud.cle.append(valeur)
        noeud.cle.sort()
        return self

    # Supprime une cle de l'arbre

    def suppression(self, valeur):
        return

    # Affiche le BArbre

    def __str__(self):
        return '\n' + self.racine.__str__() + '\n'.join([fils.__str__() for fils in self.racine.fils])

# ----------------------------------------------------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------------------------------------------------


# arbre = BTree(3)
# arbre.insertion(1)
# arbre.insertion(3)
# arbre.insertion(7)
# arbre.insertion(10)
# arbre.insertion(11)
# arbre.insertion(13)
# arbre.insertion(14)
# arbre.insertion(15)
# arbre.insertion(18)
# arbre.insertion(16)
# arbre.insertion(19)
# arbre.insertion(24)
# arbre.insertion(25)
# arbre.insertion(26)
# arbre.insertion(21)
# arbre.insertion(4)
# arbre.insertion(5)
# arbre.insertion(20)
# arbre.insertion(22)
# arbre.insertion(2)
# arbre.insertion(17)
# arbre.insertion(12)
# arbre.insertion(6)
# print(arbre)

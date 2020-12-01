# --------------------------------------- Projet Final : Btrees --------------------------------------------------


# Noeud d'un BArbre.
# Attributs : est_feuille (determine si un noeud est une feuille ou non) ; cle (liste des cles d'un noeud) ;
# fils (liste, liste des enfants d'un noeud)

# from collections import deque


class BTreeNode:
    def __init__(self):
        self.cle = list()
        self.fils = list()
        self.est_feuille = True

    # Fonction de parcours d'un noeud (utile pour redefinir la methode __iter__)

    def parcours(self):
        yield self
        for enfant in self.fils:
            yield from enfant.parcours()

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

    # Cree un noeud avec le bon format pour l'utiliser dans graphviz

    def genere_node_graphviz(self):
        res = "<f0> |"
        for i, k in enumerate(self.cle):
            res += '<f{}> {}|'.format(2 * i + 1, k)
            res += "<f{}> |".format(2 * (i + 1))
        return res[:-2]


class BTree:
    def __init__(self, t):
        self.racine = BTreeNode()
        # t est le degre minimal de l'arbre (t >= 2)
        self.t = t
        if self.t < 2:
            raise ValueError("Un B-Arbre doit etre de degre au moins egal a 2")

    def __iter__(self):
        return self.racine.parcours()

    def __next__(self):
        return self

    # Verifie si un noeud du BArbre est complet (ou non)

    def is_full(self, noeud):
        return len(noeud.cle) == 2 * self.t - 1

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
        if self.recherche(valeur):
            print("%d est deja dans le graphe !" % valeur)
            return
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
            while indice >= 0 and valeur < noeud.cle[indice]:
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

    def suppression(self, valeur, x=None):
        if not self.recherche(valeur):
            print("%d n'est pas dans le graphe, cette valeur ne peut pas etre supprimee !" % valeur)
            return
        if x is None:
            x = self.racine
        t = self.t
        i = 0
        while i < len(x.cle) and valeur > x.cle[i]:
            i += 1
        if x.est_feuille:
            if i < len(x.cle) and x.cle[i] == valeur:
                x.cle.pop(i)
                return
            return
        if i < len(x.cle) and x.cle[i] == valeur:
            return self.suppression_noeud_interne(x, valeur, i)
        elif len(x.fils[i].cle) >= t:
            self.suppression(valeur, x.fils[i])
        else:
            if i != 0 and i <= len(x.fils) - 2:
                if len(x.fils[i - 1].cle) >= t:
                    self.suppression_frere(x, i, i - 1)
                elif len(x.fils[i + 1].cle) >= t:
                    self.suppression_frere(x, i, i + 1)
                else:
                    self.suppression_fusion(x, i, i + 1)
            elif i == 0:
                if len(x.fils[i + 1].cle) >= t:
                    self.suppression_frere(x, i, i + 1)
                else:
                    self.suppression_fusion(x, i, i + 1)
            elif i == len(x.fils) - 1:
                if len(x.fils[i - 1].cle) >= t:
                    self.suppression_frere(x, i, i - 1)
                else:
                    self.suppression_fusion(x, i, i - 1)
            self.suppression(valeur, x.fils[i])

    # Delete internal node

    def suppression_noeud_interne(self, x, valeur, i):
        t = self.t
        if x.est_feuille:
            if x.cle[i] == valeur:
                x.cle.pop(i)
                return
            return
        if len(x.fils[i].cle) >= t:
            x.cle[i] = self.suppression_predecesseur(x.fils[i])
            return
        elif len(x.fils[i + 1].cle) >= t:
            x.cle[i] = self.suppression_sucesseur(x.fils[i + 1])
            return
        else:
            self.suppression_fusion(x, i, i + 1)
            self.suppression_noeud_interne(x.fils[i], valeur, self.t - 1)

    # Delete the predecessor

    def suppression_predecesseur(self, x):
        if x.est_feuille:
            return x.pop()
        n = len(x.cle) - 1
        if len(x.fils[n].cle) >= self.t:
            self.suppression_frere(x, n + 1, n)
        else:
            self.suppression_fusion(x, n, n + 1)
        self.suppression_predecesseur(x.fils[n])

    # Delete the successor

    def suppression_sucesseur(self, x):
        if x.est_feuille:
            return x.cle.pop(0)
        if len(x.fils[1].cle) >= self.t:
            self.suppression_frere(x, 0, 1)
        else:
            self.suppression_fusion(x, 0, 1)
        self.suppression_sucesseur(x.fils[0])

    # Delete resolution

    def suppression_fusion(self, x, i, j):
        cnode = x.fils[i]
        if j > i:
            rsnode = x.fils[j]
            cnode.cle.append(x.cle[i])
            for k in range(len(rsnode.cle)):
                cnode.cle.append(rsnode.cle[k])
                if len(rsnode.fils) > 0:
                    cnode.fils.append(rsnode.fils[k])
            if len(rsnode.fils) > 0:
                cnode.fils.append(rsnode.fils.pop())
            new = cnode
            x.cle.pop(i)
            x.fils.pop(j)
        else:
            lsnode = x.fils[j]
            lsnode.cle.append(x.cle[j])
            for i in range(len(cnode.cle)):
                lsnode.cle.append(cnode.cle[i])
                if len(lsnode.fils) > 0:
                    lsnode.fils.append(cnode.fils[i])
            if len(lsnode.fils) > 0:
                lsnode.fils.append(cnode.fils.pop())
            new = lsnode
            x.cle.pop(j)
            x.fils.pop(i)
        if x == self.racine and len(x.cle) == 0:
            self.racine = new

    # Delete the sibling

    def suppression_frere(self, x, i, j):
        # cnode : noeud central
        cnode = x.fils[i]
        if i < j:
            # rsnode : noeud frere droit (right sibling node)
            rsnode = x.fils[j]
            cnode.cle.append(x.cle[i])
            x.cle[i] = rsnode.cle[0]
            if len(rsnode.fils) > 0:
                cnode.fils.append(rsnode.fils[0])
                rsnode.fils.pop(0)
            rsnode.cle.pop(0)
        else:
            # lsnode : noeud frere gauche (left sibling node)
            lsnode = x.fils[j]
            cnode.cle.insert(0, x.cle[i - 1])
            x.cle[i - 1] = lsnode.cle.pop()
            if len(lsnode.fils) > 0:
                cnode.fils.insert(0, lsnode.fils.pop())

    # Fonction "print" d'un BArbre

    def __str__(self):
        return '\n' + self.racine.__str__() + '\n'.join([fils.__str__() for fils in self.racine.fils])


# ----------------------------------------------------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------------------------------------------------


def remplir_arbre(tree, liste):
    for e in liste:
        tree.insertion(e)


arbre = BTree(3)
liste_valeurs = [1, 3, 7, 10, 11, 13, 14, 15, 18, 16, 19, 24, 25, 26, 21, 4, 5, 20, 22, 2, 17, 12, 6]
remplir_arbre(arbre, liste_valeurs)

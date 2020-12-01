# --------------------------------------- Projet Final : Btrees --------------------------------------------------


# Classe representant un noeud d'un B-arbre

class BTreeNode:
    def __init__(self):
        # liste des clés d'un noeud (liste d'entiers)
        self.cle = list()

        # liste des fils d'un noeud (liste de noeuds)
        self.fils = list()

        # booleen qui determine qu'un noeud est une feuille ou non
        self.est_feuille = True

    # Fonction de parcours d'un noeud (utile pour redéfinir la methode __iter__)

    def parcours(self):
        yield self
        for enfant in self.fils:
            yield from enfant.parcours()

    # Fonction permettant de rajouter un fils à un noeud

    def ajouter_fils(self, nouveau_noeud):
        i = len(self.fils) - 1
        while i >= 0 and self.fils[i].cle[0] > nouveau_noeud.cle[0]:
            i -= 1
        return self.fils[:i + 1] + [nouveau_noeud] + self.fils[i + 1:]

    # Fonction qui permet de diviser (split) un noeud non racine

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

        # On verifie si le nouveau noeud est une feuille ou non
        if len(nouveau_noeud.fils) > 0:
            nouveau_noeud.est_feuille = False

        # On rajoute le nouveau noeud à la liste des enfants du noeud "parent"
        parent.fils = parent.ajouter_fils(nouveau_noeud)

        # On recupère les indices (dans la liste des enfants du noeud "parent") des noeuds obtenus après division
        i, j = parent.fils.index(self), parent.fils.index(nouveau_noeud)
        # On retourne ces trois valeurs pour pouvoir décider où effectuer la recherche/insertion après le split
        return valeur_milieu, i, j

    # Cree un noeud avec le bon format pour l'utiliser dans graphviz

    def genere_node_graphviz(self):
        res = "<f0> |"
        for i, k in enumerate(self.cle):
            res += '<f{}> {}|'.format(2 * i + 1, k)
            res += "<f{}> |".format(2 * (i + 1))
        return res[:-2]


# Classe représentant un B-arbre

class BTree:
    def __init__(self, t):
        self.racine = BTreeNode()
        # t est le degré minimal d'un B-arbre tel que t >= 2 et :
        # 1. Un noeud quelconque peut contenir au plus 2*t - 1 clés
        # 2. Un noeud non racine doit contenir au moins t-1 clés
        self.t = t
        if self.t < 2:
            raise ValueError("Un B-Arbre doit être de degré au moins égal à 2 !")

    # On définit une méthode __iter__ pour la structure de B-arbre pour pouvoir itérer sur un arbre grâce à un "for"

    def __iter__(self):
        return self.racine.parcours()

    def __next__(self):
        return self

    # Fonction pour vérifier qu'un noeud du B-arbre est complet ou non 

    def est_complet(self, noeud):
        return len(noeud.cle) == 2 * self.t - 1

    # Fonction qui recherche une valeur donnée dans un B-arbre
    # La fonction renvoie True ou False selon que la valeur est dans l'arbre ou non

    def recherche(self, valeur, noeud=None):
        # Si on ne precise pas à partir de quel noeud effectuer la recherche, on commence à la racine
        if noeud is None:
            noeud = self.racine

        # On trouve le bon intervalle de recherche en comparant la valeur recherchée aux clés du noeud courant
        indice = 0
        n = len(noeud.cle)
        while indice < n and valeur > noeud.cle[indice]:
            indice += 1

        # Si la valeur recherchee se trouve dans les clés du noeud courant, on s'arrete et on renvoie True
        if indice < n and valeur == noeud.cle[indice]:
            return True

        # Si on n'a pas trouvé la valeur dans les clés du noeud courant et que c'est un noeud feuille, on renvoie False
        elif noeud.est_feuille:
            return False

        # Sinon on poursuit la recherche parmi les clés du "bon fils" du noeud courant
        return self.recherche(valeur, noeud.fils[indice])

    # Fonction qui insère une valeur dans un B-arbre via un algorithme proactif (cf. Cormen)

    def insertion(self, valeur):
        # Si la valeur qu'on souhaite insérer existe déjà dans l'arbre, on arrête l'insertion
        if self.recherche(valeur):
            print("%d est déjà dans l'arbre !" % valeur)
            return

        noeud = self.racine

        # On traite la racine à part puisque sa division est différente de celle des noeuds internes de l'arbre
        if self.est_complet(noeud):
            nouvelle_racine = BTreeNode()
            nouvelle_racine.fils.append(self.racine)
            nouvelle_racine.est_feuille = False
            # On divise l'ancienne racine en deux nouveaux noeuds (qui seront les fils de "nouvelle_racine")
            valeur_milieu_root, i, j = noeud.diviser(nouvelle_racine)
            # On choisit de quel côté (avec quel enfant) poursuivre l'insertion
            if valeur < valeur_milieu_root:
                noeud = nouvelle_racine.fils[i]
            else:
                noeud = nouvelle_racine.fils[j]
            self.racine = nouvelle_racine

        # Tant qu'on n'a pas atteint une feuille (on insère une valeur uniquement dans une feuille)
        while not noeud.est_feuille:
            indice = len(noeud.cle) - 1

            # On cherche dans quel intervalle (avec quel enfant) poursuivre l'insertion
            while indice >= 0 and valeur < noeud.cle[indice]:
                indice -= 1
            prochain_noeud = noeud.fils[indice + 1]

            # Si "prochain_noeud" est complet, on le divise avant de poursuivre l'insertion
            if self.est_complet(prochain_noeud):
                valeur_milieu, l, r = prochain_noeud.diviser(noeud)
                if valeur < valeur_milieu:
                    noeud = noeud.fils[l]
                else:
                    noeud = noeud.fils[r]
            else:
                noeud = prochain_noeud

    # Vu qu'on divise tous les noeuds complets dans la déscente, on peut insérer la valeur directement dans la feuille
        noeud.cle.append(valeur)
        noeud.cle.sort()
        return self

    # Supprime une cle de l'arbre

    def suppression(self, valeur, noeud=None):
        # On vérifie que la valeur à supprimer est bien présente dans l'arbre
        if not self.recherche(valeur):
            print("%d n'est pas dans l'arbre, cette valeur ne peut pas être supprimée !" % valeur)
            return

        if noeud is None:
            noeud = self.racine
        t = self.t
        i = 0
        while i < len(noeud.cle) and valeur > noeud.cle[i]:
            i += 1
        if noeud.est_feuille:
            if i < len(noeud.cle) and noeud.cle[i] == valeur:
                noeud.cle.pop(i)
                return
            return
        if i < len(noeud.cle) and noeud.cle[i] == valeur:
            return self.suppression_noeud_interne(noeud, valeur, i)
        elif len(noeud.fils[i].cle) >= t:
            self.suppression(valeur, noeud.fils[i])
        else:
            if i != 0 and i <= len(noeud.fils) - 2:
                if len(noeud.fils[i - 1].cle) >= t:
                    self.suppression_frere(noeud, i, i - 1)
                elif len(noeud.fils[i + 1].cle) >= t:
                    self.suppression_frere(noeud, i, i + 1)
                else:
                    self.suppression_fusion(noeud, i, i + 1)
            elif i == 0:
                if len(noeud.fils[i + 1].cle) >= t:
                    self.suppression_frere(noeud, i, i + 1)
                else:
                    self.suppression_fusion(noeud, i, i + 1)
            elif i == len(noeud.fils) - 1:
                if len(noeud.fils[i - 1].cle) >= t:
                    self.suppression_frere(noeud, i, i - 1)
                else:
                    self.suppression_fusion(noeud, i, i - 1)
            self.suppression(valeur, noeud.fils[i])

    # Delete internal node

    def suppression_noeud_interne(self, noeud, valeur, i):
        t = self.t
        if noeud.est_feuille:
            if noeud.cle[i] == valeur:
                noeud.cle.pop(i)
                return
            return
        if len(noeud.fils[i].cle) >= t:
            noeud.cle[i] = self.suppression_predecesseur(noeud.fils[i])
            return
        elif len(noeud.fils[i + 1].cle) >= t:
            noeud.cle[i] = self.suppression_sucesseur(noeud.fils[i + 1])
            return
        else:
            self.suppression_fusion(noeud, i, i + 1)
            self.suppression_noeud_interne(noeud.fils[i], valeur, self.t - 1)

    # Delete the predecessor

    def suppression_predecesseur(self, noeud):
        if noeud.est_feuille:
            return noeud.pop()
        n = len(noeud.cle) - 1
        if len(noeud.fils[n].cle) >= self.t:
            self.suppression_frere(noeud, n + 1, n)
        else:
            self.suppression_fusion(noeud, n, n + 1)
        self.suppression_predecesseur(noeud.fils[n])

    # Delete the successor

    def suppression_sucesseur(self, noeud):
        if noeud.est_feuille:
            return noeud.cle.pop(0)
        if len(noeud.fils[1].cle) >= self.t:
            self.suppression_frere(noeud, 0, 1)
        else:
            self.suppression_fusion(noeud, 0, 1)
        self.suppression_sucesseur(noeud.fils[0])

    # Delete resolution

    def suppression_fusion(self, noeud, i, j):
        cnode = noeud.fils[i]
        if j > i:
            rsnode = noeud.fils[j]
            cnode.cle.append(noeud.cle[i])
            for k in range(len(rsnode.cle)):
                cnode.cle.append(rsnode.cle[k])
                if len(rsnode.fils) > 0:
                    cnode.fils.append(rsnode.fils[k])
            if len(rsnode.fils) > 0:
                cnode.fils.append(rsnode.fils.pop())
            new = cnode
            noeud.cle.pop(i)
            noeud.fils.pop(j)
        else:
            lsnode = noeud.fils[j]
            lsnode.cle.append(noeud.cle[j])
            for i in range(len(cnode.cle)):
                lsnode.cle.append(cnode.cle[i])
                if len(lsnode.fils) > 0:
                    lsnode.fils.append(cnode.fils[i])
            if len(lsnode.fils) > 0:
                lsnode.fils.append(cnode.fils.pop())
            new = lsnode
            noeud.cle.pop(j)
            noeud.fils.pop(i)
        if noeud == self.racine and len(noeud.cle) == 0:
            self.racine = new

    # Delete the sibling

    def suppression_frere(self, noeud, i, j):
        # cnode : noeud central
        cnode = noeud.fils[i]
        if i < j:
            # rsnode : noeud frere droit (right sibling node)
            rsnode = noeud.fils[j]
            cnode.cle.append(noeud.cle[i])
            noeud.cle[i] = rsnode.cle[0]
            if len(rsnode.fils) > 0:
                cnode.fils.append(rsnode.fils[0])
                rsnode.fils.pop(0)
            rsnode.cle.pop(0)
        else:
            # lsnode : noeud frere gauche (left sibling node)
            lsnode = noeud.fils[j]
            cnode.cle.insert(0, noeud.cle[i - 1])
            noeud.cle[i - 1] = lsnode.cle.pop()
            if len(lsnode.fils) > 0:
                cnode.fils.insert(0, lsnode.fils.pop())


# ----------------------------------------------------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------------------------------------------------


def remplir_arbre(tree, liste):
    for e in liste:
        tree.insertion(e)


arbre = BTree(3)
liste_valeurs = [1, 3, 7, 10, 11, 13, 14, 15, 18, 16, 19, 24, 25, 26, 21, 4, 5, 20, 22, 2, 17, 12, 6]
remplir_arbre(arbre, liste_valeurs)

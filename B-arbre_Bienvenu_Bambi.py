# --------------------------------------- Projet Final : Btrees --------------------------------------------------

from graphviz import Digraph, nohtml


# ----------------------------------------------------------------------------------------------------------------------
# Implémentation de la classe B-arbre avec notamment les fonctions recherche, insertion et suppresion
# ----------------------------------------------------------------------------------------------------------------------


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

    def recherche(self, file, valeur, log=True, noeud=None):
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
            if log:
                file.write("- Recherche de la valeur %d\n%d a été retrouvé dans le graphe !\n" % (valeur, valeur))
            return True

        # Si on n'a pas trouvé la valeur dans les clés du noeud courant et que c'est un noeud feuille, on renvoie False
        elif noeud.est_feuille:
            if log:
                file.write("- Recherche de la valeur %d\n%d n'a pas été retrouvé dans le graphe !\n" % (valeur, valeur))
            return False

        # Sinon on poursuit la recherche parmi les clés du "bon fils" du noeud courant
        return self.recherche(file, valeur, log, noeud.fils[indice])

    # Fonction qui insère une valeur dans un B-arbre via un algorithme proactif (cf. Cormen)

    def insertion(self, file, valeur):
        file.write("- Insertion de la valeur %d\n" % valeur)
        # Si la valeur qu'on souhaite insérer existe déjà dans l'arbre, on arrête l'insertion
        if self.recherche(file, valeur, log=False):
            file.write("%d n'a pas été rajouté, la valeur était déjà dans l'arbre !\n" % valeur)
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

        # Vu qu'on divise tous les noeuds complets dans la déscente, on peut insérer la valeur directement dans la
        # feuille
        noeud.cle.append(valeur)
        noeud.cle.sort()
        return self

    # Supprime une clé de l'arbre

    def suppression(self, file, valeur, noeud=None):
        file.write("- Suppression de la valeur %d\n" % valeur)
        # On vérifie que la valeur à supprimer est bien présente dans l'arbre
        if not self.recherche(file, valeur, log=False):
            file.write("%d n'est pas dans l'arbre. Cette valeur n'a pas pu être supprimée !\n" % valeur)
            return

        # Si on ne précise pas le noeud où effectuer la suppression, on commence à la racine
        if noeud is None:
            noeud = self.racine

        t = self.t  # pour alléger l'écriture
        i = 0

        # On trouve le bon intervalle (de suppression) en comparant la valeur à supprimer aux clés du noeud courant
        while i < len(noeud.cle) and valeur > noeud.cle[i]:
            i += 1

        # Si on atteint un noeud feuille et que la valeur à supprimer fait partie de ses clés, on la supprime
        # Ce noeud aura nécessairement plus que le nombre min de clés puisqu'on modifie l'arbre en descendant
        if noeud.est_feuille:
            if i < len(noeud.cle) and noeud.cle[i] == valeur:
                noeud.cle.pop(i)
                return
            return

        # Si le noeud courant est un noeud interne et que la valeur fait partie de ses clés :
        if i < len(noeud.cle) and noeud.cle[i] == valeur:
            return self.suppression_noeud_interne(noeud, valeur, i)

        # Si le noeud fils où on doit poursuivre la suppression a suffisamment de clés, on continue vers ce fils
        elif len(noeud.fils[i].cle) >= t:
            self.suppression(file, valeur, noeud.fils[i])

        # Si le noeud fils vers lequel on doit poursuivre la suppression a exactement le nombre min de clés possibles :
        else:
            # Si le fils n'est pas aux extrémités...
            if i != 0 and i <= len(noeud.fils) - 2:
                # ...on s'intéresse à son frère gauche. Si celui-ci a plus de clés que le min, il prêtera une clé
                if len(noeud.fils[i - 1].cle) >= t:
                    self.suppression_frere(noeud, i, i - 1)
                # sinon, on s'intéresse à son frère droit. Si celui-ci a plus de clés que le min, il prêtera une clé
                elif len(noeud.fils[i + 1].cle) >= t:
                    self.suppression_frere(noeud, i, i + 1)
                # Si aucun des deux frères n'a assez de noeud, on procèdera à une fusion au moment de la suppression
                else:
                    self.suppression_fusion(noeud, i, i + 1)

            # Si le fils est à l'extrémité gauche (le premier fils à gauche)...
            elif i == 0:
                # ...on s'intéresse à son frère droit. Si celui-ci a plus de clés que le min, il prêtera une clé
                if len(noeud.fils[i + 1].cle) >= t:
                    self.suppression_frere(noeud, i, i + 1)
                # sinon on procèdera à une fusion au moment de la suppression
                else:
                    self.suppression_fusion(noeud, i, i + 1)

            # Si le fils est à l'extrémité droite (le dernier fils à droite)...
            elif i == len(noeud.fils) - 1:
                # ...on s'intéresse à son frère gauche. Si celui-ci a plus de clés que le min, il prêtera une clé
                if len(noeud.fils[i - 1].cle) >= t:
                    self.suppression_frere(noeud, i, i - 1)
                # sinon on procèdera à une fusion au moment de la suppression
                else:
                    self.suppression_fusion(noeud, i, i - 1)
            self.suppression(file, valeur, noeud.fils[i])

    # Suppression d'un noeud interne

    def suppression_noeud_interne(self, noeud, valeur, i):
        t = self.t  # pour alléger l'écriture
        if noeud.est_feuille:
            if noeud.cle[i] == valeur:
                noeud.cle.pop(i)
                return
            return

        # inorder predecessor
        if len(noeud.fils[i].cle) >= t:
            noeud.cle[i] = self.suppression_predecesseur(noeud.fils[i])
            return

        # inorder successor
        elif len(noeud.fils[i + 1].cle) >= t:
            noeud.cle[i] = self.suppression_sucesseur(noeud.fils[i + 1])
            return
        else:
            self.suppression_fusion(noeud, i, i + 1)
            self.suppression_noeud_interne(noeud.fils[i], valeur, self.t - 1)

    # Suppression "predecesseur"

    def suppression_predecesseur(self, noeud):
        if noeud.est_feuille:
            return noeud.pop()
        n = len(noeud.cle) - 1
        if len(noeud.fils[n].cle) >= self.t:
            self.suppression_frere(noeud, n + 1, n)
        else:
            self.suppression_fusion(noeud, n, n + 1)
        self.suppression_predecesseur(noeud.fils[n])

    # Suppression "successeur"

    def suppression_sucesseur(self, noeud):
        if noeud.est_feuille:
            return noeud.cle.pop(0)
        if len(noeud.fils[1].cle) >= self.t:
            self.suppression_frere(noeud, 0, 1)
        else:
            self.suppression_fusion(noeud, 0, 1)
        self.suppression_sucesseur(noeud.fils[0])

    # Suppression "fusion"

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

    # Suppression "frère"

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
# Visualisation d'un B-arbre grâce aux outils de la librairie graphviz
# ----------------------------------------------------------------------------------------------------------------------


def init_digraph():
    return Digraph('g', filename='arbre_bienvenu.gv',
                   node_attr={'shape': 'record', 'height': '.1'})


# Fonction qui ajoute un noeud au graphe

def add_node(graph, node, node_number):
    graph.node('node{}'.format(node_number), nohtml(node.genere_node_graphviz()))


# Fonction principale qui génère notre B-arbre puis l'affiche dans une fenêtre

def genere_digrap(arbre):
    g = init_digraph()
    liste_nodes = [n for n in arbre]

    # Création des nodes dans graphViz
    for i, node in enumerate(arbre):
        add_node(g, node, i)

    # Création des arêtes
    for ind, node in enumerate(liste_nodes):
        parent_init = 'node{}:f'.format(ind)
        for fils in node.fils:
            parent = parent_init
            j = liste_nodes.index(fils)
            ind_edge = len(fils.cle)
            bonne_cle = 0
            if node.cle[bonne_cle] <= fils.cle[0]:
                if node.cle[-1] < fils.cle[0]:
                    bonne_cle = 2 * len(node.cle)
                else:
                    for i, _ in enumerate(node.cle[:-1]):
                        if node.cle[i + 1] > fils.cle[0]:
                            bonne_cle = 2 * (i + 1)
                            break
            parent += str(bonne_cle)
            enfant = 'node{}:f{}'.format(j, ind_edge)
            g.edge(parent, enfant)

    # Affichage de l'arbre
    g.view()


# ----------------------------------------------------------------------------------------------------------------------
# Mode batch
# ----------------------------------------------------------------------------------------------------------------------


def batch():
    liste_operations = input("Entrez le nom du fichier txt : (exemple : operations.txt)\n")
    operations = [line.rstrip('\n') for line in open(liste_operations)]
    open("log_batch_bienvenu.txt", "w").close()
    fichier = open("log_batch_bienvenu.txt", "a")
    t = int(operations.pop(0))
    arbre = BTree(t)
    for element in operations:
        value = int(element[1:])
        if element[0] == "a":
            arbre.insertion(fichier, value)
        elif element[0] == "r":
            arbre.suppression(fichier, value)
        elif element[0] == "s":
            arbre.recherche(fichier, value)
        else:
            fichier.write("!! Erreur, préfixe '%s' non reconnu !!\n" % element[0])
    fichier.close()
    genere_digrap(arbre)


# ----------------------------------------------------------------------------------------------------------------------
# Mode interactif
# ----------------------------------------------------------------------------------------------------------------------


def interactif():
    open("log_inter_bienvenu.txt", "w").close()
    fichier = open("log_inter_bienvenu.txt", "a")
    t = int(input("Entrez le degré de l'arbre :\n"))
    arbre = BTree(t)
    opr = input("Entrez votre sequence d'operations en les separant par des espaces :\n")
    operations = opr.split()
    reponse = input("Souhaitez-vous entrer d'autres opérations ? Y or N\n")
    while reponse.upper() == "Y":
        opr = input("Entrez votre sequence d'operations en les separant par des espaces :\n")
        operations.extend(opr.split())
        reponse = input("Souhaitez-vous entrer d'autres opérations ? Y or N\n")
    for element in operations:
        value = int(element[1:])
        if element[0] == "a":
            arbre.insertion(fichier, value)
        elif element[0] == "r":
            arbre.suppression(fichier, value)
        elif element[0] == "s":
            arbre.recherche(fichier, value)
        else:
            fichier.write("!! Erreur, préfixe '%s' non reconnu !!\n" % element[0])
    fichier.close()
    genere_digrap(arbre)


# ------------------------------------------------- main ----------------------------------------------------------
def main():
    mode = input("Quel mode souhaitez-vous utiliser ? 1=batch et 2=interactif\n")
    while (mode != "1") and (mode != "2"):
        print("Entrez 1 ou 2")
        mode = input("Quel mode souhaitez-vous utiliser ? 1=batch et 2=interactif\n")
    if mode == "1":
        batch()
    elif mode == "2":
        interactif()


main()

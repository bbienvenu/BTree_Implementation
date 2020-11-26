from BTree_Bienvenu import BTree, BTreeNode
from graphviz import Digraph, nohtml


def init_digraph():
    return Digraph('g', filename='graph.gv',
                   node_attr={'shape': 'record', 'height': '.1'})


def add_node(graph, node, node_number):
    graph.node('node{}'.format(node_number), nohtml(node.genere_node_graphviz()))


def genere_digrap(arbre):
    g = init_digraph()
    liste_nodes = [n for n in arbre]
    # Création des nodes dans graphViz
    for i, node in enumerate(arbre):
        add_node(g, node, i)
    # Création des arêtes
    for i, node in enumerate(liste_nodes):
        parent_init = 'node{}:f'.format(i)
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


def remplir_arbre(arbre, liste):
    for value in liste:
        arbre.insertion(value)

# liste = [1, 3, 7, 10, 11, 13, 14, 15, 18, 16, 19, 24, 25, 26, 21, 4, 5, 20, 22, 2, 17, 12, 6]

def main():
    arbre = BTree(3)
    liste = [1, 3, 7, 10, 11, 13, 14, 15, 18, 16, 19, 24, 25, 26, 21, 4, 5, 20, 22, 2, 17, 12, 6]
    remplir_arbre(arbre, liste)
    # print(arbre)
    genere_digrap(arbre)


main()

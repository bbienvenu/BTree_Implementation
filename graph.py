#!/usr/bin/env python3

from BTree_Bienvenu import BTree, BTreeNode
from graphviz import Digraph, nohtml

def init_digraph():
    return Digraph('g', filename='Test_btree.gv', 
                    node_attr={'shape': 'record', 'height': '.1'})

def add_node(graph, node, node_number):
    graph.node('node{}'.format(node_number), nohtml(node.genere_node_graphviz()))

def genere_digrap(arbre):
    g = init_digraph()
    liste_nodes = [n for n in arbre]
    # Création des nodes dans graphViz
    for i, node in enumerate(liste_nodes):
        add_node(g, node, i)

    

    # TODO : les edges

    g.view()
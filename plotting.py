import igraph
from igraph import Graph, EdgeSeq


def plotBinTree(tree: Node):
    G = Graph.Tree(nr_vertices, 2) # 2 stands for children number
    lay = G.layout('rt')
    
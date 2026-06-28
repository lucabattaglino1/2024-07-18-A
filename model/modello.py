from networkx import DiGraph
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = DiGraph()
        self._nodes = []
        self._idMapAO = {}

    def getCromosomi(self):
        return DAO.get_all_genes()

    def buildGraph(self, c1, c2):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(c1, c2)
        self._idMapAO = {}
        for n in self._nodes:
            if n.GeneID not in self._idMapAO:
                self._idMapAO[n.GeneID] = []
            self._idMapAO[n.GeneID].append(n)

        self._graph.add_nodes_from(self._nodes)
        self.addEdges(c1, c2)

    def addEdges(self, c1, c2):
        for id1, id2, peso in DAO.getCoppieRaw(c1, c2):
            for n1 in self._idMapAO.get(id1, []):
                for n2 in self._idMapAO.get(id2, []):
                    if n1.Chromosome < n2.Chromosome:
                        self._graph.add_edge(n1, n2, weight=peso)
                    elif n2.Chromosome < n1.Chromosome:
                        self._graph.add_edge(n2, n1, weight=peso)
                    else:
                        self._graph.add_edge(n1, n2, weight=peso)
                        self._graph.add_edge(n2, n1, weight=peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getTop5Uscenti(self):
        risultato = []
        for n in self._graph.nodes:
            numArchi = self._graph.out_degree(n)
            pesoTotale = 0
            for v in self._graph.successors(n):
                pesoTotale += self._graph[n][v]["weight"]
            risultato.append((n, numArchi, pesoTotale))

        risultato.sort(key=lambda x: x[1], reverse=True)
        return risultato[:5]
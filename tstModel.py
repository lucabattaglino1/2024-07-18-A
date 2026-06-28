# tstModel.py
from model.modello import Model

mdl = Model()
mdl.buildGraph(3, 7)
print(f"Nodi: {mdl.getNumNodes()}")
print(f"Archi: {mdl.getNumEdges()}")

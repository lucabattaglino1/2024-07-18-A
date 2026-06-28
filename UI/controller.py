import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDMin(self):
        cromosomi = self._model.getCromosomi()
        for c in cromosomi:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(str(c)))
        self._view.update_page()

    def fillDDMax(self):
        cromosomi = self._model.getCromosomi()
        for c in cromosomi:
            self._view.dd_max_ch.options.append(ft.dropdown.Option(str(c)))
        self._view.update_page()


    def handle_graph(self, e):
        c1 = self._view.dd_min_ch.value
        c2 = self._view.dd_max_ch.value

        if c1 is None:
            self._view.create_alert("Seleziona un valore")
            return

        if c2 is None:
            self._view.create_alert("Seleziona un valore")
            return

        if (c1 > c2):
            self._view.create_alert("Attenzione! il cromosoma minimo è maggiore del massimo")
            return

        self._model.buildGraph(c1, c2)

        # pulisco la lista risultati
        self._view.txt_result1.controls.clear()

        # stampo le info
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))

        self._view.txt_result1.controls.append(ft.Text("Top 5 nodi per archi uscenti:"))
        for nodo, numArchi, peso in self._model.getTop5Uscenti():
            self._view.txt_result1.controls.append(
                ft.Text(f"{nodo.GeneID}: {numArchi} archi uscenti, peso totale {peso}"))

        self._view.update_page()


    def handle_dettagli(self, e):
        pass


    def handle_path(self, e):
        pass
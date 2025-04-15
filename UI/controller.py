import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self.nerc = None

    def handleWorstCase(self, e):
        # TO FILL
        self._view._txtOut.controls.clear()
        if self._view._txtYears.value is None or self._view._txtHours.value is None or self.nerc is None:
            self._view.create_alert("Attenzione: inserisci tutti i valori!")
            self._view.update_page()
            return
        maxY = int(self._view._txtYears.value)
        maxH = int(self._view._txtHours.value)
        nerc = self.nerc
        listaBest, maxPersone, oreTotali = self._model.worstCase(nerc, maxY, maxH)
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {maxPersone}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {oreTotali}"))
        for i in listaBest:
            self._view._txtOut.controls.append(ft.Text(str(i)))
        self._view.update_page()
        return

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.value, data=n, on_click=self.salvaNerc))  # per salvare l'oggetto nerc
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def salvaNerc(self, e):
        self.nerc = e.control.data

import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.maxPersone = -1
        self.oreTotali = 0


    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self._solBest = []
        self.maxPersone = -1
        self.oreTotali = 0
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, self._listEvents)
        self._solBest.sort(key=lambda x: x.id)
        return self._solBest, self.maxPersone, self.oreTotali

    def isAdmissible(self, parziale, e, maxY, maxH):
        oreTotali = 0
        for i in parziale:
            ore = ((i.date_event_finished - i.date_event_began).total_seconds()) / 3600
            oreTotali += ore
        if (oreTotali + (((e.date_event_finished - e.date_event_began).total_seconds()) / 3600)) > maxH:
            return False
        parziale.append(e)
        anni = []
        for i in parziale:
            anni.append(i.date_event_finished.year)
        annoMax = max(anni)
        annoMin = min(anni)
        if (annoMax - annoMin) > maxY:
            parziale.remove(e)
            return False
        parziale.remove(e)
        return True


    def isFinished(self, parziale, lista_eventi, maxY, maxH):
        # ritorna False se trova un evento che può essere aggiunto al parziale, ritorna True se non puoi più aggiungere e quindi parziale è completo
        for e in lista_eventi:
            if e not in parziale:
                if self.isAdmissible(parziale, e, maxY, maxH):  # ritorna True se è possibile aggiungere
                    return False
        return True

    def calcolaPersone(self, parziale):
        contaPersone = 0
        for e in parziale:
            contaPersone += e.customers_affected
        return contaPersone

    def contaOre(self, parziale):
        contaOre = 0
        for e in parziale:
            contaOre += ((e.date_event_finished - e.date_event_began).total_seconds()) / 3600
        return contaOre

    def ricorsione(self, parziale, maxY, maxH, lista_eventi):
        # TO FILL
        if self.isFinished(parziale, lista_eventi, maxY, maxH):
            if self.calcolaPersone(parziale) > self.maxPersone:
                self.maxPersone = self.calcolaPersone(parziale)
                self._solBest = copy.deepcopy(parziale)
                self.oreTotali = self.contaOre(parziale)
                #print(self._solBest)
                #print(self.maxPersone)
        else:
            for e in lista_eventi:
                if self.isAdmissible(parziale, e, maxY, maxH) and e not in parziale:
                    parziale.append(e)
                    self.ricorsione(parziale, maxY, maxH, lista_eventi)
                    parziale.pop()  # backtracking

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()
        self._listNerc.sort(key=lambda x: x.value)

    @property
    def listNerc(self):
        return self._listNerc



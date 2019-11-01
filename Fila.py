import heapq

class FilaDePrioridade:

    def __init__(self):
        self._fila = []
    
    def getFila(self):
        return self._fila

    def inserir(self, item, prioridade):
        heapq.heappush(self._fila, (prioridade, item))

    def remover(self):
        return heapq.heappop(self._fila)[-1]
    
 
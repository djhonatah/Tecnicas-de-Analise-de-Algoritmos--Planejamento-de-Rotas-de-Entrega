import math

class Backtracking:
    def __init__(self, matriz_dist):
        self.matriz_dist = matriz_dist
        self.n = len(matriz_dist) - 1
        self.melhor_distancia = float('inf')
        self.melhor_rota = []
        self.estados_explorados = 0

    def resolver(self):
        self._backtracking(0, {0}, [0], 0.0)
        return self.melhor_distancia, self.melhor_rota, self.estados_explorados

    def _backtracking(self, cliente_atual, visitados, rota_atual, distancia_atual):
        self.estados_explorados += 1

        if len(visitados) == self.n + 1:
            d = distancia_atual + self.matriz_dist[cliente_atual][0]
            if d < self.melhor_distancia:
                self.melhor_distancia = d
                self.melhor_rota = rota_atual.copy()
            return

        if distancia_atual >= self.melhor_distancia:
            return

        for prox in range(self.n + 1):
            if prox not in visitados:
                visitados.add(prox)
                rota_atual.append(prox)
                self._backtracking(
                    prox,
                    visitados,
                    rota_atual,
                    distancia_atual + self.matriz_dist[cliente_atual][prox]
                )
                rota_atual.pop()
                visitados.remove(prox)

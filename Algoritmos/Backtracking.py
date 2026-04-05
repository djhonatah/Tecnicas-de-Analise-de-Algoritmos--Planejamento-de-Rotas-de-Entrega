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

    def _backtracking(self, atual, visitados, rota_atual, dist_atual):
        self.estados_explorados += 1

        # Poda por custo: se a distância acumulada já supera a melhor
        # solução conhecida, não há sentido em continuar este ramo.
        # Esta verificação antecipada evita explorar o caso base e todos
        # os filhos de um nó claramente inviável.
        if dist_atual >= self.melhor_distancia:
            return

        # Caso base: todos os nós foram visitados → fecha o ciclo
        if len(visitados) == self.n + 1:
            d = dist_atual + self.matriz_dist[atual][0]
            if d < self.melhor_distancia:
                self.melhor_distancia = d
                self.melhor_rota = rota_atual.copy()
            return

        for prox in range(1, self.n + 1):
            if prox not in visitados:
                visitados.add(prox)
                rota_atual.append(prox)
                self._backtracking(
                    prox,
                    visitados,
                    rota_atual,
                    dist_atual + self.matriz_dist[atual][prox]
                )
                rota_atual.pop()
                visitados.remove(prox)

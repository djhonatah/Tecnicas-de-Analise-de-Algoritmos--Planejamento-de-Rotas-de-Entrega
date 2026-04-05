import matplotlib.pyplot as plt
import time
import random
import os
from Algoritmos.Backtracking import Backtracking
from Algoritmos.BranchAndBound import BranchAndBound
from Algoritmos.ProgramacaoDinamica import ProgramacaoDinamica
from Algoritmos.EstrategiaGulosa import EstrategiaGulosa

def calcular_distancia(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def executar_testes_e_plotar():
    ns = list(range(3, 11))
    tempos_bt = []
    tempos_bb = []
    tempos_pd = []
    tempos_eg = []
    estados_bt = []
    estados_bb = []
    estados_pd = []
    estados_eg = []

    for n in ns:
        print(f"Testando com n = {n}...")
        pontos = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n + 1)]
        matriz_dist = [[calcular_distancia(pontos[i], pontos[j]) for j in range(n + 1)] for i in range(n + 1)]

        # Teste Backtracking
        bt = Backtracking(matriz_dist)
        inicio = time.perf_counter()
        _, _, estados = bt.resolver()
        tempos_bt.append(time.perf_counter() - inicio)
        estados_bt.append(estados)

        # Teste Branch and Bound
        bb = BranchAndBound(matriz_dist)
        inicio = time.perf_counter()
        _, _, estados = bb.resolver()
        tempos_bb.append(time.perf_counter() - inicio)
        estados_bb.append(estados)

        # Teste Programacao Dinamica
        pd = ProgramacaoDinamica(matriz_dist)
        inicio = time.perf_counter()
        _, _, estados = pd.resolver()
        tempos_pd.append(time.perf_counter() - inicio)
        estados_pd.append(estados)

        # Teste Estrategia Gulosa
        eg = EstrategiaGulosa(matriz_dist)
        inicio = time.perf_counter()
        _, _, estados = eg.resolver()
        tempos_eg.append(time.perf_counter() - inicio)
        estados_eg.append(estados)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(ns, tempos_bt, label='Backtracking', marker='o', color='red')
    ax1.plot(ns, tempos_bb, label='Branch and Bound', marker='s', color='blue')
    ax1.plot(ns, tempos_pd, label='Programação Dinâmica', marker='^', color='green')
    ax1.plot(ns, tempos_eg, label='Gulosa', marker='d', color='orange')
    ax1.set_title('Tempo de Execução vs Número de Clientes')
    ax1.set_xlabel('Nº de Clientes')
    ax1.set_ylabel('Tempo (segundos)')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(ns, estados_bt, label='Backtracking', marker='o', color='red')
    ax2.plot(ns, estados_bb, label='Branch and Bound', marker='s', color='blue')
    ax2.plot(ns, estados_pd, label='Programação Dinâmica', marker='^', color='green')
    ax2.plot(ns, estados_eg, label='Gulosa', marker='d', color='orange')
    ax2.set_title('Estados Explorados (Nós da Árvore/Passos)')
    ax2.set_xlabel('Nº de Clientes')
    ax2.set_ylabel('Quantidade de Estados')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    os.makedirs("Relatorios", exist_ok=True)
    plt.savefig("Relatorios/grafico_comparativo.png", dpi=150, bbox_inches='tight')
    print("\nGráfico salvo em 'Relatorios/grafico_comparativo.png'")
    plt.show()

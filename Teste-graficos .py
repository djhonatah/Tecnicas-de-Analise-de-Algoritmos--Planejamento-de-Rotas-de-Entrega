import math
import time
import random
import matplotlib.pyplot as plt

# --- FUNÇÕES DO ALGORITMO (SUAS FUNÇÕES) ---

def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Variáveis globais para controle
melhor_distancia = float('inf')
estados_explorados = 0

def backtracking(cliente_atual, visitados, rota_atual, distancia_atual, matriz_dist):
    global melhor_distancia, estados_explorados
    estados_explorados += 1
    n = len(matriz_dist) - 1
    
    if len(visitados) == n:
        distancia_final = distancia_atual + matriz_dist[cliente_atual][0]
        if distancia_final < melhor_distancia:
            melhor_distancia = distancia_final
        return

    for prox_cliente in range(1, n + 1):
        if prox_cliente not in visitados:
            visitados.add(prox_cliente)
            nova_distancia = distancia_atual + matriz_dist[cliente_atual][prox_cliente]
            backtracking(prox_cliente, visitados, rota_atual, nova_distancia, matriz_dist)
            visitados.remove(prox_cliente)

def branch_and_bound(cliente_atual, visitados, rota_atual, distancia_atual, matriz_dist):
    global melhor_distancia, estados_explorados
    estados_explorados += 1
    
    # Poda: A "mágica" do Branch and Bound
    if distancia_atual >= melhor_distancia:
        return
        
    n = len(matriz_dist) - 1
    if len(visitados) == n:
        distancia_final = distancia_atual + matriz_dist[cliente_atual][0]
        if distancia_final < melhor_distancia:
            melhor_distancia = distancia_final
        return

    for prox_cliente in range(1, n + 1):
        if prox_cliente not in visitados:
            visitados.add(prox_cliente)
            nova_distancia = distancia_atual + matriz_dist[cliente_atual][prox_cliente]
            branch_and_bound(prox_cliente, visitados, rota_atual, nova_distancia, matriz_dist)
            visitados.remove(prox_cliente)

# --- FUNÇÃO DE BENCHMARK ---

def executar_testes():
    global melhor_distancia, estados_explorados
    
    ns = list(range(3, 11))  # Testa de 3 a 10 clientes (Backtracking acima de 11 fica muito lento)
    tempos_bt = []
    tempos_bb = []
    estados_bt = []
    estados_bb = []

    for n in ns:
        print(f"Testando com n = {n}...")
        # Gerar pontos aleatórios (depósito + n clientes)
        pontos = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n + 1)]
        matriz_dist = [[calcular_distancia(pontos[i], pontos[j]) for j in range(n+1)] for i in range(n+1)]

        # Teste Backtracking
        melhor_distancia = float('inf')
        estados_explorados = 0
        inicio = time.perf_counter()
        backtracking(0, set(), [], 0.0, matriz_dist)
        tempos_bt.append(time.perf_counter() - inicio)
        estados_bt.append(estados_explorados)

        # Teste Branch and Bound
        melhor_distancia = float('inf')
        estados_explorados = 0
        inicio = time.perf_counter()
        branch_and_bound(0, set(), [], 0.0, matriz_dist)
        tempos_bb.append(time.perf_counter() - inicio)
        estados_bb.append(estados_explorados)

    # --- PLOTAGEM DOS GRÁFICOS ---
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico de Tempo
    ax1.plot(ns, tempos_bt, label='Backtracking', marker='o', color='red')
    ax1.plot(ns, tempos_bb, label='Branch and Bound', marker='s', color='blue')
    ax1.set_title('Tempo de Execução vs Número de Clientes')
    ax1.set_xlabel('Nº de Clientes')
    ax1.set_ylabel('Tempo (segundos)')
    ax1.legend()
    ax1.grid(True)

    # Gráfico de Estados Explorados
    ax2.plot(ns, estados_bt, label='Backtracking', marker='o', color='red')
    ax2.plot(ns, estados_bb, label='Branch and Bound', marker='s', color='blue')
    ax2.set_title('Estados Explorados (Nós da Árvore)')
    ax2.set_xlabel('Nº de Clientes')
    ax2.set_ylabel('Quantidade de Estados')
    ax2.set_yscale('log') # Escala logarítmica para ver a diferença
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    executar_testes()
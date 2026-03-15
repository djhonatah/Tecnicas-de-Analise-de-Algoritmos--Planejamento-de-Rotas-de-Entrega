import math
import time

def calcular_distancia(p1, p2):
    """Calcula a distância Euclidiana entre dois pontos."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

melhor_distancia = float('inf')
melhor_rota = []
estados_explorados = 0

#  ALGORITMO: BACKTRACKING 
def backtracking(cliente_atual, visitados, rota_atual, distancia_atual, matriz_dist):
    global melhor_distancia, melhor_rota, estados_explorados
    estados_explorados += 1
    
    n = len(matriz_dist) - 1
    
    if len(visitados) == n:
        distancia_final = distancia_atual + matriz_dist[cliente_atual][0]
        if distancia_final < melhor_distancia:
            melhor_distancia = distancia_final
            melhor_rota = rota_atual.copy()
        return

    for prox_cliente in range(1, n + 1):
        if prox_cliente not in visitados:
            visitados.add(prox_cliente)
            rota_atual.append(prox_cliente)
            
            nova_distancia = distancia_atual + matriz_dist[cliente_atual][prox_cliente]
            backtracking(prox_cliente, visitados, rota_atual, nova_distancia, matriz_dist)
            
            rota_atual.pop()
            visitados.remove(prox_cliente)


#  ALGORITMO: BRANCH AND BOUND (Ramificar e Podar)
def branch_and_bound(cliente_atual, visitados, rota_atual, distancia_atual, matriz_dist):
    global melhor_distancia, melhor_rota, estados_explorados
    estados_explorados += 1
    
    # Poda: Se a rota parcial já for pior que a melhor encontrada, para de explorar
    if distancia_atual >= melhor_distancia:
        return
        
    n = len(matriz_dist) - 1
    
    if len(visitados) == n:
        distancia_final = distancia_atual + matriz_dist[cliente_atual][0]
        if distancia_final < melhor_distancia:
            melhor_distancia = distancia_final
            melhor_rota = rota_atual.copy()
        return

    for prox_cliente in range(1, n + 1):
        if prox_cliente not in visitados:
            visitados.add(prox_cliente)
            rota_atual.append(prox_cliente)
            
            nova_distancia = distancia_atual + matriz_dist[cliente_atual][prox_cliente]
            branch_and_bound(prox_cliente, visitados, rota_atual, nova_distancia, matriz_dist)
            
            rota_atual.pop()
            visitados.remove(prox_cliente)


def main():
    global melhor_distancia, melhor_rota, estados_explorados
    
    print("=== Planejamento de Rotas de Entrega ===")
    print("1 - Branch and Bound ")
    print("2 - Backtracking Puro ")
    
    # Escolha do algoritmo
    escolha = input("Escolha o algoritmo (digite 1 ou 2): ").strip()
    
    print("\nPerfeito! Agora, a entrada de dados (o 'n' (número de clientes), o depósito e os clientes):")
    
    # Leitura dos dados linha por linha
    n = int(input().strip())
    
    deposito_coords = input().strip().split()
    deposito = (float(deposito_coords[0]), float(deposito_coords[1]))
    
    pontos = [deposito]
    for _ in range(n):
        coords = input().strip().split()
        pontos.append((float(coords[0]), float(coords[1])))
        
    # Construção da Matriz de Distâncias
    total_pontos = n + 1
    matriz_dist = [[0.0] * total_pontos for _ in range(total_pontos)]
    for i in range(total_pontos):
        for j in range(total_pontos):
            matriz_dist[i][j] = calcular_distancia(pontos[i], pontos[j])
            
    # Execução e Medição de Tempo
    inicio_tempo = time.perf_counter()
    
    if escolha == "2":
        nome_algo = "Backtracking Puro"
        backtracking(0, set(), [], 0.0, matriz_dist)
    else:
        nome_algo = "Branch and Bound"
        branch_and_bound(0, set(), [], 0.0, matriz_dist)
        
    fim_tempo = time.perf_counter()
    tempo_execucao = fim_tempo - inicio_tempo
    
    # ---------------------------------------------------------
    # SAÍDA
    # ---------------------------------------------------------
    
    print("\n" + "="*30)
    print("SAÍDA DO PROBLEMA:")
    print("="*30)
    
    print(f"{melhor_distancia:.1f}")
    
    sequencia = ["0"] + [str(c) for c in melhor_rota] + ["0"]
    print(" ".join(sequencia))
    
    # ---------------------------------------------------------
    # AVALIAÇÕES 
    # ---------------------------------------------------------
    
    print("\n" + "="*30)
    print("AVALIAÇÕES RECOMENDADAS:")
    print("="*30)
    print(f"Algoritmo utilizado.......: {nome_algo}")
    print(f"Tempo de execução.........: {tempo_execucao:.6f} segundos")
    print(f"Custo total (precisão)....: {melhor_distancia:.6f}")
    print(f"Número de estados explorados: {estados_explorados}")

if __name__ == "__main__":
    main()
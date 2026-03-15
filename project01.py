import math
import time

# ================= VARIÁVEIS GLOBAIS =================

melhor_distancia = float('inf')
melhor_rota = []
estados_explorados = 0
relatorios = []


# ================= FUNÇÕES AUXILIARES =================

def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# ================= ALGORITMOS =================

def backtracking(cliente_atual, visitados, rota_atual, distancia_atual, matriz_dist):
    global melhor_distancia, melhor_rota, estados_explorados
    estados_explorados += 1

    n = len(matriz_dist) - 1

    if len(visitados) == n:
        d = distancia_atual + matriz_dist[cliente_atual][0]
        if d < melhor_distancia:
            melhor_distancia = d
            melhor_rota = rota_atual.copy()
        return

    for prox in range(1, n + 1):
        if prox not in visitados:
            visitados.add(prox)
            rota_atual.append(prox)
            backtracking(
                prox,
                visitados,
                rota_atual,
                distancia_atual + matriz_dist[cliente_atual][prox],
                matriz_dist
            )
            rota_atual.pop()
            visitados.remove(prox)


def branch_and_bound(cliente_atual, visitados, rota_atual, distancia_atual, matriz_dist):
    global melhor_distancia, melhor_rota, estados_explorados
    estados_explorados += 1

    if distancia_atual >= melhor_distancia:
        return

    n = len(matriz_dist) - 1

    if len(visitados) == n:
        d = distancia_atual + matriz_dist[cliente_atual][0]
        if d < melhor_distancia:
            melhor_distancia = d
            melhor_rota = rota_atual.copy()
        return

    for prox in range(1, n + 1):
        if prox not in visitados:
            visitados.add(prox)
            rota_atual.append(prox)
            branch_and_bound(
                prox,
                visitados,
                rota_atual,
                distancia_atual + matriz_dist[cliente_atual][prox],
                matriz_dist
            )
            rota_atual.pop()
            visitados.remove(prox)


# ================= RELATÓRIOS =================

def imprimir_relatorios():
    if not relatorios:
        print("\nNenhum teste registrado.")
        return

    print("\n========= RELATÓRIO GERAL =========")
    for i, r in enumerate(relatorios, 1):
        print(f"\nTeste #{i}")
        print(f"Algoritmo : {r['algoritmo']}")
        print(f"Clientes  : {r['n']}")
        print(f"Status    : {r['status']}")
        print(f"Tempo     : {r['tempo']:.6f} s")
        print(f"Estados   : {r['estados']}")

        if r["status"] == "Sucesso":
            print(f"Distância : {r['distancia']:.6f}")
            print(f"Rota      : {r['rota']}")
        else:
            print(f"Erro      : {r['erro']}")


def salvar_relatorios_txt(nome):
    if not relatorios:
        print("\nNenhum teste para salvar.")
        return

    with open(nome, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE TESTES - TSP\n")
        f.write("=" * 60 + "\n\n")

        for i, r in enumerate(relatorios, 1):
            f.write(f"Teste #{i}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Algoritmo : {r['algoritmo']}\n")
            f.write(f"Clientes  : {r['n']}\n")
            f.write(f"Status    : {r['status']}\n")
            f.write(f"Tempo     : {r['tempo']:.6f} s\n")
            f.write(f"Estados   : {r['estados']}\n")

            if r["status"] == "Sucesso":
                f.write(f"Distância : {r['distancia']:.6f}\n")
                f.write(f"Rota      : {r['rota']}\n")
            else:
                f.write(f"Erro      : {r['erro']}\n")

            f.write("\n")

    print(f"\nRelatório salvo em '{nome}'")


# ================= MAIN =================

def main():
    global melhor_distancia, melhor_rota, estados_explorados

    while True:
        try:
            melhor_distancia = float('inf')
            melhor_rota = []
            estados_explorados = 0

            print("\n=== Planejamento de Rotas de Entrega ===")
            print("1 - Executar teste")
            print("2 - Ver relatório")
            print("3 - Salvar relatório em arquivo")
            print("0 - Sair")

            op = input("Opção: ").strip()

            if op == "0":
                print("Encerrando aplicação...")
                break

            if op == "2":
                imprimir_relatorios()
                continue

            if op == "3":
                nome = input("Nome do arquivo (.txt): ").strip()
                salvar_relatorios_txt(nome)
                continue

            if op != "1":
                print("Opção inválida.")
                continue

            # ===== EXECUÇÃO DO TESTE =====
            try:
                print("\n1 - Branch and Bound")
                print("2 - Backtracking")
                alg = input("Algoritmo: ").strip()

                if alg not in ("1", "2"):
                    raise ValueError("Algoritmo inválido")

                n = int(input("Número de clientes: ").strip())
                if n <= 0:
                    raise ValueError("Número de clientes inválido")

                xd, yd = map(float, input("Depósito (x y): ").split())
                pontos = [(xd, yd)]

                for i in range(n):
                    x, y = map(float, input(f"Cliente {i+1} (x y): ").split())
                    pontos.append((x, y))

                total = n + 1
                matriz = [[0.0] * total for _ in range(total)]
                for i in range(total):
                    for j in range(total):
                        matriz[i][j] = calcular_distancia(pontos[i], pontos[j])

                inicio = time.perf_counter()

                if alg == "2":
                    nome_alg = "Backtracking"
                    backtracking(0, set(), [], 0.0, matriz)
                else:
                    nome_alg = "Branch and Bound"
                    branch_and_bound(0, set(), [], 0.0, matriz)

                tempo = time.perf_counter() - inicio
                rota_str = "0 " + " ".join(map(str, melhor_rota)) + " 0"

                print(f"\nDistância: {melhor_distancia:.6f}")
                print(f"Rota     : {rota_str}")

                relatorios.append({
                    "algoritmo": nome_alg,
                    "n": n,
                    "distancia": melhor_distancia,
                    "rota": rota_str,
                    "tempo": tempo,
                    "estados": estados_explorados,
                    "status": "Sucesso"
                })

            except Exception as e:
                relatorios.append({
                    "algoritmo": "Indefinido",
                    "n": None,
                    "distancia": None,
                    "rota": None,
                    "tempo": 0.0,
                    "estados": estados_explorados,
                    "status": "Falhou",
                    "erro": str(e)
                })
                print("Erro no teste. Registrado no relatório.")
                continue

        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Retornando ao menu...")
            continue
# ================= EXECUÇÃO =================

if __name__ == "__main__":
    main()
# Técnicas de Análise de Algoritmos — Planejamento de Rotas de Entrega

Este repositório contém uma implementação didática de algoritmos de otimização
para o problema do Caixeiro Viajante (TSP) aplicado ao planejamento de rotas
de entrega. O código foi organizado em módulos para facilitar manutenção e
reuso.

## Estrutura do projeto

- `main.py` — Programa principal (menu) que orquestra o sistema.
- `README.md` — Este arquivo com descrição e instruções.

- `Algoritmos/`
	- `Backtracking.py` — Classe `Backtracking` que implementa a solução por
		backtracking. Uso: instanciar com a matriz de distâncias e chamar
		`resolver()`.
	- `BranchAndBound.py` — Classe `BranchAndBound` que implementa branch-and-bound
		com poda por bound simples. Uso: instanciar com a matriz de distâncias e
		chamar `resolver()`.

- `Controller/`
	- `relatorioController.py` — Funções para gerenciar relatórios em memória,
		imprimir no console e salvar em arquivo texto. Funções principais:
		`adicionar_relatorio(dict)`, `imprimir_relatorios()`,
		`salvar_relatorios_txt(nome_arquivo)`.
	- `graficoController.py` — Função `executar_testes_e_plotar()` que gera
		benchmarks comparando tempo e estados explorados dos algoritmos e plota
		gráficos (usa `matplotlib`).

- `IO/`
	- `leitor_entrada.py` — Funções de leitura interativa do usuário:
		`ler_dados_teste()` (lê opção de algoritmo, número de clientes e coordenadas),
		`ler_opcao_menu()`, `ler_nome_arquivo()`.
	- `escritor_saida.py` — Funções para imprimir no console: `imprimir_menu()`,
		`imprimir_resultado(distancia, rota)` e `imprimir_mensagem(msg)`.

## Formato esperado

- Matriz de distâncias: uma lista de listas `matriz[i][j]` com distância entre o
	depósito (índice 0) e clientes (1..n). O construtor das classes espera essa
	matriz pronta.
- Retorno de `resolver()`: tupla `(melhor_distancia, melhor_rota, estados_explorados)`.
	- `melhor_rota` é uma lista de índices (inclui o depósito `0` quando aplicável).

## Como executar

1. Crie e ative um ambiente virtual (opcional, recomendado):

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Instale dependências (somente `matplotlib` é requerida para plots):

```powershell
pip install matplotlib
```

3. Rode a aplicação principal:

```powershell
python main.py
```

4. Menu disponível (executado por `project01.py`):
- `1 - Executar teste`: solicita algoritmo, número de clientes e coordenadas;
	executa o algoritmo escolhido e registra o relatório.
- `2 - Ver relatório`: imprime relatórios salvos em memória.
- `3 - Salvar relatório em arquivo`: salva relatórios no caminho informado.
- `4 - Gerar gráficos comparativos`: executa benchmarks e mostra gráficos.
- `0 - Sair`.

## Exemplos de uso programático

Se preferir usar os algoritmos a partir de outro script, siga este padrão:

```python
from Algoritmos.Backtracking import Backtracking
from Algoritmos.BranchAndBound import BranchAndBound

# matriz é uma lista de listas de distâncias com depósito no índice 0
solver = Backtracking(matriz)
dist, rota, estados = solver.resolver()
```

Para gerar gráficos programaticamente, chame:

```python
from Controller.graficoController import executar_testes_e_plotar
executar_testes_e_plotar()
```

Para adicionar/visualizar relatórios:

```python
from Controller import relatorioController
relatorioController.adicionar_relatorio({...})
relatorioController.imprimir_relatorios()
```

## Observações

- O código tem intenção didática; para instâncias grandes (n > 11) o
	backtracking ficará muito lento.
- Estruture a matriz de distâncias corretamente (depósito no índice `0`).
- Testes e gráficos usam coordenadas geradas aleatoriamente por padrão.

Se quiser, posso adicionar um `requirements.txt`, exemplos de matrizes de teste
ou scripts automatizados para rodar benchmarks em lote.

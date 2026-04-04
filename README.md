# Técnicas de Análise de Algoritmos — Planejamento de Rotas de Entrega

Projeto didático que implementa várias estratégias para o problema do
Caixeiro Viajante (TSP) aplicado ao planejamento de rotas de entrega. O
código está modularizado para facilitar experimentos, geração de relatórios
e criação de gráficos comparativos.

## Estrutura do projeto

- `main.py` — Programa principal com menu interativo que orquestra execução
	de testes, relatórios e gráficos.
- `README.md` — Documentação (este arquivo).

- `Algoritmos/` — Implementações das estratégias para TSP:
	- `Backtracking.py` — classe `Backtracking`: busca exaustiva (DFS) com
		poda baseada na melhor solução atual. Uso: instanciar com a matriz de
		distâncias e chamar `resolver()` que retorna `(melhor_distancia, melhor_rota, estados_explorados)`.
	- `BranchAndBound.py` — classe `BranchAndBound`: implementação similar ao
		backtracking com poda simples (ver observações sobre heurísticas abaixo).
	- `ProgramacaoDinamica.py` — classe `ProgramacaoDinamica`: implementação do
		algoritmo de programação dinâmica (bitmask) para TSP. Retorna a melhor
		distância, a rota reconstruída e o número de estados explorados.
	- `EstrategiaGulosa.py` — classe `EstrategiaGulosa`: heurística gulosa que
		constrói uma rota escolhendo o cliente mais próximo não visitado.

- `Controller/` — Controle de relatórios e geração de gráficos:
	- `relatorioController.py` — mantém relatórios em memória, imprime e salva
		em arquivo texto (`adicionar_relatorio`, `imprimir_relatorios`, `salvar_relatorios_txt`).
	- `graficoController.py` — executa benchmarks (vários `n`) e plota tempo x n
		e estados explorados x n (usa `matplotlib`).

- `IO/` — Entrada e saída de usuário:
	- `leitor_entrada.py` — funções para ler opção do menu, parâmetros de teste
		(algoritmo, número de clientes e coordenadas) e nome de arquivo.
	- `escritor_saida.py` — funções para imprimir o menu, resultados e mensagens.

- `Relatorios/` — Pasta onde relatórios podem ser salvos (texto).
- `Documento/` — Documentação e análises comparativas.



## Como executar

1. Crie e ative um ambiente virtual (opcional):

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependência para gráficos (se quiser gerar plots):

```powershell
pip install matplotlib
```

3. Rodar o programa:

```powershell
python main.py
```

4. Menu disponível (executado por `main.py`):
- `1 - Executar teste`: solicita algoritmo, número de clientes e coordenadas;
	executa o algoritmo escolhido e registra o relatório.
- `2 - Ver relatório`: imprime relatórios salvos em memória.
- `3 - Salvar relatório em arquivo`: salva relatórios no formato .txt na pasta `Relatorios`.
- `4 - Gerar gráficos comparativos`: executa benchmarks e mostra gráficos.
- `0 - Sair`.



## Observações

- O código tem intenção didática; para instâncias grandes (n > 11) o
	backtracking ficará muito lento.
- Estruture a matriz de distâncias corretamente (depósito no índice `0`).
- Testes e gráficos usam coordenadas geradas aleatoriamente por padrão.


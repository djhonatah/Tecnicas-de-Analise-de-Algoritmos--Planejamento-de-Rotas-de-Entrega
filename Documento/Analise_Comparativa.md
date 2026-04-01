# Análise Comparativa de Estratégias Algorítmicas: Planejamento de Rotas (TSP)

Este relatório compila a análise crítica solicitada comparando as quatro táticas implementadas para resolver o Planejamento de Rotas (o clássico Caixeiro Viajante - TSP) em nosso simulador.

## 1. Complexidade Assintótica (Teórica)

| Algoritmo | Complexidade de Tempo | Complexidade de Espaço / Memória |
| :--- | :--- | :--- |
| **Backtracking** | $O(N!)$ | $O(N)$ (Profundidade da raiz à folha) |
| **Branch and Bound** | $O(N!)$ no pior caso | $O(N)$ (Uso de recursão DFS) |
| **Programação Dinâmica** | $O(N^2 \cdot 2^N)$ | $O(N \cdot 2^N)$ (Armazenamento Subproblemas) |
| **Estratégia Gulosa** | $O(N^2)$ | $O(N)$ (Para guardar a rota/lista de visitados) |

*Nota técnica:* B&B no pior caso (quando nenhuma poda ocorre) avalia a mesma árvore permutacional inteira do Backtracking. O algoritmo Dinâmico (Held-Karp) reduz o modelo combinatório em custo algorítmico drástico ao permutar as viagens da ordem fatorial por conta dos subproblemas sobrepostos superando o cálculo na mesma sub-árvore. 

## 2. Tempo de Execução (Empírico)

Testes rodados usando a função de Plot do `graficoController` demonstraram na prática as distinções teóricas apresentadas acima:

*   **Estratégia Gulosa:** Como sua natureza é iterativa e local (escolhe a melhor à frente, a ignora em retrospectiva), o tempo é computacionalmente nulo nos gráficos frente a escala milimétrica do MatPlotLib (< 0.001 segundos mesmo para N=10).
*   **Programação Dinâmica:** Mantém-se de forma estável e muito veloz frente a N=10 gerando em poucas dezenas de milissegundos.
*   **Branch and Bound:** Notavelmente mais rápido que Backtracking devido aos cortes do limitante (Bound), mas eventualmente começa a espelhar uma curva de ascensão rápida quando N atinge \~10-12 pois as podas já não escalam perfeitamente sem decência exponencial.
*   **Backtracking:** O método escala o gráfico terrivelmente superando um segundo em N=10 rapidamente indo a tempo inviável para $N \ge 12$.

## 3. Uso de Memória

*   Crescimento assustador apenas se dá na **Programação Dinâmica (PD)**. Em PD armazenamos, a cada estado `(nó_atual, máscara_visitados)`, todos os resultados do subproblema de forma a nunca precisar re-calcular (Memoização). Devido à máscara de bits poder gerar até $2^N$ combinações por número de nós, esta abordagem consome Memória Exponencial (explosão de estado). 
*   **Backtracking, B&B e Guloso** detêm vantagens inquestionáveis de eficiência sistêmica de memória em relação à PD pois demandam apenas uma tabela fixa ($O(N)$). B&B e Backtracking são varreduras de profundidade DFS em árvores.

## 4. Qualidade da Solução (Ótima vs Aproximada)

*   **Algoritmos Exatos (Backtracking, B&B, PD):** Todos eles validam, através da natureza global combinatória, a solução com **100% de garantia de Otimidade**. Eles obrigatoriamente retornarão a melhor rota possível sempre (menor distância).
*   **Algoritmo Aproximado (Estratégia Gulosa):** O processo local e sem voltar atrás em decisões passadas (sem retrospecto), frequentemente provê rotas sub-ótimas. Apesar de muito mais rápido, a falta de horizonte e a possibilidade heurística de ficar engarrafado de realizar saltos pioress no fim geram saídas **não otimizadas**, mas na média um nível viável de aproximação se o recurso tempo for restrito limitador.

## 5. Escalabilidade

*   **Gulosa:** Excelentemente escalável até $N > 10,000$ nós no dia-a-dia moderno.
*   **PD:** Limitadamente escalável até cerca de uso em \~25 clientes. Após isto, necessitaria-se de dezenas a centenas de GBs de memória RAM na máquina (apesar de bater limites drásticos de tempo perante O($N^2 2^N$)).
*   **B&B:** Pode conseguir respostas razoáveis sob $N \le 20\sim30$ no máximo para tempos curtos se os limites iniciais funcionarem fortes. 
*   **Backtracking:** Terrível para escalar e obsoleto sem cortes para um Problema NP-Difícil desse grau > 12.

## 6. Métricas de Qualidade

Foram registradas ao plotar os gráficos de comportamento os "Estados Explorados". Observou-se:
- *Backtracking* gera milhões de estados.
- *Branch and Bound* retem em média de $40\%$ a $80\%$ este número em cortes logarítmicos notáveis usando a função limitante inicial `distancia_atual > melhor_distancia`.
- *Programação Dinâmica* diminui drasticamente, focando as computações únicas geradoras da curva exponencial ($N \cdot 2^{N}$).

## 7. Podas no Espaço de Busca e Justificativas (B&B e PD)

> **Podas Efetuadas (Branch & Bound):**
> A regra de corte é `if distancia_atual >= self.melhor_distancia: return`.
> A justificativa realça a técnica porque se o viajante já andou pela cidade A, B, C gastando $D=200km$, mas previamente foi encontrada uma rota por outra região onde a viagem completa usou $180km$, é **matematicamente impossível** a rota atual da árvore se tornar a menor. Abandona-se aquele galho inteiramente, poupando centenas de nós descendentes do sub-nível de espaço temporal $O(K!)$ não mapeado.

> **Justificativa da Otimização do Espaço (Programação Dinâmica):**
> PD utiliza "Subestrutura Ótima". O princípio alega que a menor rota indo de uma cidade A para o grupo final $\{X, Y, Z\}$ é a mesma não importa por onde fomos *antes* de chegar em A. Quando guardamos essas minimizações parciais nos dicionários, nós colapsamos todos os "galhos" com os mesmos remanescentes no problema de TSP a um tempo constante $O(1)$ de leitura ao invés de recalculo constante, alterando a complexidade da base fatorial de enumeração total $O(N!)$ para $O(N^2 2^N)$.

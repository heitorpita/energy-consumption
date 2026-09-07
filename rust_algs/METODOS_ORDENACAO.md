# Duas versões de cada método de ordenação — comparação e consumo energético

Implementação em Rust de duas versões de cada um dos três métodos de
ordenação, medidas em hardware real com RAPL (`perf stat -a -e
power/energy-pkg/`), nas mesmas entradas embaralhadas do experimento em
Python (`alg_ordenacao/entrada_{10,50,100}.in`, com 10.000, 50.000 e 100.000
elementos).

Os seis programas compartilham exatamente o mesmo `main()` (lê `n` e `n`
inteiros de stdin, ordena, imprime) — a única diferença entre eles é a função
de ordenação, para que qualquer diferença medida de tempo/energia seja
atribuível ao algoritmo e não ao resto do código.

## Complexidade

| Programa | Método | Melhor caso | Caso médio | Pior caso |
|---|---|---|---|---|
| `bubble_sort_v1.rs` | Flutuação, ingênuo | O(n²) | O(n²) | O(n²) |
| `bubble_sort_v2.rs` | Flutuação, com parada e encolhimento | O(n) | O(n²) | O(n²) |
| `insertion_sort_v1.rs` | Inserção com `swap` | O(n) | O(n²) | O(n²) |
| `insertion_sort_v2.rs` | Inserção com deslocamento | O(n) | O(n²) | O(n²) |
| `selection_sort_v1.rs` | Seleção linear | O(n²) | O(n²) | O(n²) |
| `selection_sort_v2.rs` | Seleção com heap (**heap sort**) | O(n log n) | O(n log n) | O(n log n) |

## Ordenação por Flutuação (Bubble Sort)

**v1** executa sempre as `n` passadas completas, comparando todos os pares
vizinhos em cada uma. Ele não tem como perceber que o vetor já ficou
ordenado no meio do caminho: continua fazendo passadas inteiras que não
mudam mais nada.

**v2** guarda a posição da última troca de cada passada (`ultima`). Tudo o
que está depois dessa posição já está garantidamente ordenado, então a
passada seguinte só varre até ali. Como consequência natural, se uma passada
não faz nenhuma troca, o alcance cai a zero e o algoritmo para.

**Por que gasta menos energia:** cada comparação e cada troca são instruções
executadas pela CPU e acessos à memória — ambos consomem energia. A v2 corta
duas fontes de desperdício ao mesmo tempo: as passadas finais que já não
mudam nada, e o trecho final de cada passada que já está ordenado. Menos
instruções executadas para o mesmo resultado significa menos tempo com a CPU
ativa e, portanto, menos Joules.

## Ordenação por Inserção (Insertion Sort)

Ambas fazem a mesma coisa conceitualmente: pegam cada elemento e o
"empurram" para trás até achar sua posição no trecho já ordenado. A
diferença é **como** esse empurrão é feito.

**v1** usa `v.swap(j-1, j)` a cada posição andada — uma troca completa entre
dois elementos, que custa duas leituras e **duas escritas** por posição.

**v2** tira o elemento do vetor uma vez (`let key = v[i]`), desloca os
maiores uma casa para a direita (`v[j] = v[j-1]`, **uma escrita** por
posição) e grava a chave uma única vez na posição final.

**Por que gasta menos energia:** para o mesmo número de comparações e o mesmo
número de posições andadas, a v2 faz aproximadamente **metade das escritas
em memória**. Escrita custa mais que leitura (envolve invalidação de linha de
cache e, eventualmente, tráfego até a RAM), e movimentação de dados é uma
das operações mais caras em energia num processador moderno — bem mais cara
que a comparação aritmética em si. A complexidade assintótica é idêntica
(O(n²)); o ganho vem inteiramente da constante.

## Ordenação por Seleção (Selection Sort)

**v1** é a versão clássica: para cada posição `i`, varre todo o resto do
vetor procurando o menor elemento e o coloca em `i`. Não existe parada
antecipada possível — mesmo que o vetor já esteja ordenado, é preciso varrer
o restante inteiro para *provar* que o mínimo é aquele. Por isso é O(n²) em
todos os casos. Em compensação, faz no máximo `n` trocas no total.

**v2 é o heap sort**, que é exatamente a mesma ideia de "selecionar
repetidamente o extremo", só que com uma estrutura de dados melhor para essa
seleção. Em vez de varrer linearmente em O(n) para achar o maior, o vetor é
primeiro transformado num heap máximo (`build-heap`, O(n)) e depois o maior
é extraído da raiz `n` vezes, com o heap sendo reorganizado em O(log n) a
cada extração (`sift_down`). Total: **O(n log n)** em todos os casos.

**Por que gasta menos energia:** aqui a diferença não é de constante, é de
**classe de complexidade**. Para n=100.000, a seleção linear faz cerca de
5 bilhões de comparações (n²/2), enquanto o heap sort faz da ordem de
1,7 milhão (n log₂n) — três ordens de grandeza a menos de trabalho. Como a
economia é proporcional a n/log n, ela *cresce* conforme a entrada aumenta,
diferente das otimizações de constante dos outros dois métodos, cujo ganho
percentual fica mais ou menos estável.

## Resultados medidos (1 repetição, RAPL `power/energy-pkg/`)

Energia em Joules; tempo de execução em segundos.

| Programa | n=10.000 | n=50.000 | n=100.000 |
|---|---|---|---|
| `bubble_sort_v1` | 1,31 J (0,18 s) | 39,10 J (5,54 s) | 147,95 J (22,12 s) |
| `bubble_sort_v2` | 0,80 J (0,12 s) | 27,24 J (3,95 s) | 105,10 J (15,99 s) |
| `insertion_sort_v1` | 0,14 J (0,023 s) | 3,68 J (0,54 s) | 14,01 J (2,12 s) |
| `insertion_sort_v2` | 0,14 J (0,017 s) | 2,46 J (0,35 s) | 8,64 J (1,32 s) |
| `selection_sort_v1` | 0,45 J (0,060 s) | 9,27 J (1,37 s) | 33,98 J (5,30 s) |
| `selection_sort_v2` | 0,02 J (0,003 s) | 0,10 J (0,013 s) | 0,16 J (0,025 s) |

Economia de energia da v2 sobre a v1, em n=100.000:

- **Flutuação:** 147,95 J → 105,10 J = **29% menos energia**
- **Inserção:** 14,01 J → 8,64 J = **38% menos energia**
- **Seleção:** 33,98 J → 0,16 J = **99,5% menos energia** (~212x)

## Por que essas diferenças levam a menor consumo

A potência medida ficou praticamente constante em todas as execuções, entre
**6,4 W e 8,3 W**, independentemente do algoritmo. Isso é o ponto central:
como a CPU consome aproximadamente a mesma potência enquanto trabalha, e
energia = potência × tempo, **a energia gasta é essencialmente proporcional
ao trabalho total realizado**. Nenhum dos algoritmos "gasta menos por
instrução" — eles gastam menos porque executam menos instruções.

Isso divide as otimizações em duas categorias, com potenciais bem
diferentes:

1. **Reduzir a constante** (bubble v2, insertion v2): eliminar comparações
   redundantes, passadas inúteis e escritas desnecessárias. O ganho medido
   ficou na faixa de 29% a 38% e é aproximadamente estável conforme n cresce,
   porque a complexidade continua a mesma.

2. **Reduzir a classe de complexidade** (heap sort): trocar O(n²) por
   O(n log n). O ganho foi de 99,5% e — mais importante — *aumenta* com o
   tamanho da entrada: em n=10.000 o heap sort gastou 22x menos energia que
   a seleção linear, em n=50.000 foram 93x, e em n=100.000 chegou a 212x.

Um detalhe que reforça o argumento: `selection_sort_v1` e `bubble_sort_v1`
são ambos O(n²), mas a seleção gastou **4,4x menos energia** (33,98 J contra
147,95 J em n=100.000). Os dois fazem o mesmo número de comparações; a
diferença é que o bubble sort faz O(n²) trocas enquanto a seleção faz no
máximo `n`. Ou seja: dentro da mesma complexidade, **movimentação de dados é
o que domina o custo energético**.

## Ressalva sobre a medição

Em n=10.000 as duas versões de inserção registraram o mesmo valor (0,14 J),
apesar de a v2 ter sido 28% mais rápida (0,017 s contra 0,023 s). Nessa
escala a execução é curta demais para a resolução do contador RAPL, e o
ruído domina a diferença real. Isso não invalida os números maiores, mas
indica que conclusões sobre n=10.000 devem se apoiar em várias repetições —
a bateria completa pode ser rodada com `./run_benchmarks_rust.sh 2 20`,
acumulando no mesmo `resultados_rust.csv`.

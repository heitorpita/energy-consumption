# Conclusões — Consumo de Energia em Algoritmos de Ordenação

O experimento comparou quatro implementações (bubble sort, bubble sort melhorado,
selection sort e selection sort melhorado) em três tamanhos de entrada (10.000,
50.000 e 100.000 elementos), com 10 repetições de cada combinação, medindo energia
via perf (`power/energy-pkg/`) em Python.

## Os 4 algoritmos e o que muda entre eles

**bubble_sort (normal):** faz sempre n-1 passadas completas pelo vetor, e em cada
passada compara todo par de elementos vizinhos, trocando os dois de lugar
quando estão fora de ordem. Ele não sabe se o vetor já ficou ordenado no meio
do processo — continua rodando o total de passadas previsto de qualquer
forma. É o motivo do desperdício: comparações e passadas que já não mudam
mais nada continuam sendo feitas.

**bubble_sort_melhorado:** guarda, em cada passada, a posição da última troca
que foi feita (variável `ultima` no código). Na passada seguinte, ele só
varre o vetor até essa posição, porque tudo que vem depois do último swap já
está garantidamente ordenado e não precisa ser conferido de novo. Como
consequência, se numa passada não acontece nenhuma troca, o alcance da
varredura cai pra zero e o algoritmo para ali — ou seja, ele também para
mais cedo quando o vetor já está ordenado. Mas o ganho principal não é só
"parar no final": é o alcance de cada passada encolher progressivamente
conforme o final do vetor vai se ordenando, mesmo antes de tudo estar
pronto.

**selection_sort (normal):** pra cada posição i do vetor, percorre todo o
restante (do i+1 até o fim) procurando o menor elemento, e só então troca
esse menor pra posição i. Diferente do bubble sort, ele faz no máximo uma
troca por passada (não fica trocando pares repetidamente). Mas ele sempre
varre o restante inteiro do vetor pra ter certeza de que achou o menor,
então não tem como parar mais cedo mesmo se o vetor já estiver ordenado —
por isso a versão normal do selection sort não tem "gordura" óbvia pra
cortar, diferente do bubble sort.

**selection_sort_melhorado:** em vez de procurar só o menor elemento a cada
passada, procura o menor E o maior ao mesmo tempo, no mesmo laço interno
(é a técnica de "min-max selection sort"). O menor vai pro começo do trecho
ainda não ordenado e o maior vai pro final desse mesmo trecho, na mesma
passada. Isso corta o número de passadas externas pela metade (de n para
aproximadamente n/2), porque cada passada resolve duas posições do vetor de
uma vez (uma na ponta inicial, outra na ponta final) em vez de uma só.

**Por que bubble perde pra selection mesmo otimizado:** a família bubble sort
troca elementos vizinhos repetidamente até tudo se acomodar no lugar certo,
o que gera muito mais operações de troca no total. A família selection sort
localiza o elemento certo primeiro (comparando, sem trocar) e troca só uma
vez por passada pra colocá-lo na posição final. Menos trocas de memória e
menos operações redundantes de um jeito estrutural — é por isso que mesmo o
bubble_sort_melhorado, com sua otimização, ainda gasta mais energia que o
selection_sort sem otimização nenhuma.

## Como os cálculos foram feitos

**Média de energia** (e das outras colunas): pra cada combinação de algoritmo e
tamanho de entrada (ex.: bubble_sort com n=10.000), existem 10 valores de
`energia_j` no `resultados.csv`, um por repetição. A média é a soma desses 10
valores dividida por 10 (média aritmética simples). O mesmo cálculo foi
repetido, coluna por coluna, pra `tempo_exe_s`, `tempo_cpu_s`, `potencia_exe_w` e
`potencia_cpu_w` — sempre usando os 10 valores daquela mesma combinação
algoritmo+n. Essas médias foram acrescentadas no final do `resultados.csv`,
numa seção separada por uma linha em branco, com "media" no lugar do número
da repetição.

**Percentual de economia de energia** (ex.: "bolha->melhorado: 32,5%"): não veio
de um cálculo linha a linha, e sim das médias de energia já calculadas acima.
A fórmula usada foi `(1 - media_melhorado / media_original) * 100`, comparando
sempre o mesmo tamanho de entrada (ex.: media de bubble_sort_melhorado em
10.000 contra a media de bubble_sort em 10.000). Os dados necessários foram
só essas duas médias de energia, uma por versão do algoritmo, no mesmo n.

**Razão bubble_sort_melhorado vs selection_sort** (ex.: "2,03x" em 10.000):
mesma lógica, mas dividindo uma média pela outra em vez de calcular
percentual: `media_bubble_sort_melhorado / media_selection_sort`, pro mesmo n.
Precisa das médias de energia dos dois algoritmos, no mesmo tamanho.

**Faixa de potência** (~6,3W a ~7,2W): potência não foi calculada aqui, ela já
vem pronta em cada linha do `resultados.csv` (`potencia_exe_w = energia_j /
tempo_exe_s`, calculado pelo `run_repeticoes.sh` no momento da coleta). O que eu
fiz foi só olhar o menor e o maior valor de `potencia_exe_w` entre as 120
execuções brutas (10 repetições x 4 algoritmos x 3 tamanhos) pra descrever a
faixa observada. Quando essa mesma verificação é feita só em cima das 12
médias (uma por combinação algoritmo+n), a faixa fica ainda mais estreita,
entre 6,49W e 6,83W — reforçando que a potência varia pouco entre execuções
individuais e ainda menos quando se olha a média de cada combinação.

**Crescimento de energia com o tamanho da entrada** (ex.: "~107x" pro bubble
sort): razão entre a média de energia em n=100.000 e a média de energia em
n=10.000, pro mesmo algoritmo: `media_energia(n=100000) / media_energia(n=10000)`.
Só precisa das médias de energia nos dois tamanhos extremos testados.

## Médias de energia (10 repetições, em Joules)

| Algoritmo                 | 10.000 | 50.000  | 100.000  |
|----------------------------|-------:|--------:|---------:|
| bubble_sort                 | 114 J  | 2.926 J | 12.247 J |
| bubble_sort_melhorado        | 77 J   | 1.951 J | 7.675 J  |
| selection_sort               | 38 J   | 893 J   | 3.775 J  |
| selection_sort_melhorado     | 32 J   | 771 J   | 3.043 J  |

## O que os números mostram

O bubble sort é, sem surpresa, o mais caro dos quatro em qualquer tamanho de
entrada. Já era esperado, dado que ele faz muito mais trocas e comparações
redundantes que o selection sort pra chegar no mesmo resultado.

A otimização aplicada no bubble sort (a versão "melhorado") entrega uma economia
de energia bem relevante e consistente: em torno de 32-37% a menos de energia
gasta, dependendo do tamanho da entrada, e a economia cresce um pouco conforme n
aumenta (32,5% em 10k, chegando a 37,3% em 100k). Isso sugere que a otimização
não é só um ganho fixo, ela escala bem — provavelmente porque reduz o número de
iterações desnecessárias de forma proporcional ao tamanho do vetor (ex.: parar
cedo quando já está ordenado).

No selection sort, a versão melhorada também economiza energia, mas menos: entre
14% e 19%. Faz sentido, já que o selection sort original é estruturalmente mais
enxuto que o bubble sort original, então sobra menos gordura pra cortar.

Mesmo depois de otimizado, o bubble sort continua perdendo pro selection sort sem
otimização nenhuma. Em todos os tamanhos testados, o bubble_sort_melhorado gasta
cerca de 2 a 2,2x mais energia que o selection_sort puro. Ou seja, a escolha do
algoritmo base pesa mais do que a otimização aplicada em cima dele — não adianta
otimizar o algoritmo errado.

O selection_sort_melhorado foi o mais eficiente em energia nos três tamanhos,
como esperado por combinar o algoritmo mais enxuto com a otimização.

## Potência x tempo

Um ponto que chamou atenção: a potência média (energia dividida pelo tempo de
execução) ficou sempre numa faixa estreita, entre ~6,3W e ~7,2W, independente do
algoritmo ou do tamanho da entrada. Isso indica que a CPU trabalha com uma
potência praticamente constante durante essas execuções (o processo é
CPU-bound o tempo todo, sem períodos de espera/ociosidade que reduziriam o
consumo médio). Na prática, isso quer dizer que o fator que realmente decide o
gasto de energia aqui não é "quanto a CPU puxa de potência", e sim quanto tempo
o algoritmo leva pra terminar. Energia e tempo de execução andam praticamente
juntos nesse experimento — reduzir o tempo de execução é, na prática, a mesma
coisa que reduzir a energia gasta.

## Crescimento com o tamanho da entrada

Todos os quatro algoritmos são O(n²), e os dados confirmam isso na prática: indo
de 10.000 para 100.000 elementos (10x o tamanho), o consumo de energia sobe
cerca de 100x em todos os casos (bubble: ~107x, selection: ~99x). Isso é
esperado pra complexidade quadrática, mas é bom ver o comportamento teórico
batendo com a medição real de energia, e não só com tempo de execução.

## Conclusão geral

Pra quem se importa com consumo de energia em ordenação de listas grandes, dois
pontos práticos saem desse experimento: primeiro, escolher um algoritmo mais
eficiente (selection sort no lugar de bubble sort) importa mais do que só
otimizar a implementação de um algoritmo ruim. Segundo, otimizações que cortam
tempo de execução se traduzem quase diretamente em economia de energia aqui,
já que a potência consumida pela CPU se mantém praticamente estável — então
qualquer ganho de desempenho (menos iterações, parar mais cedo, evitar trabalho
redundante) tende a virar economia de energia proporcional.

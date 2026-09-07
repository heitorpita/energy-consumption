# Comparação das implementações de Bubble Sort (Rust)

Todas leem `n` e depois `n` inteiros de stdin (mesmo formato de
`alg_ordenacao/entrada_*.in`) e imprimem `n` seguido do vetor ordenado.

`bubblesort_1/2/3` são o mesmo algoritmo (double loop, trocas adjacentes)
com otimizações incrementais — isolam a estratégia como única variável.
`bubblesort_4_cocktail` e `bubblesort_5_comb` já mudam a estrutura da
comparação/varredura. `bubblesort_3_i64` isola só o efeito do tamanho da
palavra (i32→i64), mantendo o algoritmo do `bubblesort_3`.

| Arquivo | Estratégia | Melhor caso | Médio/Pior caso |
|---|---|---|---|
| `bubblesort_1.rs` | Ingênuo: sempre roda as `n` passadas completas | O(n²) | O(n²) |
| `bubblesort_2.rs` | Para quando uma passada não faz troca (`swapped`), mas cada passada ainda percorre o vetor inteiro | O(n) | O(n²) |
| `bubblesort_3.rs` | Além de parar, encolhe o intervalo a cada passada até a posição da última troca (equivalente ao `bubble_sort_melhorado.py`) | O(n) | O(n²), constante menor |
| `bubblesort_4_cocktail.rs` | Cocktail shaker sort: varre ida (empurra o maior pro fim) e volta (empurra o menor pro início) a cada ciclo, encolhendo dos dois lados. Resolve o problema das "tartarugas" (valor pequeno perto do fim) em um ciclo em vez de várias passadas | O(n) | O(n²), constante ainda menor |
| `bubblesort_5_comb.rs` | Comb sort: compara elementos afastados por um `gap` que encolhe a cada passada (fator 1.3), virando bubble sort normal só quando `gap=1`. Ataca as "tartarugas" deixando-as pular várias posições de uma vez | O(n) | O(n²) pior caso, mas caso médio bem melhor na prática |
| `bubblesort_3_i64.rs` | Mesmo algoritmo do `bubblesort_3`, só com `Vec<i64>` em vez de `Vec<i32>` — isola o efeito do dobro de memória por elemento na energia | O(n) | O(n²), constante menor |

Como as entradas são embaralhadas (`geraEntrada.cpp`), nenhuma atinge o
melhor caso — todas ficam em O(n²) na prática. O interessante do experimento
não é a complexidade assintótica das 3 primeiras (é igual), e sim a
diferença real de tempo/energia entre implementações com constantes e
estruturas diferentes.

## Build

```bash
cd rust_algs
cargo build --release
# binários em target/release/bubblesort_{1,2,3,4_cocktail,5_comb,3_i64}
```

## Medição de energia — `run_benchmarks_rust.sh` (recomendado)

Roda a bateria completa (6 binários x 3 entradas) e grava
`resultados_rust.csv` com as mesmas colunas do `alg_ordenacao/resultados.csv`
(`repeticao;algoritmo;n;energia_j;tempo_exe_s;tempo_cpu_s;potencia_exe_w;potencia_cpu_w`),
baseado no `alg_ordenacao/run_repeticoes.sh` já existente no projeto.

```bash
./run_benchmarks_rust.sh 1 20   # repeticoes 1 a 20
```

Recomendado usar bem mais repetições que o experimento Python (10): os
binários Rust rodam ~100x mais rápido, então o ruído do RAPL pesa
proporcionalmente mais por execução.

## Medição manual com `perf` (debug pontual)

`-a` (system-wide) é obrigatório: `power/energy-pkg/` é um contador de
pacote (RAPL), só existe em modo system-wide. Sem `-a`, ao misturar com
`user_time`/`system_time` (eventos por processo) o `perf` cai no modo
por-processo e a energia aparece como `<not supported>` — mesmo como root.
Isso não tem relação com o aviso de `nmi_watchdog` que o `perf` imprime.

```bash
sudo perf stat -a -e power/energy-pkg/,duration_time,user_time,system_time \
  -- ./target/release/bubblesort_1 < ../alg_ordenacao/entrada_10.in > /dev/null
```

Não use a flag `-r` do perf aqui: com stdin redirecionado de arquivo, `-r`
reexecuta o mesmo processo reaproveitando o mesmo descritor de stdin, então
da 2ª repetição em diante o arquivo já está no EOF e o programa recebe
entrada vazia (panic). É por isso que `run_benchmarks_rust.sh` repete no
shell em vez de usar `-r`.

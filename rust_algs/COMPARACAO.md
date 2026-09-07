# Comparação das 3 implementações de Bubble Sort (Rust)

As três variantes leem `n` e depois `n` inteiros de stdin (mesmo formato de
`alg_ordenacao/entrada_*.in`) e imprimem `n` seguido do vetor ordenado.

Todas têm pior caso **O(n²)**; a diferença é o quanto de trabalho
desnecessário cada uma evita quando o vetor já está (parcialmente) ordenado.

| Arquivo | Estratégia | Melhor caso | Médio/Pior caso |
|---|---|---|---|
| `bubblesort_1.rs` | Ingênuo: sempre roda as `n` passadas completas | O(n²) | O(n²) |
| `bubblesort_2.rs` | Para quando uma passada não faz troca (`swapped`), mas cada passada ainda percorre o vetor inteiro | O(n) | O(n²) |
| `bubblesort_3.rs` | Além de parar, encolhe o intervalo a cada passada até a posição da última troca (equivalente ao `bubble_sort_melhorado.py`) | O(n) | O(n²), constante menor |

Como as entradas são embaralhadas (`geraEntrada.cpp`), nenhuma atinge o
melhor caso — as três ficam em O(n²). O interessante do experimento não é a
complexidade assintótica (é igual), e sim a diferença real de tempo/energia
entre implementações com constantes diferentes.

## Build

```bash
cd rust_algs
cargo build --release
# binários em target/release/bubblesort_1, bubblesort_2, bubblesort_3
```

## Medição com `perf`

`-a` (system-wide) é obrigatório: `power/energy-pkg/` é um contador de
pacote (RAPL), só existe em modo system-wide. Sem `-a`, ao misturar com
`user_time`/`system_time` (eventos por processo) o `perf` cai no modo
por-processo e a energia aparece como `<not supported>` — mesmo como root.
Isso não tem relação com o aviso de `nmi_watchdog` que o `perf` imprime.

```bash
sudo perf stat -a -e power/energy-pkg/,duration_time,user_time,system_time \
  -- ./target/release/bubblesort_1 < ../alg_ordenacao/entrada_10.in > /dev/null

sudo perf stat -a -e power/energy-pkg/,duration_time,user_time,system_time \
  -- ./target/release/bubblesort_2 < ../alg_ordenacao/entrada_10.in > /dev/null

sudo perf stat -a -e power/energy-pkg/,duration_time,user_time,system_time \
  -- ./target/release/bubblesort_3 < ../alg_ordenacao/entrada_10.in > /dev/null
```

Repita trocando `entrada_10.in` por `entrada_50.in`/`entrada_100.in`.

Para repetir e tirar média, **não use a flag `-r` do perf** com stdin
redirecionado de arquivo: `-r` reexecuta o mesmo processo reaproveitando o
mesmo descritor de stdin, então da 2ª repetição em diante o arquivo já está
no EOF e o programa recebe entrada vazia (panic). Repita no shell em vez
disso, acumulando no CSV com `--append`:

```bash
REPS=5
for algo in bubblesort_1 bubblesort_2 bubblesort_3; do
  for entrada in entrada_10 entrada_50 entrada_100; do
    out="resultados_${algo}_${entrada}.csv"
    rm -f "$out"
    for rep in $(seq 1 "$REPS"); do
      sudo perf stat -a -x';' --append \
        -e power/energy-pkg/,duration_time,user_time,system_time \
        -o "$out" \
        -- ./target/release/${algo} < "../alg_ordenacao/${entrada}.in" > /dev/null
    done
  done
done
```

- `power/energy-pkg/` retorna Joules; divida pelo `duration_time` (ns→s)
  para obter potência média em Watts, igual ao cálculo do `run_benchmarks.sh`.
- Os CSVs saem com dono `root` (rodam via `sudo`). Para mexer neles depois
  sem `sudo`: `sudo chown "$USER": resultados_*.csv`.

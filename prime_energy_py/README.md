# Consumo de energia de algoritmos de primalidade

Comparação de quatro implementações em Python de um teste de primalidade
(`primos1.py`…), medindo **energia** e **tempo de execução** para
diferentes tamanhos de entrada.

## Dicionário de variáveis

| Coluna | Unidade | O que é |
|---|---|---|
| `algoritmo` | — | Arquivo `.py` executado. |
| `numero` | — | Entrada `n` testada quanto à primalidade. |
| `energy_pkg_J` | joules | Energia consumida pelo **pacote inteiro do processador**. |
| `tempo_ns` | nanossegundos | Tempo de parede (*wall clock*) do processo inteiro, do `exec` até o `exit`. |
| `variancia_pkg_pct` | % | Dispersão relativa das repetições da medida de `energy_pkg_J` (desvio-padrão / média). Quanto menor, mais estável a medida. |
| `energy_cores_J` | joules | Energia do RAPL. |
| `variancia_cores_pct` | % | Mesma ideia, para `energy_cores_J`. |

**Notas importantes sobre as unidades:**

- O CSV usa `;` como separador de campo e **vírgula como separador decimal**
  (padrão pt-BR). Ao ler com pandas:
  `pd.read_csv("resultados.csv", sep=";", decimal=",")`.
- RAPL é uma **estimativa por modelo interno** do processador, não um wattímetro.
  Serve muito bem para comparação relativa, mas não é medida absoluta calibrada.

---

## Como reproduzir

```bash
# medição de um ponto
perf stat -r 10 -e power/energy-pkg/,power/energy-cores/ \
    python3 primos2.py 9999991
```
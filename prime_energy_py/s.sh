#!/bin/bash
# run_experiment.sh
# Roda os 4 algoritmos de primalidade para varios numeros,
# medindo energia (pkg e cores) via perf, com 10 repeticoes cada.
#
# Uso: coloque este script dentro da pasta prime_energy_py
# (junto de primos1.py, primos2.py, primos3.py, primos4.py) e rode:
#   chmod +x run_experiment.sh && ./run_experiment.sh
#
# Formato real de saida do perf -x ";" neste sistema:
#   valor;unidade;evento;variancia_pct;tempo_ns;pct_ativo;;
# (confirmado via teste manual em 24/08/2026)

ALGORITHMS=("primos1.py" "primos2.py" "primos3.py" "primos4.py")
NUMBERS=(5 100 10007 100000 9999991)
REPS=10
OUTFILE="resultados.csv"

echo "algoritmo;numero;energy_pkg_J;tempo_ns;variancia_pkg_pct;energy_cores_J;variancia_cores_pct" > "$OUTFILE"

for algo in "${ALGORITHMS[@]}"; do
    for n in "${NUMBERS[@]}"; do
        echo "Rodando $algo com n=$n (10 repeticoes)..."

        raw=$(echo "$n" | perf stat -r $REPS -x ";" -e power/energy-pkg/,power/energy-cores/ \
              python3 "$algo" "$n" 2>&1 >/dev/null)

        pkg_line=$(echo "$raw" | grep "energy-pkg")
        cores_line=$(echo "$raw" | grep "energy-cores")

        pkg_val=$(echo "$pkg_line" | cut -d';' -f1)
        pkg_var=$(echo "$pkg_line" | cut -d';' -f4 | tr -d '%')
        tempo_ns=$(echo "$pkg_line" | cut -d';' -f5)

        cores_val=$(echo "$cores_line" | cut -d';' -f1)
        cores_var=$(echo "$cores_line" | cut -d';' -f4 | tr -d '%')

        echo "${algo};${n};${pkg_val};${tempo_ns};${pkg_var};${cores_val};${cores_var}" >> "$OUTFILE"
    done
done

echo ""
echo "Concluido! Resultados salvos em $OUTFILE"

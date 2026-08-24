# energy-consumption

Estudo empírico do consumo energético de software em hardware real.

## Ambiente de medição

Os experimentos são executados em uma máquina Linux com acesso direto aos
contadores RAPL, expostos em `/sys/class/powercap/`. Ambientes virtualizados não
são utilizados para medição, pois o hipervisor não expõe os contadores reais de
hardware.

## Referências

Trabalhos que servem de base metodológica:

https://luiscruz.github.io/course_sustainableSE/2026/
https://github.com/tdurieux/energibridge

## Contexto

Repositório desenvolvido no âmbito da disciplina ECT3707 (UFRN), sob orientação
do professor Sérgio Queiroz de Medeiros.

from timeit import default_timer

import matplotlib.pyplot as plt

from pizzaria import estado, estado_lock, iniciar_simulacao

ARQUIVO_GRAFICO = "grafico_pizzaria.png"

CONFIGURACOES_TESTE = [
    (1, 1),
    (2, 2),
    (4, 4),
    (8, 8),
]

PIZZAS_POR_CHEF = 10


def resetar_estado():
    with estado_lock:
        estado["chefs"] = {}
        estado["entregadores"] = {}
        estado["fila"] = 0
        estado["produzidas"] = 0
        estado["entregues"] = 0


def executar_testes():
    tempos = []
    total_threads_list = []
    labels_configuracao = []

    for chefs, entregadores in CONFIGURACOES_TESTE:
        total_threads = chefs + entregadores
        label = f"{chefs} chef(s) + {entregadores} entregador(es)"

        print(f"\nIniciando teste: {label}")
        resetar_estado()

        inicio = default_timer()
        iniciar_simulacao(chefs, entregadores, PIZZAS_POR_CHEF)
        fim = default_timer()

        tempo_total = fim - inicio

        tempos.append(tempo_total)
        total_threads_list.append(total_threads)
        labels_configuracao.append(label)

        print(f"{label} | total de threads: {total_threads} | tempo: {tempo_total:.2f}s")

    tempo_base = tempos[0]
    speedups = [tempo_base / tempo for tempo in tempos]

    print("\nSpeedups:")
    for label, speedup in zip(labels_configuracao, speedups):
        print(f"{label}: S = {speedup:.2f}")

    return total_threads_list, tempos, speedups


def gerar_graficos(total_threads_list, tempos, speedups):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(total_threads_list, tempos, marker="o")
    plt.xlabel("Numero total de threads (chefs + entregadores)")
    plt.ylabel("Tempo total (s)")
    plt.title("Tempo vs Numero de Threads")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(total_threads_list, speedups, marker="o", color="r")
    plt.xlabel("Numero total de threads")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Numero de Threads")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(ARQUIVO_GRAFICO, dpi=150, bbox_inches="tight")
    print(f"\nGrafico salvo em: {ARQUIVO_GRAFICO}")

    try:
        plt.show()
    finally:
        plt.close()


if __name__ == "__main__":
    try:
        total_threads_list, tempos, speedups = executar_testes()
        gerar_graficos(total_threads_list, tempos, speedups)
        print("\nExecucao finalizada com sucesso.")
    except KeyboardInterrupt:
        print("\nExecucao interrompida pelo usuario.")

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

TOTAL_PIZZAS = 120


def resetar_estado():
    with estado_lock:
        estado["chefs"] = {}
        estado["entregadores"] = {}
        estado["fila"] = 0
        estado["produzidas"] = 0
        estado["entregues"] = 0


def executar_testes():
    resultados = []

    for chefs, entregadores in CONFIGURACOES_TESTE:
        if TOTAL_PIZZAS % chefs != 0:
            raise ValueError(
                f"TOTAL_PIZZAS={TOTAL_PIZZAS} precisa ser divisivel por {chefs} chefs."
            )

        pizzas_por_chef = TOTAL_PIZZAS // chefs
        total_threads = chefs + entregadores
        label = f"{chefs} chef(s) + {entregadores} entregador(es)"

        print(
            f"\nIniciando teste: {label} | "
            f"{pizzas_por_chef} pizza(s) por chef | {TOTAL_PIZZAS} pizzas no total"
        )
        resetar_estado()

        inicio = default_timer()
        iniciar_simulacao(chefs, entregadores, pizzas_por_chef)
        fim = default_timer()

        tempo_total = fim - inicio

        resultados.append(
            {
                "label": label,
                "total_threads": total_threads,
                "pizzas_por_chef": pizzas_por_chef,
                "tempo_total": tempo_total,
            }
        )

        print(f"{label} | total de threads: {total_threads} | tempo: {tempo_total:.2f}s")

    tempo_base = resultados[0]["tempo_total"]
    for resultado in resultados:
        resultado["speedup"] = tempo_base / resultado["tempo_total"]

    print("\nSpeedups:")
    for resultado in resultados:
        print(f"{resultado['label']}: S = {resultado['speedup']:.2f}")

    return resultados


def imprimir_tabela_resultados(resultados):
    colunas = [
        ("Configuracao", lambda r: r["label"]),
        ("Threads", lambda r: str(r["total_threads"])),
        ("Pizzas/Chef", lambda r: str(r["pizzas_por_chef"])),
        ("Pizzas Totais", lambda r: str(TOTAL_PIZZAS)),
        ("Tempo (s)", lambda r: f"{r['tempo_total']:.4f}"),
        ("Speedup", lambda r: f"{r['speedup']:.4f}"),
    ]

    larguras = []
    for titulo, extrair in colunas:
        largura = len(titulo)
        for resultado in resultados:
            largura = max(largura, len(extrair(resultado)))
        larguras.append(largura)

    cabecalho = " | ".join(
        titulo.ljust(largura)
        for (titulo, _), largura in zip(colunas, larguras)
    )
    separador = "-+-".join("-" * largura for largura in larguras)

    print("\nTabela final dos resultados:")
    print(cabecalho)
    print(separador)

    for resultado in resultados:
        linha = " | ".join(
            extrair(resultado).ljust(largura)
            for (_, extrair), largura in zip(colunas, larguras)
        )
        print(linha)


def gerar_graficos(resultados):
    total_threads_list = [resultado["total_threads"] for resultado in resultados]
    tempos = [resultado["tempo_total"] for resultado in resultados]
    speedups = [resultado["speedup"] for resultado in resultados]

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
        resultados = executar_testes()
        imprimir_tabela_resultados(resultados)
        gerar_graficos(resultados)
        print("\nExecucao finalizada com sucesso.")
    except KeyboardInterrupt:
        print("\nExecucao interrompida pelo usuario.")

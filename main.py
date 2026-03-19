import tkinter as tk
from interface import Interface
from pizzaria import iniciar_simulacao
import threading
import signal
import sys

def signal_handler(sig, frame):
    print('Interrupção detectada, encerrando...')
    sys.exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    chefs = int(input("Chefs: "))
    entregadores = int(input("Entregadores: "))
    pizzas = int(input("Pizzas por chef: "))

    root = tk.Tk()

    Interface(root)

    # Executar simulação em uma thread separada para não bloquear a interface
    sim_thread = threading.Thread(target=iniciar_simulacao, args=(chefs, entregadores, pizzas))
    sim_thread.start()

    root.mainloop()
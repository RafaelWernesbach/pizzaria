import threading
from queue import Queue
import time
from random import randint
from math import sqrt

fila = Queue(maxsize=100)
forno = threading.Semaphore(2)
condition = threading.Condition()

intervalo = 100000
SENTINELA = object()

estado_lock = threading.Lock()
estado = {
    "chefs": {},
    "entregadores": {},
    "fila": 0,
    "produzidas": 0,
    "entregues": 0,
}

num_pizzas = 0


def eh_primo(x):
    if x < 2:
        return None
    if x == 2:
        return x
    if x % 2 == 0:
        return None

    limit = int(sqrt(x)) + 1
    for i in range(3, limit, 2):
        if x % i == 0:
            return None
    return x


def atualizar_estado_chef(nome, status=None, pizza=None, feitas=None):
    with estado_lock:
        if nome not in estado["chefs"]:
            estado["chefs"][nome] = {"status": "", "pizzas": [], "feitas": 0}

        if status:
            estado["chefs"][nome]["status"] = status

        if pizza:
            estado["chefs"][nome]["pizzas"].append(pizza)

        if feitas is not None:
            estado["chefs"][nome]["feitas"] = feitas

        estado["fila"] = fila.qsize()


def atualizar_estado_entregador(nome, status=None):
    with estado_lock:
        if nome not in estado["entregadores"]:
            estado["entregadores"][nome] = {"status": ""}

        if status:
            estado["entregadores"][nome]["status"] = status

        estado["fila"] = fila.qsize()


class Chef(threading.Thread):

    def run(self):
        pizzas_feitas = 0
        atualizar_estado_chef(self.name, "separando ingredientes")

        while pizzas_feitas < num_pizzas:

            atualizar_estado_chef(self.name, "esperando forno")

            with forno:

                atualizar_estado_chef(self.name, "usando forno")

                ingrediente = randint(10**13, 10**13 + intervalo)

                if eh_primo(ingrediente):
                    pizza = ingrediente
                    print(f"Chef {self.name} faz uma pizza sendo o numero {pizza}")
                    pizzas_feitas += 1
                else:
                    pizza = None

            if pizza:

                with condition:

                    fila.put(pizza)

                    with estado_lock:
                        estado["produzidas"] += 1

                    atualizar_estado_chef(
                        self.name,
                        f"pizza {pizza}",
                        pizza,
                        pizzas_feitas
                    )

                    condition.notify()

            else:

                atualizar_estado_chef(
                    self.name,
                    "não encontrou primo",
                    feitas=pizzas_feitas
                )

        atualizar_estado_chef(self.name, "finalizado")


class Entregador(threading.Thread):

    def run(self):

        atualizar_estado_entregador(self.name, "ocioso")

        while True:

            with condition:

                while fila.empty():
                    condition.wait()

                pizza = fila.get()

            if pizza is SENTINELA:
                atualizar_estado_entregador(self.name, "finalizado")
                break

            print(f"Entregador {self.name} entrega pizza premium: {pizza}")

            atualizar_estado_entregador(self.name, f"entregando {pizza}")

            time.sleep(0.2)

            with estado_lock:
                estado["entregues"] += 1

            atualizar_estado_entregador(self.name, "ocioso")


def iniciar_simulacao(chefs, entregadores, pizzas_por_chef):

    global num_pizzas
    num_pizzas = pizzas_por_chef

    chefs_threads = [Chef(name=f"Chef-{i+1}") for i in range(chefs)]
    entregadores_threads = [Entregador(name=f"Entregador-{i+1}") for i in range(entregadores)]

    for e in entregadores_threads:
        e.start()

    for c in chefs_threads:
        c.start()

    # Esperar chefs terminarem
    for c in chefs_threads:
        c.join()

    # Enviar sentinela para cada entregador e acordar
    # todas as threads consumidoras que possam estar esperando.
    with condition:
        for _ in range(entregadores):
            fila.put(SENTINELA)
        condition.notify_all()

    # Esperar entregadores terminarem
    for e in entregadores_threads:
        e.join()

    return chefs_threads, entregadores_threads

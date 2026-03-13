import threading
from queue import Queue
import time
from random import randint
from math import sqrt

fila = Queue()
forno = threading.Semaphore(3)
condition = threading.Condition()

def eh_primo(x):
    """
    Retorna o proprio numero se for primo, None caso contrario.
    """
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


def buscar_primos_no_intervalo(ingredientes):
    primos = Queue()

    for num in ingredientes:
        if eh_primo(num) is not None:
            primos.put(num)

    return primos




class Chef(threading.Thread):
    def run(self):
        intervalo = randint(2000, 2000)
        ingredientes = range(10**13, 10**13 + intervalo)

        print(f"Chef {self.name} separando os ingredientes")
        pizzas = buscar_primos_no_intervalo(ingredientes)

        print("FORNO QUENTE!!!!!!")
        time.sleep(2)

        count = pizza._qsize()
        while not pizzas.empty():

            print(f"{self.name} esperando forno")

            with forno:
                print(f"{self.name} usando forno ")
                time.sleep(0.1)

            with condition:
                pizza = pizzas.get()
                fila.put(pizza)
                print(f"{self.name} fez pizza {pizza}")
                condition.notify()
        
        print(f"Pizzas feitas pelo chef {self.name}: {count}")


class Entregador(threading.Thread):
    def run(self):
        while True:

            with condition:
                while fila.empty():
                    condition.wait()

                pizza = fila.get()

            print(f"Entregue pizza premium {pizza}")
            time.sleep(0.1)



chefs = [Chef() for _ in range(2)]
entregadores = [Entregador() for _ in range(2)]

for c in chefs:
    c.start()

for e in entregadores:
    e.start()

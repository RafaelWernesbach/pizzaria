import tkinter as tk
from tkinter import ttk
from pizzaria import estado, estado_lock


class Interface:

    def __init__(self, root):

        self.root = root
        root.title("Pizzaria Concorrente")

        self.lbl = ttk.Label(root, text="")
        self.lbl.pack()

        self.txt_chefs = tk.Text(root, width=80, height=25)
        self.txt_chefs.pack()

        self.txt_entregadores = tk.Text(root, width=40, height=25)
        self.txt_entregadores.pack()

        self.update()

    def update(self):

        with estado_lock:

            chefs = dict(estado["chefs"])
            entregadores = dict(estado["entregadores"])
            fila = estado["fila"]
            prod = estado["produzidas"]
            entr = estado["entregues"]

        self.lbl.config(
            text=f"Pizzas produzidas {prod} | entregues {entr} | fila {fila}"
        )

        self.txt_chefs.delete("1.0", tk.END)

        for nome, info in chefs.items():

            self.txt_chefs.insert(
                tk.END,
                f"{nome} | {info['status']} | feitas {info['feitas']}\n"
            )

        self.txt_entregadores.delete("1.0", tk.END)

        for nome, info in entregadores.items():

            self.txt_entregadores.insert(
                tk.END,
                f"{nome} | {info['status']}\n"
            )

        self.root.after(500, self.update)
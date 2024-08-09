import threading as tr
import datetime as dt
import random as rd

# Inicializando semáforos para três barbeiros, todos começando "dormindo"
barbeiros = [tr.Semaphore(0) for _ in range(3)]

# Função para simular um cliente acordando um barbeiro
def cliente_chega(id_cliente):
    # Escolhe um barbeiro para acordar (simplesmente o primeiro barbeiro dormindo)
    for i, barbeiro in enumerate(barbeiros):
        if barbeiro._value == 0:  # Verifica se o barbeiro está dormindo
            barbeiro.release()
            print(f"Cliente {id_cliente} acordou o barbeiro {i}")
            break

# Função para simular um barbeiro atendendo um cliente
def barbeiro_atende(id_barbeiro):
    barbeiros[id_barbeiro].acquire()
    print(f"Barbeiro {id_barbeiro} está atendendo um cliente")

# Simulando a chegada de três clientes
for i in range(3):
    cliente_chega(i)

# Simulando barbeiros atendendo clientes
for i in range(3):
    barbeiro_atende(i)

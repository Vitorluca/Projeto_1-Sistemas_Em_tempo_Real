#dev.: Vitorluca
#version 1.0

import threading as tr
import datetime as dt
import random as rd
import time as tm
import queue 

# Inicializando semáforos para três barbeiros, todos começando "dormindo"
barbers = [tr.Semaphore(1), tr.Semaphore(1), tr.Semaphore(1)] # create 3 brabers init dormindo
chairs = tr.Semaphore(5) # create five chairs alive

lock_barbers = tr.Lock() # create mutex for barbers
lock_chairs = tr.Lock() # create mutex for chairs


# create a function to simulate a client arriving
def cliente_chega(id_cliente):
        print(f"Cliente {id_cliente} chegou.\n")
        if chairs._value > 0:
            with lock_chairs: # lock sessão critica do codigo
                chairs.acquire()
                print(f"Cliente {id_cliente} sentou na cadeira de espera.\n")
            tm.sleep(3) # tempo para visualização da saida
        else:
            print(f"Cliente {id_cliente} foi embora sem ser atendido, não há cadeiras de espera disponíveis.\n") # cliente vai embora

barber_queue = queue.Queue()  # Fila para gerenciar a ordem dos barbeiros
for i in range(3):
    barber_queue.put(i)  # Inicializa a fila com os índices dos barbeiros

def barbeiro_atende(id_cliente):
    while True:
        i = barber_queue.get()  # Obtém o próximo barbeiro da fila
        with lock_barbers:
            if barbers[i]._value == 1:
                barbers[i].acquire()  # acorda o barbeiro
                print(f"Barbeiro {i} está atendendo o cliente {id_cliente}\n")
                tm.sleep(3)  # tempo para visualização da saída
                chairs.release()  # libera cadeira para cliente
                barbers[i].release()  # libera o barbeiro
                print(f"Barbeiro {i} terminou de atender e está pronto para o próximo cliente.\n")
                barber_queue.put(i)  # Coloca o barbeiro de volta na fila
                break  # Sai do loop após o atendimento
            else:
                barber_queue.put(i)  # Recoloca o barbeiro na fila se estiver ocupado
                tm.sleep(1)  # Espera um pouco antes de tentar novamente
            

def wrapper(client_number): #involucro para passar parametros para a função
    cliente_chega(client_number)
    barbeiro_atende(client_number)

#main code
clients = [] # cria uma lista de threads para os clientes

client_number = 0 # inicializa o contador de clientes

while True:
    tm.sleep(1) # tempo para visualização da saida
    if rd.randint(0, 1) == 1: # se o numero aleatorio for 1, um cliente chega
        client = tr.Thread(target=wrapper ,args=(client_number,) ,name=f"Trhead-{client_number}") #cria uma trhead para o cliente
        client.start()
        clients.append(client) # adiciona a trhead cliente a lista de trheads clientes
        # for client in clients: # Wait for all threads to finish
        #     client.join()
        client_number += 1 # incrementa o contador de clientes
    else:
        pass

import threading as tr
import datetime as dt
import random as rd
import time as tm

# Inicializando semáforos para três barbeiros, todos começando "dormindo"
barbers = [tr.Semaphore(1), tr.Semaphore(1), tr.Semaphore(1)] # create 3 brabers init dormindo
chairs = tr.Semaphore(5) # create five chairs alive

lock_barbers = tr.Lock() # create mutex for barbers
lock_chairs = tr.Lock() # create mutex for chairs


# create a function to simulate a client arriving
def cliente_chega(id_cliente):
        print(f"Cliente {id_cliente} chegou.")
        if chairs._value > 0:
            with lock_chairs: # lock sessão critica do codigo
                chairs.acquire()
                print(f"Cliente {id_cliente} sentou na cadeira de espera.")
            tm.sleep(3) # tempo para visualização da saida
        else:
            print(f"Cliente {id_cliente} foi embora sem ser atendido, não há cadeiras de espera disponíveis.") # cliente vai embora

# Função para simular um barbeiro atendendo um cliente
def barbeiro_atende(id_cliente):
    for i in range(3):
        print(f'contador for {i}')
        if barbers[i]._value == 1:
            with lock_barbers:
                barbers[i].acquire() # acorda barbeiro 1
                print(f"Barbeiro {i} está atendendo o cliente {id_cliente}")
                tm.sleep(3) # tempo para visualização da saida
                chairs.release() # libera cadeira para cliente
                barbers[i].release() #libera um barbeiro
                print(f"Barbeiro {i} terminou de atender e está pronto para o próximo cliente.")
        else:
            print(f"Todos os Barbeiro estão ocupados, cliente deve esperar.") # barbeiro ocupado
            

def wrapper(client_number): #involucro para passar parametros para a função
    cliente_chega(client_number)
    barbeiro_atende(client_number)

    # threads_cliente_chega = tr.Thread(target=cliente_chega,args=(client_number,) ,name=f"Trhead-{client_number}")
    # threads_barbeiro_atende = tr.Thread(target=barbeiro_atende,args=(client_number,) ,name=f"Trhead-{client_number}")

    # #inicia as trheads
    # threads_cliente_chega.start()
    # threads_barbeiro_atende.start()

    # #espera as trheads terminarem
    # threads_cliente_chega.join()
    # threads_barbeiro_atende.join()


#main code
clients = [] # cria uma lista de threads para os clientes

client_number = 0 # inicializa o contador de clientes

while True:
    tm.sleep(1) # tempo para visualização da saida
    if rd.randint(0, 1) == 1 or 0: # se o numero aleatorio for 1, um cliente chega
        client = tr.Thread(target=wrapper ,args=(client_number,) ,name=f"Trhead-{client_number}") #cria uma trhead para o cliente
        client.start()
        clients.append(client) # adiciona a trhead cliente a lista de trheads clientes
        # for client in clients: # Wait for all threads to finish
        #     client.join()
        client_number += 1 # incrementa o contador de clientes
    else:
        pass

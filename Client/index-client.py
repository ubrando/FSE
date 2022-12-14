import threading
import socket
import distribuido


def main():
    global sala
    sala = distribuido.Sala(1)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 10213))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')
    username = sala.nome
    print(f'\n{username}, está conectada!')
    sala.configuraEntradas()
    sala.configuraSaidas()
    sala.ligarLampada1()

    thread1 = threading.Thread(target=receiveMessages, args=[client, username])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()
    

def receiveMessages(client,username):
    global sala
    while True:
        try:
            msg = str(client.recv(2048).decode('utf-8'))                    
            if msg == "l_01":
                print(f'{username} - Lâmpada 01 está ligada.')
                sala.ligarLampada1()
            if msg == "l_02":
                print(f'{username} - Lâmpada 02 está ligada.')
                sala.ligarLampada2()
            if msg == "AC":
                print(f'{username} - Ar condicionado está ligado.')
                sala.ligarAC()
            if msg == "PR":
                print(f'{username} - Projetor está ligado.')
                sala.ligarProjetor()
            if msg == "l_01OFF":
                sala.desligarLampada1()
            if msg == "l_02OFF":
                sala.desligarLampada2()
            if msg == "ACOFF":
                sala.desligarAC()
            if msg == "PROFF":
                sala.desligarPojetor()                
            

        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


main()
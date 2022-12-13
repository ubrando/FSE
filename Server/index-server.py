import threading
import socket

clients = []

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = 'Servidor Central'
    try:
        server.bind(('localhost', 7777))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)

        thread01 = threading.Thread(target=messagesTreatment, args=[client])
        thread01.start()
        thread02 = threading.Thread(target=sendMessages, args=[client,username])
        thread02.start()

def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'{msg}'.encode('utf-8'))
        except:
            return

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg + '\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)

main()
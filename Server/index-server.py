import threading
import socket
from os.path import exists
from datetime import datetime
from csv import writer
import json
import Sala 
import sys

# Inicialização da estrura Sala.
global sala
sala = Sala.monitoramento()

# Lista de Clients conectados.
clients = []

# Função main do servidor.
def main():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7794))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)
        thread1 = threading.Thread(target=messagesTreatment, args=[client])
        thread2 = threading.Thread(target=sendMessages, args=[client])
        thread1.start()
        thread2.start()

# Função da thread mandar mensagem para o client.
def sendMessages(client):
    while True:
        try:
            menu()
            resp = input('\n')
            msg = navergar(resp,client)
            client.send(f'{msg}'.encode('utf-8'))
        except:
            client.shutdown()
            client.close()
            return

# Função de tratar a mensagem recebida
# Recebe o json enviado pelo client preenche os dados na estrutura de Sala.
def messagesTreatment(client):
    while True:
        try:
            msg= client.recv(1024).decode()
            msg_decode = json.loads(msg)
            sala.numero_sala = msg_decode["Sala"]
            sala.lampada01 = msg_decode["Lampada01"]
            sala.lampada02 = msg_decode["Lampada02"]
            sala.ar_condicionado = msg_decode["ArCondicionado"]
            sala.projetor = msg_decode["Projetor"]
            sala.alarme =  msg_decode["Alarme"]
            sala.alarmeIncendio = msg_decode["AlarmeIncendio"]
            sala.buzina = msg_decode["Buzina"]
            sala.sensor_presenca = msg_decode["SPres"]
            sala.sensor_janela = msg_decode['Sjan']
            sala.sensor_fumaca = msg_decode['SFum']
            sala.temperatura = msg_decode['temperatura']
            sala.humidade = msg_decode['humidade']
            sala.pessoas = msg_decode['pessoas']

        except:
            print("não foi possível receber a mensagem")
            deleteClient(client)
            client.shutdown()
            client.close()
            break

# Gerar estado do sensor para relatório
def getActive(sensor):
    if sensor:
        return 'Ligado'
    else:
        return 'Desligado.'

# Gerar Relatório da sala.
def gerarRelatorio():
    print(f"""
        Numero da sala -        {sala.numero_sala}
        Lampada 01              {getActive(sala.lampada01)}
        Lampada 02              {getActive(sala.lampada02)}
        Ar Condicionado         {getActive(sala.ar_condicionado)}
        Projetor                {getActive(sala.projetor)}
        Alarme                  {getActive(sala.alarme)}
        Alarme de Incendio      {getActive(sala.alarmeIncendio)}
        Buzina                  {getActive(sala.buzina)}
        Sensor de Presença      {getActive(sala.sensor_presenca)}
        Sensor de Janela        {getActive(sala.sensor_janela)}
        Sensor de Fumaça        {getActive(sala.sensor_fumaca)}
        Temperatura             {sala.temperatura}
        Humidade                {sala.humidade}
        Ocupantes               {sala.pessoas}
                    
    """)

# Função para exibir mo menu de opções.
def menu():
    print('''Digite o número da opção:
        1 - Ligar lâmpada 1.
        2 - Desligar lâmpada 1.
        3 - Ligar lâmpada 2.
        4 - Desligar lâmpada 2.
        5 - Ligar ar condionado.
        6 - Desligar ar condionado.
        7 - Ligar projetor.
        8 - Desligar projetor.
        9 - Ligar alarme.
        10 - Desligar alarme.
        11 - Ligar alarme de incêndio.
        12 - Desligar alarme de incêndio.
        13 - Exibir relatório da Sala. 
        14 - Desligar Buzina.
        15 - Sair.
        ''')

# Função selecionar a opção desenjada regitando no log.
def navergar(resp,client):
    try:
        if resp == '1':
            msg = 'l_01'
            registrar_log('Ligar lâmpada 1.')
        if resp == '2':
            msg = 'l_01OFF'
            registrar_log('Desligar lâmpada 1.')
        if resp == '3':
            msg = 'l_02'
            registrar_log('Ligar lâmpada 2.')
        if resp == '4':
            msg = 'l_02OFF'
            registrar_log('Desligar lâmpada 1.')
        if resp == '5':
            msg = 'AC'
            registrar_log('Ligar ar condicionado.')
        if resp == '6':
            msg = 'ACOFF'
            registrar_log('Desligar ar condicionado.')
        if resp == '7':
            msg = 'PR'
            registrar_log('Ligar projetor.')
        if resp == '8':
            msg = 'PROFF'
            registrar_log('Desligar projetor.')
        if resp == '9':
            msg = 'AL'
            registrar_log('Ligar alarme.')
        if resp == '10':
            msg = 'ALOFF'
            registrar_log('Desligar alarme.')
        if resp == '11':
            msg = 'FUM'
            registrar_log('Ligar alarme de incendio.')
        if resp == '12':
            msg = 'FUMOFF'
            registrar_log('Desligar alarme de incendio.')
        if resp == '13':
            gerarRelatorio()
            input("Pressione <Enter> para voltar ao menu.")
            msg = 'relatório'
            registrar_log('Solicitar relatório.')
        if resp == '14':
            registrar_log('Desligar Buzina.')
            msg = 'AL_BZ'
        if resp == '15':
            registrar_log('Sair.')
            msg = 'encerrando' 
            client.shutdown()
            client.close()
            client.close()  
            sys.exit()         
        print ("\n" * 130) 
        return msg

    except KeyboardInterrupt:
        client.shutdown()
        client.close()
        client.close()
        sys.exit()

        
# Função para deletar client da lista de clients conectdados
def deleteClient(client):
    clients.remove(client)

# Função para registrar os comandos no log.
def registrar_log(mensagem_registro):

    if exists('log.csv') == False:
        with open('log.csv','w', encoding='UTF8') as log_file:
            writter = writer(log_file)
            data = ["mensagem", "data do registro", "hora do registro"]
            writter.writerow(data)

    now = datetime.now()
    
    data_do_registro = now.strftime("%d/%m/%Y")
    hora_do_registro = now.strftime("%H:%M:%S")

    List = [mensagem_registro, data_do_registro, hora_do_registro]
    
    with open('log.csv', 'a') as f_object:
    
        writer_object = writer(f_object)    
        writer_object.writerow(List)
        f_object.close()



main()
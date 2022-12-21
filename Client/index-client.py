import threading
import socket
import distribuido
import time
import json
import sys

# Inicialização da estrutura sala
global sala
sala = distribuido.Sala(2)

# Função main do client
def main():
    global sala
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 7794))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')
    print (f"Sala {sala.numero_sala} conectada.")
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client])
    thread3 = threading.Thread(target=contagemDePessoas, args=[])
    thread1.start()
    thread2.start()
    thread3.start()
    
# Função para thread receber mensagens
# Recebe uma mensagem em forma de ID do servidor e altera os estados solocitados.
def receiveMessages(client):
    global sala
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg == "l_01":
                print('chegou')
                sala.ligarLampada1()
            if msg == "l_02":
                sala.ligarLampada2()
            if msg == "AC":
                sala.ligarAC()
            if msg == "PR":
                sala.ligarProjetor()
            if msg == "l_01OFF":
                sala.desligarLampada1()
            if msg == "l_02OFF":
                sala.desligarLampada2()
            if msg == "ACOFF":
                sala.desligarAC()
            if msg == "PROFF":
                sala.desligarPojetor()   
            if msg == "AL":
                sala.ligarAlarme()            
            if msg == "ALOFF":
                sala.desligarAlarme()
            if msg == "FUM":
                sala.ligarAlarmeIncendio()           
            if msg == "FUMOFF":
                sala.desligarAlarmeIncendio()
            if msg == 'encerrando':
                client.shutdown()
                client.close()
                sys.exit()
            if msg == "AL_BZ":
                sala.desligarBuzina()
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.shutdown()
            client.close()
            break
            
# Função da thread enviar mensagem onde gera ym relattório e envia para o servidor em forma de json
def sendMessages(client):
    while True:
        try:
            sala.contadorDepessoas()
            msg = gerarRelatorio()
            client.send(f'{json.dumps(msg)}'.encode('utf-8'))
        except:
            print("não foi possível enviar a mensagem")
            client.shutdown()
            client.close()
            break

# Função que formaliza o estado dos outputs 
def getActive(sensor):
    if sensor.is_active:
        return True
    else:
        return False

# Função que formaliza o estado dos sensores 
def getActiveSensor(sensor):
    if not sensor.is_active:
        return True
    else:
        return False

# Função para gerar relatório do estado da sala.
def gerarRelatorio():
    sala.medidor()
    sala.ligarBuzina()
    lampada01 = getActive(sala.L_01)
    lampada02 = getActive(sala.L_02)
    arCondicionado = getActive(sala.AC)
    projetor = getActive(sala.PR)
    buzina = getActive(sala.AL_BZ)
    spres =  getActiveSensor(sala.SPres)
    sjan = getActiveSensor(sala.SJan)
    sfum = getActiveSensor(sala.SFum)
    temperatura = sala.temperatura
    humidade = sala.humidity
    pessoas = str(sala.pessoas)
    estado = {
        'Sala':"1",
        'Lampada01': lampada01,
        'Lampada02': lampada02,
        'ArCondicionado': arCondicionado,
        'Projetor': projetor,
        'Alarme' : sala.SensorAlarme,
        'AlarmeIncendio': sala.SensorIncendio,
        'Buzina': buzina,
        'SPres': spres,
        'Sjan': sjan,
        'SFum': sfum,
        'temperatura': temperatura,
        'humidade': humidade,
        'pessoas' : pessoas

}
    return estado

# Função para a thread de contagem de pessoas.
def contagemDePessoas():
    while True:
        sala.contadorDepessoas()
main()

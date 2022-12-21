import RPi.GPIO as GPIO
import json
import time
from gpiozero import LED, Button
import board
import adafruit_dht



class Sala:
    GPIO.setwarnings(False)
    def __init__(self,ID):
        
        # Abertura do json para configuração da placa
        if (ID % 2 == 1):
            with open("configuracao_sala_01.json", encoding='utf-8') as file:
                config_sala = json.load(file)

        if (ID % 2 == 0):
            with open("configuracao_sala_02.json", encoding='utf-8') as file:
                config_sala = json.load(file)        
        
        #Número da sala
        self.numero_sala = ID

        #Saídas
        self.nome = config_sala["nome"]
        self.L_01 = LED(config_sala["outputs"][0]["gpio"]) #lâmpada 01
        self.L_02 = LED(config_sala["outputs"][1]["gpio"]) #lâmpada 02
        self.AC = LED(config_sala["outputs"][3]["gpio"])  #ar-condicionado
        self.PR = LED(config_sala["outputs"][2]["gpio"]) #projetos
        self.AL_BZ = LED(config_sala["outputs"][4]["gpio"]) #buzina

        #Entradas
        self.SPres = Button(config_sala["inputs"][0]["gpio"]) # sensor de presença
        self.SFum = Button(config_sala["inputs"][1]["gpio"]) #sensor de fumaça
        self.SJan = Button(config_sala["inputs"][2]["gpio"]) #sensor de janela
        self.SPor = Button(config_sala["inputs"][3]["gpio"]) #sensor de portas
        self.SC_IN = Button(config_sala["inputs"][4]["gpio"]) #sensor de entrada
        self.SC_OUT = Button(config_sala["inputs"][5]["gpio"]) #sensor de saída

        #Sensor DHT22
        self.temperatura = '21.7C'
        self.humidity = '79.0%'

        #Estados
        self.SensorAlarme = False
        self.SensorIncendio = False
        self.pessoas = 0

    # Funções de setar estados

    def ligarLampada1(self):
        self.L_01.on()


    def ligarLampada2(self):
        self.L_02.on()


    def desligarLampada1(self):
        self.L_01.off()


    def desligarLampada2(self):
        self.L_02.off()


    def ligarAC(self):
        self.AC.on()


    def desligarAC(self):
        self.AC.off()

    def ligarProjetor(self):
        self.PR.on()

    def desligarPojetor(self):
        self.PR.off()
    
    def ligarBuzina(self):
        if(((not self.SFum.is_active) and self.SensorIncendio) or ((self.SensorAlarme) and ((not self.SJan.is_active) or (not self.SPor.is_active) or (not self.SPres.is_active)))):
            self.AL_BZ.on()

    def desligarBuzina(self):
        self.AL_BZ.off()
    
    def ligarAlarme(self):
        self.SensorAlarme = True

    def desligarAlarme(self):
        self.SensorAlarme = False

    def ligarAlarmeIncendio(self):
        self.SensorIncendio = True 

    def desligarAlarmeIncendio(self):
        self.SensorIncendio = False 

    # Função de contar pessoas na sala
    def contadorDepessoas(self):
        if not self.SC_IN.is_active:
            self.pessoas +=1
            time.sleep(0.05)
                      
        if not self.SC_OUT.is_active:
            self.pessoas -= 1
            time.sleep(0.05)
        if self.pessoas < 0:
            self.pessoas = 0
            
    #   Função de medir temperatura 
    def medidor(self):
            if (self.numero_sala % 2 == 0): 
                GPIO.setup(18, GPIO.IN)
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                dhtDevice = adafruit_dht.DHT22(board.D18)
                dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
            else:
                GPIO.setup(4, GPIO.IN)
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                dhtDevice = adafruit_dht.DHT22(board.D4)
                dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
            try:
                self.humidity = f"{dhtDevice.humidity:.1f}%"
                self.temperatura = f"{dhtDevice._temperature}C"
                
            except RuntimeError as error:
                pass
                time.sleep(2.0)
            except Exception as error:
                dhtDevice.exit()
                raise error

    



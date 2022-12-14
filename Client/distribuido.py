import RPi.GPIO as GPIO
import json
import time

class Sala:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    def __init__(self,ID):
        #Abertura do json para configuração da placa
        with open("configuracao_sala_01.json", encoding='utf-8') as file:
            config_sala = json.load(file)
        
        self.numero_sala = ID
        #Saídas
        self.nome = config_sala["nome"]
        self.L_01 = config_sala["outputs"][0]["gpio"] #lâmpada 01
        self.L_02 = config_sala["outputs"][1]["gpio"] #lâmpada 02
        self.AC =config_sala["outputs"][3]["gpio"]  #ar-condicionado
        self.PR = config_sala["outputs"][2]["gpio"] #projetos
        self.AL_BZ = config_sala["outputs"][4]["gpio"] #buzina
        #Entradas
        self.SPres = config_sala["inputs"][0]["gpio"] # sensor de presença
        self.SFum = config_sala["inputs"][1]["gpio"] #sensor de fumaça
        self.SJan =config_sala["inputs"][2]["gpio"] #sensor de janela
        self.SPor =config_sala["inputs"][3]["gpio"] #sensor de portas
        self.SC_IN =config_sala["inputs"][4]["gpio"] #sensor de entrada
        self.SC_OUT =config_sala["inputs"][5]["gpio"] #sensor de saída
        #Sensor
        self.DHT22 = 4 #sensor de temperatura
        self.SensorAlarme = False
        self.SensorIncendio = True
    
    def configuraSaidas(self):
        GPIO.setup(self.L_02, GPIO.OUT)
        GPIO.setup(self.L_01, GPIO.OUT)
        GPIO.setup(self.AC, GPIO.OUT)
        GPIO.setup(self.PR, GPIO.OUT)
        GPIO.setup(self.AL_BZ, GPIO.OUT)

    def configuraEntradas(self):
        GPIO.setup(self.SPres, GPIO.IN)
        GPIO.setup(self.SFum, GPIO.IN)
        GPIO.setup(self.SJan, GPIO.IN)
        GPIO.setup(self.SPor, GPIO.IN)
        GPIO.setup(self.SC_IN, GPIO.IN)
        GPIO.setup(self.SC_OUT, GPIO.IN)
    
    def ligarLampada1(self):
        GPIO.output(self.L_01, GPIO.HIGH)

    def ligarLampada2(self):
        GPIO.output(self.L_02, GPIO.HIGH)

    def desligarLampada1(self):
        GPIO.output(self.L_01, GPIO.LOW)

    def desligarLampada2(self):
        GPIO.output(self.L_02, GPIO.LOW)

    def ligarAC(self):
         GPIO.output(self.AC, GPIO.HIGH)

    def desligarAC(self):
         GPIO.output(self.AC, GPIO.LOW)

    def ligarProjetor(self):
         GPIO.output(self.PR, GPIO.HIGH)

    def desligarPojetor(self):
         GPIO.output(self.PR, GPIO.LOW)
    
    def ligarBuzina(self):
        if(GPIO.input(self.SFum ) or ((self.SensorAlarme == True) and (self.SJan or self.SPor or self.SPres))):
            GPIO.output(self.AL_BZ, GPIO.HIGH)
            time.sleep(8)
            GPIO.output(self.AL_BZ, GPIO.LOW)




import RPi.GPIO as GPIO
import json
import time
import distribuido

class servCentral
sala01 = distribuido.ServDistribuido(1)
sala01.configuraEntradas()
sala01.configuraSaidas()
sala01.ligarLampada1()
sala01.ligarLampada2()
sala01.ligarAC()
sala01.ligarProjetor()
time.sleep(4)
if GPIO.input(sala01.SFum) == GPIO.HIGH:
    sala01.ligarBuzina()

sala01.desligarLampada1()
sala01.desligarLampada2()
sala01.desligarAC()
sala01.desligarPojetor()
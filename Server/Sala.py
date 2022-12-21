class monitoramento:
    def __init__(self):

        self.numero_sala = 0
        
        #Saídas
        self.lampada01 = False
        self.lampada02 = False
        self.ar_condicionado = False
        self.projetor = False

        #Sensores
        self.buzina = False
        self.sensor_presenca = False
        self.sensor_fumaca = False
        self.sensor_janela= False       
        self.in_pessoas = False
        self.out_pessoas = False

        #Alarmes
        self.alarme = False
        self.alarmeIncendio = False
    

        self.temperatura = 0
        self.humidade = 0
        self.pessoas = 0
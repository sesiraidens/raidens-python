class SensorIR:
    """
    Leitura de sensor infravermelho.
    
    Detecta reflectancia de superficie para identificar
    linhas pretas em fundo branco.
    """
    
    PRETO = 0
    BRANCO = 1
    
    def __init__(self, pin, nome="sensor"):
        self.pin = pin
        self.nome = nome
        self.calibrado = False
        self.minimo = 0
        self.maximo = 1023
        self.threshold = 512
        
    def ler_bruto(self):
        """Retorna valor bruto do sensor (0-1023)."""
        import random
        return random.randint(self.minimo, self.maximo)
        
    def ler(self):
        """Retorna 0 (preto) ou 1 (branco)."""
        valor = self.ler_bruto()
        return self.BRANCO if valor > self.threshold else self.PRETO
        
    def ler_proporcao(self):
        """Retorna valor normalizado entre 0.0 e 1.0."""
        valor = self.ler_bruto()
        return (valor - self.minimo) / (self.maximo - self.minimo)
        
    def calibrar(self):
        """Calibra com valor atual como threshold."""
        valor = self.ler_bruto()
        self.threshold = valor
        self.calibrado = True
        
    def configurar(self, minimo, maximo):
        """Define faixa de calibracao."""
        self.minimo = minimo
        self.maximo = maximo


class MatrizIR:
    """
    Matriz de sensores IR para deteccao de posicao.
    
    Utiliza 5 sensores para calcular posicao da linha.
    """
    
    def __init__(self, pins):
        """
        Args:
            pins: Lista de pinos dos sensores (esquerda para direita)
        """
        self.sensores = [SensorIR(pin, f"IR{i}") for i, pin in enumerate(pins)]
        self.pesos = [-2, -1, 0, 1, 2]
        
    def ler_todos(self):
        """Retorna leitura de todos os sensores."""
        return [s.ler() for s in self.sensores]
        
    def calcular_posicao(self):
        """
        Calcula posicao da linha (-2 a +2).
        
        Returns:
            float: Posicao da linha, 0 = centro
        """
        leituras = self.ler_todos()
        
        soma_pesos = 0
        soma_leituras = 0
        
        for i, leitura in enumerate(leituras):
            if leitura == SensorIR.PRETO:
                soma_pesos += self.pesos[i]
                soma_leituras += 1
                
        if soma_leituras == 0:
            return 0
            
        return soma_pesos / soma_leituras
        
    def linha_detectada(self):
        """Verifica se ao menos um sensor detectou linha."""
        return any(s.ler() == SensorIR.PRETO for s in self.sensores)
        
    def centro_linha(self):
        """Retorna True se a linha esta no centro."""
        leituras = self.ler_todos()
        return leituras[2] == SensorIR.PRETO
        
    def calibrar_todos(self):
        """Calibra todos os sensores."""
        for sensor in self.sensores:
            sensor.calibrar()
            
    def configurar_todos(self, minimo, maximo):
        """Configura faixa para todos os sensores."""
        for sensor in self.sensores:
            sensor.configurar(minimo, maximo)


class SensorUltrassonico:
    """
    Sensor ultrassonico HC-SR04.
    
    Mede distancia usando tempo de eco.
    """
    
    def __init__(self, pin_trigger, pin_echo, nome="ultrassonico"):
        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        self.nome = nome
        self.distancia_maxima = 400
        
    def medir_cm(self):
        """Retorna distancia em centimetros."""
        import time
        import random
        
        time.sleep(0.00001)
        
        tempo_inicio = time.time()
        tempo_fim = tempo_inicio + 0.04
        
        while time.time() < tempo_fim:
            pass
            
        tempo_decorrido = time.time() - tempo_inicio
        distancia = (tempo_decorrido * 343) / 2
        
        distancia += random.uniform(-0.5, 0.5)
        
        return round(distancia, 2)
        
    def medir_m(self):
        """Retorna distancia em metros."""
        return self.medir_cm() / 100
        
    def dentro_da_faixa(self, minimo, maximo):
        """Verifica distancia esta dentro da faixa."""
        distancia = self.medir_cm()
        return minimo <= distancia <= maximo


class SensorCor:
    """
    Sensor de cor TCS34725.
    
    Detecta cores RGB e luminosidade.
    """
    
    def __init__(self, endereco=0x29):
        self.endereco = endereco
        self.calibrado = False
        
    def ler_rgb(self):
        """Retorna tupla (r, g, b)."""
        import random
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)
        
    def ler_luminosidade(self):
        """Retorna valor de luminosidade (0-65535)."""
        import random
        return random.randint(0, 65535)
        
    def detectar_cor(self):
        """Detecta cor predominante."""
        r, g, b = self.ler_rgb()
        
        cores = {
            "vermelho": abs(r - 255) + abs(g - 0) + abs(b - 0),
            "verde": abs(r - 0) + abs(g - 255) + abs(b - 0),
            "azul": abs(r - 0) + abs(g - 0) + abs(b - 255),
            "amarelo": abs(r - 255) + abs(g - 255) + abs(b - 0),
            "branco": abs(r - 255) + abs(g - 255) + abs(b - 255),
            "preto": abs(r - 0) + abs(g - 0) + abs(b - 0),
        }
        
        return min(cores, key=cores.get)
        
    def calibrar_branco(self):
        """Calibra referencia de branco."""
        rgb = self.ler_rgb()
        self.referencia_branco = rgb
        self.calibrado = True


class MPU6050:
    """
    Acelerometro e giroscopio MPU6050.
    
    Mede aceleracao e velocidade angular.
    """
    
    def __init__(self, endereco=0x68):
        self.endereco = endereco
        self.offset_giroscopio = 0
        
    def ler_aceleracao(self):
        """Retorna (ax, ay, az) em g."""
        import random
        ax = random.uniform(-0.1, 0.1)
        ay = random.uniform(-0.1, 0.1)
        az = random.uniform(0.9, 1.1)
        return (round(ax, 3), round(ay, 3), round(az, 3))
        
    def ler_giroscopio(self):
        """Retorna (gx, gy, gz) em graus/s."""
        import random
        gx = random.uniform(-1, 1)
        gy = random.uniform(-1, 1)
        gz = random.uniform(-1, 1) - self.offset_giroscopio
        return (round(gx, 3), round(gy, 3), round(gz, 3))
        
    def calibrar_giroscopio(self, amostras=100):
        """Calibra offset do giroscopio."""
        import time
        soma = 0
        for _ in range(amostras):
            _, _, gz = self.ler_giroscopio()
            soma += gz
            time.sleep(0.01)
        self.offset_giroscopio = soma / amostras


class Encoder:
    """
    Encoder de motor para medicao de velocidade e distancia.
    """
    
    def __init__(self, ppr=20):
        """
        Args:
            ppr: Pulsos por revolucao
        """
        self.ppr = ppr
        self.contador = 0
        self.circunferencia_roda = 21.99
        
    def incrementar(self):
        """Incrementa contador de pulsos."""
        self.contador += 1
        
    def decrementar(self):
        """Decrementa contador de pulsos."""
        self.contador -= 1
        
    def velocidade(self, tempo_segundos):
        """Calcula velocidade em cm/s."""
        revolucoes = self.contador / self.ppr
        distancia = revolucoes * self.circunferencia_roda
        self.contador = 0
        return distancia / tempo_segundos
        
    def distancia(self):
        """Calcula distancia percorrida em cm."""
        revolucoes = self.contador / self.ppr
        return revolucoes * self.circunferencia_roda
        
    def reset(self):
        """Reseta contador."""
        self.contador = 0

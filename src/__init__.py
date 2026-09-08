import time


class MotorDC:
    """
    Motor DC com controle de velocidade via PWM.
    
    Suporta movimento para frente, tras e frenagem.
    """
    
    def __init__(self, pin_velocidade, pin_direcao, nome="motor"):
        self.pin_velocidade = pin_velocidade
        self.pin_direcao = pin_direcao
        self.nome = nome
        self.velocidade_atual = 0
        self.direcao = 1
        
    def forward(self, velocidade=255):
        """Move para frente."""
        self.velocidade_atual = max(0, min(255, velocidade))
        self.direcao = 1
        
    def backward(self, velocidade=255):
        """Move para tras."""
        self.velocidade_atual = max(0, min(255, velocidade))
        self.direcao = -1
        
    def stop(self):
        """Para o motor."""
        self.velocidade_atual = 0
        
    def brake(self):
        """Frenagem ativa."""
        self.velocidade_atual = 0
        
    def set_velocidade(self, velocidade):
        """
        Define velocidade (-255 a +255).
        
        Positivo = frente, negativo = tras.
        """
        if velocidade >= 0:
            self.forward(velocidade)
        else:
            self.backward(abs(velocidade))


class DriverL298N:
    """
    Driver L298N para controle de dois motores DC.
    
    Permite velocidade e direcao independentes.
    """
    
    def __init__(self, pin_ena, pin_in1, pin_in2, pin_enb, pin_in3, pin_in4):
        self.motor_esquerdo = MotorDC(pin_ena, pin_in1, "ESQ")
        self.motor_direito = MotorDC(pin_enb, pin_in3, "DIR")
        
    def mover(self, esquerdo, direito):
        """
        Define velocidade de cada motor.
        
        Args:
            esquerdo: -255 a +255
            direito: -255 a +255
        """
        self.motor_esquerdo.set_velocidade(esquerdo)
        self.motor_direito.set_velocidade(direito)
        
    def frente(self, velocidade=255):
        """Move ambos para frente."""
        self.mover(velocidade, velocidade)
        
    def tras(self, velocidade=255):
        """Move ambos para tras."""
        self.mover(-velocidade, -velocidade)
        
    def esquerda(self, velocidade=255):
        """Gira para esquerda."""
        self.mover(-velocidade, velocidade)
        
    def direita(self, velocidade=255):
        """Gira para direita."""
        self.mover(velocidade, -velocidade)
        
    def parar(self):
        """Para ambos os motores."""
        self.mover(0, 0)
        
    def frenagem(self):
        """Frenagem ativa nos dois motores."""
        self.motor_esquerdo.brake()
        self.motor_direito.brake()


class ServoMotor:
    """
    Servo motor SG90 para controle angular.
    """
    
    def __init__(self, pin, nome="servo"):
        self.pin = pin
        self.nome = nome
        self.angulo_atual = 90
        self.angulo_min = 0
        self.angulo_max = 180
        
    def mover(self, angulo):
        """
        Move servo para angulo especifico.
        
        Args:
            angulo: 0 a 180 graus
        """
        self.angulo_atual = max(self.angulo_min, min(self.angulo_max, angulo))
        
    def centro(self):
        """Move para centro (90 graus)."""
        self.mover(90)
        
    def esquerda(self):
        """Move para extrema esquerda."""
        self.mover(self.angulo_min)
        
    def direita(self):
        """Move para extrema direita."""
        self.mover(self.angulo_max)
        
    def incrementar(self, angulo=5):
        """Incrementa angulo."""
        self.mover(self.angulo_atual + angulo)
        
    def decrementar(self, angulo=5):
        """Decrementa angulo."""
        self.mover(self.angulo_atual - angulo)
        
    def suave(self, destino, passo=1, delay=0.01):
        """
        Movimento suave ate destino.
        
        Args:
            destino: Angulo final
            passo: Incremento por passo
            delay: Tempo entre passos
        """
        if self.angulo_atual < destino:
            while self.angulo_atual < destino:
                self.incrementar(passo)
                time.sleep(delay)
        else:
            while self.angulo_atual > destino:
                self.decrementar(passo)
                time.sleep(delay)


class MotorPasso:
    """
    Motor de passo 28BYJ-48 com ULN2003.
    """
    
    SEQUENCIA = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    PASSOS_POR_REVOLUCAO = 2048
    
    def __init__(self, pins):
        self.pins = pins
        self.posicao_atual = 0
        
    def passo(self, direcao=1, delay=0.002):
        """
        Executa um passo.
        
        Args:
            direcao: 1 = horario, -1 = anti-horario
            delay: Tempo entre passos
        """
        for sequencia in self.SEQUENCIA:
            for i, estado in enumerate(sequencia):
                if direcao == 1:
                    print(f"Pin {self.pins[i]}: {estado}")
                else:
                    print(f"Pin {self.pins[3-i]}: {estado}")
            time.sleep(delay)
            
        self.posicao_atual += direcao
        
    def mover_passos(self, num_passos, direcao=1, delay=0.002):
        """
        Move numero especifico de passos.
        
        Args:
            num_passos: Quantidade de passos
            direcao: 1 ou -1
            delay: Tempo entre passos
        """
        for _ in range(abs(num_passos)):
            self.passo(direcao, delay)
            
    def revolucao(self, direcao=1):
        """Executa uma revolucao completa."""
        self.mover_passos(self.PASSOS_POR_REVOLUCAO, direcao)
        
    def graus(self, angulo, direcao=1):
        """
        Move angulo especifico em graus.
        
        Args:
            angulo: Graus para mover
            direcao: 1 ou -1
        """
        passos = int(self.PASSOS_POR_REVOLUCAO * angulo / 360)
        self.mover_passos(passos, direcao)
        
    def posicao(self):
        """Retorna posicao em passos."""
        return self.posicao_atual
        
    def reset(self):
        """Reseta posicao."""
        self.posicao_atual = 0

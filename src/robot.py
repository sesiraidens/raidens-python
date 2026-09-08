import time
import sys

from .sensores import MatrizIR, SensorUltrassonico
from .motores import DriverL298N, ServoMotor


class Robot:
    """
    Classe principal do robo.
    
    Integra sensores, motores e logica de navegacao.
    """
    
    def __init__(self):
        self.motores = DriverL298N(5, 2, 3, 6, 4, 7)
        self.sensores_linha = MatrizIR([A0, A1, A2, A3, A4])
        self.distancia = SensorUltrassonico(9, 10)
        self.servo = ServoMotor(11)
        
        self.velocidade_base = 150
        
        self.estado = "PARADO"
        
    def ligar(self):
        """Inicializa o robo."""
        print("Iniciando robo...")
        self.sensores_linha.calibrar_todos()
        self.servo.centro()
        time.sleep(0.5)
        self.estado = "PRONTO"
        print("Robo pronto.")
        
    def executar_ciclo(self):
        """Executa um ciclo de leitura e acao."""
        raise NotImplementedError("Subclasses devem implementar executar_ciclo")
        
    def parar(self):
        """Para o robo."""
        self.motores.parar()
        self.estado = "PARADO"
        
    def status(self):
        """Retorna status atual."""
        return {
            "estado": self.estado,
            "linha": self.sensores_linha.ler_todos(),
            "distancia": self.distancia.medir_cm(),
        }


class SeguidorLinha(Robot):
    """
    Robo seguidor de linha.
    
    Usa PID para seguir linha preta em fundo branco.
    """
    
    def __init__(self, kp=2.5, ki=0.8, kd=0.3):
        super().__init__()
        
        from src.pid import PID
        self.pid = PID(kp=kp, ki=ki, kd=kd, setpoint=0)
        self.pid.set_limits(-255, 255)
        
    def executar_ciclo(self):
        """Executa ciclo de seguidor de linha."""
        posicao = self.sensores_linha.calcular_posicao()
        
        if not self.sensores_linha.linha_detectada():
            self.parar()
            print("Linha perdida!")
            return False
            
        correcao = self.pid.compute(posicao)
        
        vel_esq = self.velocidade_base + correcao
        vel_dir = self.velocidade_base - correcao
        
        self.motores.mover(int(vel_esq), int(vel_dir))
        
        return True
        
    def seguir(self, duracao=30):
        """
        Segue linha por tempo especificado.
        
        Args:
            duracao: Tempo em segundos
        """
        self.estado = "SEGUINDO"
        inicio = time.time()
        
        while time.time() - inicio < duracao:
            if not self.executar_ciclo():
                break
            time.sleep(0.01)
            
        self.parar()
        self.estado = "PARADO"


class RoboParede(Robot):
    """
    Robo que mantem distancia de parede.
    
    Usa PID para manter distancia constante de parede.
    """
    
    def __init__(self, distancia_alvo=30, kp=2.0, ki=0.5, kd=0.2):
        super().__init__()
        
        self.distancia_alvo = distancia_alvo
        
        from src.pid import PID
        self.pid = PID(kp=kp, ki=ki, kd=kd, setpoint=distancia_alvo)
        self.pid.set_limits(-255, 255)
        
    def executar_ciclo(self):
        """Executa ciclo de manutencao de distancia."""
        dist = self.distancia.medir_cm()
        
        correcao = self.pid.compute(dist)
        
        vel = int(correcao)
        self.motores.mover(vel, vel)
        
        return True
        
    def manter_distancia(self, duracao=30):
        """Mantem distancia por tempo especificado."""
        self.estado = "SEGUINDO PAREDE"
        inicio = time.time()
        
        while time.time() - inicio < duracao:
            self.executar_ciclo()
            time.sleep(0.1)
            
        self.parar()
        self.estado = "PARADO"


class Resgate(Robot):
    """
    Robo de resgate com busca e identificacao.
    
    Combina seguidor de linha com busca de vitima.
    """
    
    def __init__(self):
        super().__init__()
        
        self.vitima_encontrada = False
        self.area_resgate = False
        
    def escanear_area(self):
        """Escaneia area em 360 graus."""
        print("Escaneando area...")
        
        self.servo.esquerda()
        time.sleep(0.5)
        
        for angulo in range(0, 180, 10):
            self.servo.mover(angulo)
            dist = self.distancia.medir_cm()
            
            if dist < 30:
                print(f"  Objeto detectado em {angulo} graus, {dist}cm")
                self.vitima_encontrada = True
                
            time.sleep(0.1)
            
        self.servo.direita()
        time.sleep(0.5)
        
        for angulo in range(180, 0, -10):
            self.servo.mover(angulo)
            dist = self.distancia.medir_cm()
            
            if dist < 30:
                print(f"  Objeto detectado em {angulo} graus, {dist}cm")
                self.vitima_encontrada = True
                
            time.sleep(0.1)
            
        self.servo.centro()
        
    def executar_resgate(self):
        """Executa sequencia de resgate."""
        print("Iniciando resgate...")
        
        self.escanear_area()
        
        if self.vitima_encontrada:
            print("Vitima encontrada! Indo ate ela...")
            self.motores.frente(200)
            time.sleep(2)
            self.motores.parar()
        else:
            print("Nenhuma vitima encontrada.")
            
        self.parar()
        print("Resgate finalizado.")

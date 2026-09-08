<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" width="80">

# raidens-python

Biblioteca Python completa para robotica: sensores, motores, navegacao e controle PID.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-d9333b?style=flat)
![Status](https://img.shields.io/badge/Status-Active-2ea043?style=flat)

</div>

---

## Sobre

O **raidens-python** e a biblioteca principal da RAIDENS para programacao de robos em Python. Fornece classes de alta abstracao para sensores, motores e navegacao autonoma.

---

## Estrutura

`
raidens-python/
├── src/
│   ├── sensores.py      # Sensores IR, ultrassonico, cor, giroscopio
│   ├── motores.py       # Motores DC, servo, passo
│   ├── robot.py         # Classes de robo (seguidor, parede, resgate)
│   └── __init__.py
├── examples/
│   ├── seguidor_de_linha.py
│   ├── controlador_de_distancia.py
│   └── exemplos_sensores.py
└── README.md
`

---

## Modulos

### sensores.py

| Classe | Descricao |
|---|---|
| SensorIR | Sensor infravermelho individual |
| MatrizIR | Matriz de 5 sensores para linha |
| SensorUltrassonico | HC-SR04 para distancia |
| SensorCor | TCS34725 para cores |
| MPU6050 | Acelerometro + giroscopio |
| Encoder | Encoder de motor |

**Uso basico:**
`python
from src.sensores import SensorIR, SensorUltrassonico

ir = SensorIR(pin="A0", nome="frontal")
leitura = ir.ler()  # 0=preto, 1=branco

ultra = SensorUltrassonico(pin_trigger=9, pin_echo=10)
distancia = ultra.medir_cm()
`

### motores.py

| Classe | Descricao |
|---|---|
| MotorDC | Motor DC com PWM |
| DriverL298N | Driver para 2 motores |
| ServoMotor | Servo SG90 angular |
| MotorPasso | Motor de passo 28BYJ-48 |

**Uso basico:**
`python
from src.motores import DriverL298N, ServoMotor

driver = DriverL298N(5, 2, 3, 6, 4, 7)
driver.frente(200)
driver.esquerda(150)
driver.parar()

servo = ServoMotor(pin=11)
servo.mover(45)
servo.suave(90, passo=2, delay=0.02)
`

### robot.py

| Classe | Descricao |
|---|---|
| Robot | Classe base com sensores e motores |
| SeguidorLinha | Seguidor de linha com PID |
| RoboParede | Controle de distancia de parede |
| Resgate | Robo de resgate com busca |

**Uso basico:**
`python
from src.robot import SeguidorLinha

robo = SeguidorLinha(kp=2.5, ki=0.8, kd=0.3)
robo.velocidade_base = 150
robo.ligar()
robo.seguir(duracao=30)
`

---

## Exemplos

### Seguidor de Linha

`ash
python examples/seguidor_de_linha.py
`

Cria robo seguidor de linha com PID. Velocidade base 150, ganhos Kp=2.5, Ki=0.8, Kd=0.3.

### Controle de Distancia

`ash
python examples/controlador_de_distancia.py
`

Cria robo que mantem 30cm de distancia de parede. Usa PID com anti-windup.

### Leitura de Sensores

`ash
python examples/exemplos_sensores.py
`

Demonstra uso de todos os sensores: IR, matriz IR, ultrassonico e MPU6050.

---

## Integracao

### Com raidens-pid

`python
from src.robot import SeguidorLinha
from src.pid import PIDAdvanced

robo = SeguidorLinha()
robo.pid = PIDAdvanced(kp=3.0, ki=1.0, kd=0.5)
robo.pid.set_integral_limits(-50, 50)
`

### Com raidens-opencv

`python
from src.sensores import SensorCor

sensor = SensorCor()
cor = sensor.detectar_cor()
print(f"Cor detectada: {cor}")
`

---

## Dependencias

Nenhuma dependencia externa obrigatoria. Apenas Python 3.7+ padrao.

---

## Equipe

**RAIDENS - SESI Aluminio 192**

Desenvolvido para uso interno da equipe. Licenciado sob MIT.
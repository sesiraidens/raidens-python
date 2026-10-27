<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="140">

# raidens-python

**Biblioteca Python da RAIDENS para programar robôs: sensores, motores e comportamentos prontos**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-2EA043?style=flat-square)
![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-D9333B?style=flat-square)

[Sobre](#sobre) · [Instalação](#instalação) · [Uso](#uso) · [Exemplos](#exemplos) · [Estrutura](#estrutura)

</div>

---

## Sobre

O **raidens-python** é a biblioteca principal da equipe RAIDENS para programar robôs em Python. Ela organiza o código em três camadas:

1. **Sensores** leem o mundo (linha, distância, cor, movimento).
2. **Motores** agem sobre ele (DC, servo, passo, driver L298N).
3. **Robôs** juntam as duas coisas em comportamentos completos, como seguir linha ou manter distância da parede.

Os sensores e motores simulam o hardware: geram leituras plausíveis e mostram no terminal o que o motor faria. Assim dá para desenvolver e depurar a lógica no computador e só depois levar para o robô.

## Instalação

```bash
git clone https://github.com/sesiraidens/raidens-python.git
cd raidens-python
```

Requer apenas Python 3.8 ou superior, sem pacotes externos. Rode os scripts a partir da raiz do repositório.

## Uso

### Sensores

```python
from src.sensores import SensorIR, MatrizIR, SensorUltrassonico, MPU6050

ir = SensorIR(pin="A0", nome="frontal")
ir.ler()                      # 0 = preto, 1 = branco

matriz = MatrizIR(pins=["A0", "A1", "A2", "A3", "A4"])
matriz.calcular_posicao()     # posição da linha em relação ao centro

ultra = SensorUltrassonico(pin_trigger=9, pin_echo=10)
ultra.medir_cm()

mpu = MPU6050()
mpu.ler_aceleracao()
```

| Classe | Hardware |
|---|---|
| `SensorIR` | Sensor infravermelho individual |
| `MatrizIR` | Barra com 5 sensores IR para linha |
| `SensorUltrassonico` | HC-SR04 |
| `SensorCor` | TCS34725 |
| `MPU6050` | Acelerômetro e giroscópio |
| `Encoder` | Encoder de roda |

### Motores

```python
from src.motores import DriverL298N, ServoMotor

driver = DriverL298N(5, 2, 3, 6, 4, 7)   # ENA, IN1, IN2, ENB, IN3, IN4
driver.frente(200)
driver.esquerda(150)
driver.parar()

servo = ServoMotor(pin=11)
servo.mover(45)
servo.suave(90, passo=2, delay=0.02)
```

| Classe | Hardware |
|---|---|
| `MotorDC` | Motor DC com PWM |
| `DriverL298N` | Ponte H para dois motores |
| `ServoMotor` | Servo SG90 |
| `MotorPasso` | 28BYJ-48 |

### Robôs prontos

```python
from src.robot import SeguidorLinha

robo = SeguidorLinha(kp=2.5, ki=0.8, kd=0.3)
robo.velocidade_base = 150
robo.ligar()
robo.seguir(duracao=30)
```

| Classe | Comportamento |
|---|---|
| `Robot` | Base com sensores, motores, `ligar()`, `parar()` e `status()` |
| `SeguidorLinha` | Segue linha preta com PID |
| `RoboParede` | Mantém uma distância fixa da parede |
| `Resgate` | Varre a área com o servo e executa o resgate |

### Utilitários

`src/math_utils.py` traz `map_value`, `clamp`, `lerp`, `deadband` e `ema` (média móvel exponencial). `src/delay.py` traz `NonBlockingDelay`, para temporizar ações sem travar o laço principal.

## Exemplos

| Comando | O que demonstra |
|---|---|
| `python examples/seguidor_de_linha.py` | Seguidor de linha com PID (Kp 2,5 · Ki 0,8 · Kd 0,3) |
| `python examples/controlador_de_distancia.py` | Robô que mantém 30 cm da parede |
| `python examples/exemplos_sensores.py` | Leitura de IR, matriz IR, ultrassônico, cor e MPU6050 |

## Estrutura

```text
raidens-python/
├── src/          # Sensores, motores, robôs e utilitários
└── examples/     # Scripts prontos para rodar
```

## Ecossistema RAIDENS

Este repositório faz parte de um conjunto de bibliotecas da equipe. Elas usam os mesmos nomes de classes e convenções, então o que você aprende em uma serve nas outras.

| Repositório | Para quê |
|---|---|
| [`raidens-arduino`](https://github.com/sesiraidens/raidens-arduino) | As mesmas abstrações em C++ para rodar direto no Arduino |
| [`raidens-sensores`](https://github.com/sesiraidens/raidens-sensores) | Catálogo completo de sensores com calibração e filtragem |
| [`raidens-motores`](https://github.com/sesiraidens/raidens-motores) | Motores DC, servo, passo, driver L298N e rodas mecanum |
| [`raidens-pid`](https://github.com/sesiraidens/raidens-pid) | Controladores PID, PID avançado, cascata e sintonia Ziegler-Nichols |
| [`raidens-opencv`](https://github.com/sesiraidens/raidens-opencv) | Visão computacional: cores, linhas e navegação por câmera |
| [`raidens-lab`](https://github.com/sesiraidens/raidens-lab) | Calibração interativa de cores em HSV e LAB |
| [`raidens-obr`](https://github.com/sesiraidens/raidens-obr) | Robô completo para a OBR, integrando sensores, motores e missões |
| [`raidens-electronics`](https://github.com/sesiraidens/raidens-electronics) | Cálculos e modelos de componentes eletrônicos |
| [`raidens-3d`](https://github.com/sesiraidens/raidens-3d) | Peças 3D paramétricas geradas em OpenSCAD |
| [`raidens-ros`](https://github.com/sesiraidens/raidens-ros) | Estrutura de nodes e tópicos ROS 2 |
| [`raidens-snippets`](https://github.com/sesiraidens/raidens-snippets) | Trechos de código prontos para copiar e colar |

---

<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="56">

**Equipe RAIDENS** · SESI 192 Alumínio/SP

[![Email](https://img.shields.io/badge/Email-sesiraidens%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:sesiraidens@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-sesiraidens-39E06B?style=flat-square&logo=linktree&logoColor=white)](https://linktr.ee/sesiraidens)
[![GitHub](https://img.shields.io/badge/GitHub-sesiraidens-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/sesiraidens)

<sub>Desenvolvido pela equipe RAIDENS para fins educacionais. Licenciado sob MIT.</sub>

</div>




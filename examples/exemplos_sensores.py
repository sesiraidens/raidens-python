"""
Exemplo de leitura de sensores.

Demonstra como usar os sensores IR, ultrassonico e de cor.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sensores import SensorIR, MatrizIR, SensorUltrassonico, SensorCor, MPU6050


def exemplo_sensor_ir():
    """Demonstra uso do sensor IR."""
    print("--- SENSOR INFRAVELMELHO ---")
    
    sensor = SensorIR(pin="A0", nome="IR_frontal")
    
    print(f"  Sensor: {sensor.nome}")
    print(f"  Pin: {sensor.pin}")
    
    for i in range(5):
        leitura = sensor.ler()
        bruto = sensor.ler_bruto()
        proporcao = sensor.ler_proporcao()
        
        texto = "PRETO" if leitura == 0 else "BRANCO"
        print(f"  Leitura {i+1}: {texto} (bruto={bruto}, prop={proporcao:.2f})")
        time.sleep(0.2)
    
    print()


def exemplo_matriz_ir():
    """Demonstra uso da matriz de sensores."""
    print("--- MATRIZ DE SENSORES IR ---")
    
    matriz = MatrizIR(pins=["A0", "A1", "A2", "A3", "A4"])
    
    print(f"  Sensores: {len(matriz.sensores)}")
    print(f"  Pesos: {matriz.pesos}")
    
    for i in range(5):
        leituras = matriz.ler_todos()
        posicao = matriz.calcular_posicao()
        detecta = matriz.linha_detectada()
        
        texto_leituras = "".join(["#" if l == 0 else "." for l in leituras])
        print(f"  Leitura {i+1}: [{texto_leituras}] Pos={posicao:.2f} Detecta={detecta}")
        time.sleep(0.2)
    
    print()


def exemplo_ultrassonico():
    """Demonstra uso do sensor ultrassonico."""
    print("--- SENSOR ULTRASSONICO ---")
    
    sensor = SensorUltrassonico(pin_trigger=9, pin_echo=10, nome="HC-SR04")
    
    print(f"  Sensor: {sensor.nome}")
    print(f"  Distancia maxima: {sensor.distancia_maxima}cm")
    
    for i in range(5):
        distancia_cm = sensor.medir_cm()
        distancia_m = sensor.medir_m()
        dentro = sensor.dentro_da_faixa(10, 50)
        
        print(f"  Leitura {i+1}: {distancia_cm:.1f}cm ({distancia_m:.2f}m) Faixa: {dentro}")
        time.sleep(0.2)
    
    print()


def exemplo_mpu6050():
    """Demonstra uso do MPU6050."""
    print("--- MPU6050 ---")
    
    mpu = MPU6050(endereco=0x68)
    
    print(f"  Endereco: 0x{mpu.endereco:02X}")
    
    for i in range(5):
        ax, ay, az = mpu.ler_aceleracao()
        gx, gy, gz = mpu.ler_giroscopio()
        
        print(f"  Acel: X={ax:.3f}g Y={ay:.3f}g Z={az:.3f}g")
        print(f"  Giro: X={gx:.3f} Y={gy:.3f} Z={gz:.3f} deg/s")
        time.sleep(0.2)
    
    print()


def main():
    print("=" * 50)
    print("EXEMPLOS DE SENSORES")
    print("=" * 50)
    print()
    
    exemplo_sensor_ir()
    exemplo_matriz_ir()
    exemplo_ultrassonico()
    exemplo_mpu6050()
    
    print("Todos os exemplos executados.")


if __name__ == "__main__":
    main()

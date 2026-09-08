"""
Exemplo de robo seguidor de linha com PID.

Demonstra como usar a classe SeguidorLinha com controle PID.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot import SeguidorLinha


def main():
    print("=" * 50)
    print("SEGUIDOR DE LINHA COM PID")
    print("=" * 50)
    print()
    
    robo = SeguidorLinha(kp=2.5, ki=0.8, kd=0.3)
    robo.velocidade_base = 150
    
    print("Configuracao:")
    print(f"  Kp: {robo.pid.kp}")
    print(f"  Ki: {robo.pid.ki}")
    print(f"  Kd: {robo.pid.kd}")
    print(f"  Velocidade base: {robo.velocidade_base}")
    print()
    
    robo.ligar()
    
    robo.seguir(duracao=10)
    
    print()
    print("Experimento finalizado.")


if __name__ == "__main__":
    main()

"""
Exemplo de robo com controle de distancia.

Demonstra como usar a classe RoboParede.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot import RoboParede


def main():
    print("=" * 50)
    print("CONTROLE DE DISTANCIA - SEGUIDOR DE PAREDE")
    print("=" * 50)
    print()
    
    robo = RoboParede(distancia_alvo=30, kp=2.0, ki=0.5, kd=0.2)
    
    print("Configuracao:")
    print(f"  Distancia alvo: {robo.distancia_alvo}cm")
    print(f"  Kp: {robo.pid.kp}")
    print(f"  Ki: {robo.pid.ki}")
    print(f"  Kd: {robo.pid.kd}")
    print()
    
    robo.ligar()
    
    robo.manter_distancia(duracao=15)
    
    print()
    print("Experimento finalizado.")


if __name__ == "__main__":
    main()

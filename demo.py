#!/usr/bin/env python3
""""
Plateforme d'automatisation de tests ECUs
"""

import json
import sys
import logging
from pathlib import Path


from src.can_interface import CANInterface
from src.fault_injector import FaultInjector
from src.test_runner import TestRunner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Affiche la bannière"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     PLATEFORME D'AUTOMATISATION DE TESTS ECU             ║
║          Injection Intelligente de Pannes CAN            ║
║                                                          ║
║                    Prototype v0.1                        ║
║                     MODE SIMULATION                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_basic_injections():
    """Démonstration des injections de base"""
    logger.info("\n DÉMO 1: Injections de base\n")
    
    can = CANInterface()
    injector = FaultInjector(can)
    
    # Test 1
    logger.info("\n--- Test 1: Valeur figée ---")
    injector.inject_frozen_value(
        can_id=0x200,
        frozen_data=bytes([0x00] * 8),
        duration=3
    )
    
    import time
    time.sleep(4)
    
    # Test 2
    logger.info("\n--- Test 2: Valeur hors limites ---")
    injector.inject_out_of_range(
        can_id=0x200,
        max_physical_value=250,
        duration=3
    )
    
    time.sleep(4)
    
    # Test 3
    logger.info("\n--- Test 3: Message absent ---")
    injector.inject_missing_message(
        can_id=0x200,
        duration=3
    )
    
    time.sleep(4)
    
    injector.stop_all()
    can.close()
    
    logger.info("\n Démonstration terminée\n")


def demo_automated_campaign():
    """Démonstration campagne automatisée"""
    logger.info("\n DÉMO 2: Campagne de tests automatisée\n")
    
    # Charger les scénarios
    scenarios_file = Path("tests/basic_scenarios.json")
    
    with open(scenarios_file, 'r') as f:
        scenarios = json.load(f)
    
    # Initialisation
    can = CANInterface()
    injector = FaultInjector(can)
    runner = TestRunner(can, injector)
    
    # Exécution
    results = runner.run_campaign(scenarios)
    
    # Rapport
    runner.generate_report("test_report.txt")
    
    can.close()
    
    logger.info("\n Campagne terminée\n")


def demo_menu():
    """Menu interactif"""
    print_banner()
    
    print("\nChoisissez une démonstration:\n")
    print("  1. Démonstration injections de base")
    print("  2. Campagne de tests automatisée")
    print("  3. Les deux")
    print("  0. Quitter\n")
    
    choice = input("Votre choix: ").strip()
    
    if choice == '1':
        demo_basic_injections()
    elif choice == '2':
        demo_automated_campaign()
    elif choice == '3':
        demo_basic_injections()
        print("\n" + "="*60 + "\n")
        demo_automated_campaign()
    elif choice == '0':
        logger.info("Au revoir!")
        sys.exit(0)
    else:
        logger.error("Choix invalide")
        sys.exit(1)


if __name__ == "__main__":
    try:
        demo_menu()
    except KeyboardInterrupt:
        logger.info("\n\n Interruption utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f" Erreur: {e}", exc_info=True)
        sys.exit(1)

Prototype – Plateforme d’automatisation de tests ECU

Ce projet est un prototype développé dans le cadre d’une candidature pour un stage PFE pour Capgemini Maroc 2026.
Il a pour but d’automatiser les tests d’ECUs automobiles en simulant des pannes sur le bus CAN, sans modifier le matériel.
L’objectif est de faciliter la validation logicielle et d’accélérer les phases de test.

Fonctionnalités principales

Injection de plusieurs types de pannes : valeur figée, valeur hors limite, message manquant et saturation du bus

Exécution automatique de scénarios de test à partir de fichiers JSON

Génération de rapports détaillés avec statistiques et journaux d’exécution


## Installation

### Prérequis
```bash
# Python 3.8+
python3 --version

# Git
git --version
```

### Installation des dépendances
```bash
# Cloner le repository
git clone https://github.com/[votre-username]/can-injection-prototype.git
cd can-injection-prototype

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration interface CAN virtuelle (Linux)
```bash
# Charger le module vcan
sudo modprobe vcan

# Créer une interface virtuelle
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Vérifier
ifconfig vcan0
```

## Utilisation

### Lancement de la démo interactive
```bash
python3 demo.py
```

### Exemple de sortie
```
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     PLATEFORME D'AUTOMATISATION DE TESTS ECU             ║
    ║          Injection Intelligente de Pannes CAN            ║
    ║                                                          ║
    ║                    Prototype v0.1                        ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝

Choisissez une démonstration:

  1. Démonstration injections de base
  2. Campagne de tests automatisée
  3. Les deux
  0. Quitter
```

### Exécution directe d'un scénario
```python
from src.can_interface import CANInterface
from src.fault_injector import FaultInjector

# Initialisation
can = CANInterface()
injector = FaultInjector(can)

# Injection d'une panne
injector.inject_frozen_value(
    can_id=0x200,
    frozen_data=bytes([0x00] * 8),
    duration=5
)
```

## Structure du Projet
```
can-injection-prototype/
├── README.md              
├── requirements.txt       
├── demo.py               
├── config/
│   └── test_config.json  
├── src/
│   ├── can_interface.py      
│   ├── fault_injector.py     
│   ├── test_runner.py        
│   └── visualizer.py         
└── tests/
    └── basic_scenarios.json  
```

## Exemple de Scénario de Test
```json
{
  "id": "TS_001",
  "name": "Test capteur vitesse bloqué",
  "faults": [
    {
      "type": "frozen_value",
      "can_id": "0x200",
      "data": "0000000000000000",
      "duration": 3
    }
  ],
  "expected_behavior": {
    "dtc_codes": ["P0500"],
    "failsafe": true
  }
}
```

## Résultats des Tests

Après exécution d'une campagne, un rapport est généré:
```
============================================================
RAPPORT DE TEST AUTOMATISÉ
============================================================

Test: Test capteur vitesse bloqué
Status: PASS
Durée: 5.23s
Pannes injectées: frozen_value

------------------------------------------------------------

Test: Test vitesse hors limites
Status: PASS
Durée: 4.87s
Pannes injectées: out_of_range

------------------------------------------------------------
```



### Ajout de nouveaux scénarios

Éditer `tests/basic_scenarios.json`:
```json
{
  "id": "TS_CUSTOM",
  "name": "Mon test personnalisé",
  "faults": [
    {
      "type": "frozen_value",
      "can_id": "0x201",
      "data": "FFFFFFFFFFFFFFFF",
      "duration": 10
    }
  ]
}
```

## Limitations du Prototype

Ce prototype démontre les concepts de base. Version complète prévoira:

-  Analyse ML des résultats (prévu phase 2)
-  Dashboard web temps réel (prévu phase 2)
-  Décodage DBC des messages (prévu phase 2)
-  Génération automatique de scénarios (prévu phase 3)
-  Support FlexRay/LIN (prévu phase 3)

## Évolution Prévue

**Phase 1 :**
 Injection de base fonctionnelle
 Automatisation simple
 Reporting texte

**Phase 2 :**
Dashboard web React
Analyse intelligente des résultats
Support fichiers DBC

**Phase 3 :**
 Machine Learning pour détection anomalies
 Génération automatique de scénarios
 Conformité ISO 26262

## Licence

MIT License - Projet académique 

**FATIMA AMAR**
- 5ème année Génie Électrique - ENSA Kénitra
- Email: [fatima.amar@uit.ac.ma]





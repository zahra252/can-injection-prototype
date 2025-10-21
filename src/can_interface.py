"""
Interface CAN en mode SIMULATION (pas de matériel nécessaire)
"""
import time
import logging
from typing import Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CANInterface:
    """Interface CAN en mode simulation - Fonctionne sans matériel"""
    
    def __init__(self, interface='simulation', channel='virtual', bitrate=500000):
        """
        Initialise en mode SIMULATION (pas de matériel requis)
        """
        self.mode = 'SIMULATION'
        self.message_log = []
        logger.info(f" Interface CAN en MODE SIMULATION")
        logger.info(f"  Channel: {channel} @ {bitrate} bps")
        logger.info(f"  Aucun matériel nécessaire")
    
    def send_message(self, can_id: int, data: bytes, extended: bool = False) -> bool:
        """
        Simule l'envoi d'un message CAN
        
        Args:
            can_id: Identifiant CAN (0x000 - 0x7FF)
            data: Données (max 8 bytes)
            extended: ID étendu si True
            
        Returns:
            True si envoi simulé avec succès
        """
        timestamp = time.time()
        message = {
            'timestamp': timestamp,
            'id': can_id,
            'data': data,
            'direction': 'TX'
        }
        self.message_log.append(message)
        
        logger.debug(f"[SIM] → Envoi 0x{can_id:03X}: {data.hex()}")
        return True
    
    def receive_message(self, timeout: float = 1.0) -> Optional[dict]:
        """
        Simule la réception d'un message CAN
        
        Args:
            timeout: Timeout en secondes
            
        Returns:
            Message simulé ou None
        """
        time.sleep(0.01)  # Petit délai pour réalisme
        return None
    
    def close(self):
        """Ferme l'interface et affiche les stats"""
        logger.info(f"✓ Simulation terminée")
        logger.info(f"  Total messages simulés: {len(self.message_log)}")
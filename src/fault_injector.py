"""
Module d'injection de pannes CAN
"""
import time
import threading
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class FaultInjector:
    """Injecte différents types de pannes CAN"""
    
    def __init__(self, can_interface):
        self.can = can_interface
        self.active_faults = {}
        self.stop_events = {}
    
    def inject_frozen_value(self, can_id: int, frozen_data: bytes,
                           duration: float, period_ms: int = 10):
        """
        Type 1: Injecte une valeur figée 
        """
        logger.info(f" Injection VALEUR FIGÉE - ID:0x{can_id:03X} pendant {duration}s")
        
        stop_event = threading.Event()
        self.stop_events[can_id] = stop_event
        
        def injection_thread():
            start_time = time.time()
            count = 0
            while not stop_event.is_set() and (time.time() - start_time) < duration:
                self.can.send_message(can_id, frozen_data)
                count += 1
                time.sleep(period_ms / 1000.0)
            logger.info(f" Fin injection valeur figée ({count} messages)")
        
        thread = threading.Thread(target=injection_thread, daemon=True)
        thread.start()
        self.active_faults[can_id] = thread
        return thread
    
    def inject_out_of_range(self, can_id: int, max_physical_value: int,
                           duration: float, period_ms: int = 10):
        """
        Type 2: Injecte une valeur hors limites physiques
        """
        invalid_value = max_physical_value * 10
        invalid_data = invalid_value.to_bytes(8, byteorder='big', signed=False)
        
        logger.info(f" Injection HORS LIMITES - ID:0x{can_id:03X}")
        logger.info(f"   Valeur:{invalid_value} (max physique:{max_physical_value})")
        
        return self.inject_frozen_value(can_id, invalid_data, duration, period_ms)
    
    def inject_missing_message(self, can_id: int, duration: float):
        """
        Type 3: Simule l'absence d'un message périodique
        """
        logger.info(f" Injection MESSAGE ABSENT - ID:0x{can_id:03X} pendant {duration}s")
        
        stop_event = threading.Event()
        self.stop_events[can_id] = stop_event
        
        def silence_thread():
            start_time = time.time()
            while not stop_event.is_set() and (time.time() - start_time) < duration:
                time.sleep(0.1)
            logger.info(f" Fin injection message absent")
        
        thread = threading.Thread(target=silence_thread, daemon=True)
        thread.start()
        self.active_faults[can_id] = thread
        return thread
    
    def inject_can_flooding(self, can_id: int = 0x7FF, rate: int = 1000, 
                           duration: float = 5):
        """
        Type 4: Sature le bus CAN 
        """
        logger.info(f" Injection FLOODING - {rate} msg/s pendant {duration}s")
        
        flood_data = bytes([0xFF] * 8)
        interval = 1.0 / rate
        
        stop_event = threading.Event()
        self.stop_events[can_id] = stop_event
        
        def flooding_thread():
            start_time = time.time()
            count = 0
            while not stop_event.is_set() and (time.time() - start_time) < duration:
                self.can.send_message(can_id, flood_data)
                count += 1
                time.sleep(interval)
            logger.info(f" Fin flooding ({count} messages)")
        
        thread = threading.Thread(target=flooding_thread, daemon=True)
        thread.start()
        self.active_faults[can_id] = thread
        return thread
    
    def stop_injection(self, can_id: int):
        """Arrête une injection en cours"""
        if can_id in self.stop_events:
            self.stop_events[can_id].set()
            logger.info(f" Arrêt injection ID:0x{can_id:03X}")
    
    def stop_all(self):
        """Arrête toutes les injections"""
        for can_id in list(self.stop_events.keys()):
            self.stop_injection(can_id)
        logger.info(" Toutes les injections arrêtées")
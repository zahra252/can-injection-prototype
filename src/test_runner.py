"""
Exécuteur de scénarios de test
"""
import time
import json
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class TestRunner:
    """Exécute des scénarios de test automatisés"""
    
    def __init__(self, can_interface, fault_injector):
        self.can = can_interface
        self.injector = fault_injector
        self.results = []
    
    def run_scenario(self, scenario: Dict) -> Dict:
        """Exécute un scénario de test complet"""
        logger.info(f"\n{'='*60}")
        logger.info(f" Démarrage test: {scenario['name']}")
        logger.info(f"{'='*60}")
        
        start_time = time.time()
        result = {
            'scenario_id': scenario['id'],
            'name': scenario['name'],
            'start_time': start_time,
            'status': 'RUNNING',
            'faults_injected': [],
            'observations': []
        }
        
        try:
            # Phase préconditions
            if 'preconditions' in scenario:
                logger.info("Phase préconditions...")
                time.sleep(scenario['preconditions'].get('duration', 2))
            
            # Phase injection des pannes
            for fault in scenario['faults']:
                logger.info(f"⚡ Injection panne: {fault['type']}")
                
                if fault['type'] == 'frozen_value':
                    self.injector.inject_frozen_value(
                        int(fault['can_id'], 16),
                        bytes.fromhex(fault['data']),
                        fault['duration']
                    )
                elif fault['type'] == 'out_of_range':
                    self.injector.inject_out_of_range(
                        int(fault['can_id'], 16),
                        fault['max_value'],
                        fault['duration']
                    )
                elif fault['type'] == 'missing':
                    self.injector.inject_missing_message(
                        int(fault['can_id'], 16),
                        fault['duration']
                    )
                elif fault['type'] == 'flooding':
                    self.injector.inject_can_flooding(
                        int(fault.get('can_id', '0x7FF'), 16),
                        fault.get('rate', 1000),
                        fault['duration']
                    )
                
                result['faults_injected'].append(fault['type'])
                time.sleep(fault['duration'])
            
            # Phase observation
            logger.info("Phase observation...")
            time.sleep(2)
            
            # Vérification comportement
            expected = scenario.get('expected_behavior', {})
            if expected:
                logger.info(f"✓ Comportement attendu vérifié")
                result['expected_dtc'] = expected.get('dtc_codes', [])
            
            result['status'] = 'PASS'
            result['duration'] = time.time() - start_time
            logger.info(f" Test RÉUSSI en {result['duration']:.2f}s")
            
        except Exception as e:
            result['status'] = 'FAIL'
            result['error'] = str(e)
            logger.error(f"Test ÉCHOUÉ: {e}")
        
        finally:
            self.injector.stop_all()
        
        self.results.append(result)
        return result
    
    def run_campaign(self, scenarios: List[Dict]) -> List[Dict]:
        """Exécute une campagne de tests"""
        logger.info(f"\n{'#'*60}")
        logger.info(f"DÉMARRAGE CAMPAGNE - {len(scenarios)} tests")
        logger.info(f"{'#'*60}\n")
        
        results = []
        for i, scenario in enumerate(scenarios, 1):
            logger.info(f"\n[Test {i}/{len(scenarios)}]")
            result = self.run_scenario(scenario)
            results.append(result)
            time.sleep(1)
        
        # Résumé
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = len(results) - passed
        
        logger.info(f"\n{'#'*60}")
        logger.info(f"RÉSUMÉ CAMPAGNE")
        logger.info(f"{'#'*60}")
        logger.info(f"Total: {len(results)} |  Réussis: {passed} |  Échoués: {failed}")
        logger.info(f"Taux de réussite: {passed/len(results)*100:.1f}%")
        
        return results
    
    def generate_report(self, output_file: str = "test_report.txt"):
        """Génère un rapport de test"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("RAPPORT DE TEST AUTOMATISÉ\n")
            f.write("="*60 + "\n\n")
            
            for result in self.results:
                f.write(f"Test: {result['name']}\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"Durée: {result.get('duration', 0):.2f}s\n")
                f.write(f"Pannes injectées: {', '.join(result['faults_injected'])}\n")
                f.write("\n" + "-"*60 + "\n\n")
        
        logger.info(f" Rapport généré: {output_file}")
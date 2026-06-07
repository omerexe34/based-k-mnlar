from .dsl_parser import dsl_parser

class CompatibilityEngine:
    """
    Executes the compatibility logic over the Digital Twin state.
    Relies entirely on the deterministic MTB Rules DSL.
    """
    def __init__(self):
        pass
        
    def evaluate(self, state_dict: dict) -> dict:
        """
        Runs the DSL COMPATIBILITY section against the current state.
        Returns a dictionary with status, warnings, and errors.
        """
        results = {
            'status': 'OK',
            'warnings': [],
            'errors': []
        }
        
        issues = dsl_parser.evaluate('COMPATIBILITY', state_dict)
        for issue in issues:
            if 'set_status(INCOMPATIBLE)' in issue['actions'] or 'set_status(HIGH_RISK)' in issue['actions']:
                results['status'] = 'INCOMPATIBLE'
                results['errors'].append(issue['reason'])
            else:
                results['warnings'].append(issue['reason'])
                
        return results

compatibility_engine = CompatibilityEngine()

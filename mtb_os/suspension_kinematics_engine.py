class SuspensionKinematicsEngine:
    """
    Simulates suspension behavior (Anti-squat, leverage ratio, progression).
    """
    def __init__(self):
        pass

    def calculate(self, state_dict: dict) -> dict:
        results = {
            'anti_squat_estimate': 'Unknown',
            'progression_curve': 'Linear',
            'pedal_bob_tendency': 'Medium',
            'bottom_out_resistance': 'Medium',
            'notes': []
        }
        
        frame = state_dict.get('frame', {})
        shock = state_dict.get('rear_shock', {})
        
        linkage_type = frame.get('linkage_type', 'Single Pivot')
        shock_type = shock.get('type', 'Air')
        
        # Progression & Bottom out
        if linkage_type == 'High Pivot' or linkage_type == 'Horst Link':
            results['progression_curve'] = 'Progressive'
        
        if results['progression_curve'] == 'Progressive' and shock_type == 'Air':
            results['bottom_out_resistance'] = 'High'
            results['notes'].append("Highly progressive frame with air shock creates excellent bottom-out resistance.")
        elif results['progression_curve'] == 'Linear' and shock_type == 'Coil':
            results['bottom_out_resistance'] = 'Low'
            results['notes'].append("Linear frame with coil shock risks harsh bottom-outs on big hits.")
            
        # Pedal Bob (Anti-squat)
        if linkage_type in ['VPP', 'DW-Link', 'High Pivot']:
            results['anti_squat_estimate'] = 'High (~110%)'
            results['pedal_bob_tendency'] = 'Low'
        elif shock.get('has_lockout'):
            results['notes'].append("Relies on shock lockout for climbing efficiency.")
            
        return results

suspension_kinematics_engine = SuspensionKinematicsEngine()

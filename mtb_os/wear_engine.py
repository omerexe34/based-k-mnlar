class WearEngine:
    """
    Calculates maintenance intervals, brake pad wear, and drivetrain stretch.
    """
    def __init__(self):
        pass

    def calculate_intervals(self, state_dict: dict, rider_profile: dict) -> dict:
        results = {
            'brake_pad_life_months': 6,
            'suspension_service_hours': 50,
            'drivetrain_chain_life_km': 1500,
            'bearing_life_months': 12
        }
        
        # Adjust based on riding conditions (from profile)
        conditions = rider_profile.get('riding_conditions', 'Dry')
        aggression = rider_profile.get('aggression_level', 'Medium')
        
        if conditions == 'Wet/Mud':
            results['brake_pad_life_months'] = int(results['brake_pad_life_months'] * 0.4)
            results['bearing_life_months'] = int(results['bearing_life_months'] * 0.6)
            results['drivetrain_chain_life_km'] = int(results['drivetrain_chain_life_km'] * 0.7)
            
        if aggression in ['High', 'Pro']:
            results['suspension_service_hours'] = 30
            results['drivetrain_chain_life_km'] = int(results['drivetrain_chain_life_km'] * 0.8)
            
        return results

wear_engine = WearEngine()

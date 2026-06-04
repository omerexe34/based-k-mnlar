class UpgradeImpactSimulator:
    """
    Simulates the delta (change) between two digital twin states.
    Calculates the exact performance gained or lost.
    """
    def __init__(self):
        pass

    def simulate(self, base_state_results: dict, upgraded_state_results: dict) -> dict:
        delta = {
            'weight_diff_kg': 0.0,
            'stability_change': 'Neutral',
            'climbing_penalty': 'Neutral',
            'overall_impact': 'Neutral'
        }
        
        # Weight Delta
        base_w = base_state_results.get('weight', {}).get('estimated_weight_kg', 0)
        new_w = upgraded_state_results.get('weight', {}).get('estimated_weight_kg', 0)
        delta['weight_diff_kg'] = round(new_w - base_w, 2)
        
        # Example logic for stability / climbing
        # If new weight is significantly higher or geometry distorted
        if delta['weight_diff_kg'] > 0.5:
            delta['climbing_penalty'] = 'High'
        elif delta['weight_diff_kg'] < -0.3:
            delta['climbing_penalty'] = 'Improved'
            
        if delta['weight_diff_kg'] > 0.2:
            delta['overall_impact'] = 'Heavy Duty Upgrade'
        else:
            delta['overall_impact'] = 'Lightweight Upgrade'
            
        return delta

upgrade_impact_simulator = UpgradeImpactSimulator()

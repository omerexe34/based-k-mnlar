class TerrainSimulator:
    """
    Simulates the performance, fatigue, and efficiency of the build across various terrains.
    """
    def __init__(self):
        self.terrains = ['Bike Park', 'Steep Downhill', 'Flow Trail', 'Enduro Race', 'XC Race', 'Urban Freeride']

    def simulate(self, state_dict: dict) -> dict:
        results = {}
        
        # Pull required data from state (would be outputted by category/physics engines normally)
        category = state_dict.get('frame', {}).get('category', 'Unknown')
        estimated_weight = 15.0 # Mocked for simplicity in this skeleton
        
        for terrain in self.terrains:
            score = {
                'confidence': 'Medium',
                'fatigue': 'Medium',
                'efficiency': 'Medium'
            }
            
            if terrain == 'Steep Downhill':
                if category == 'DH':
                    score['confidence'] = 'High'
                    score['fatigue'] = 'Low'
                elif category == 'XC':
                    score['confidence'] = 'Dangerous'
                    score['fatigue'] = 'Extreme'
                    
            elif terrain == 'XC Race':
                if category == 'DH':
                    score['efficiency'] = 'Terrible'
                    score['fatigue'] = 'Extreme'
                elif category == 'XC':
                    score['efficiency'] = 'High'
                    score['fatigue'] = 'Low'
            
            results[terrain] = score
            
        return results

terrain_simulator = TerrainSimulator()

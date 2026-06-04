class BuildPhysicsEngine:
    """
    Calculates estimated weights, unsprung mass, and front/rear balance.
    """
    def __init__(self):
        pass

    def calculate(self, state_dict: dict) -> dict:
        results = {
            'estimated_weight_kg': 0.0,
            'front_bias_percentage': 50.0,
            'unsprung_mass_kg': 0.0,
            'notes': []
        }
        
        # Calculate total weight
        total_weight = 0
        front_weight = 0
        unsprung = 0
        
        for slot, part in state_dict.items():
            if not isinstance(part, dict): continue
            
            w = part.get('weight_grams', 0)
            total_weight += w
            
            # Rough front vs rear bias
            if slot in ['fork', 'front_wheel', 'front_tire', 'front_rotor', 'cockpit']:
                front_weight += w
                
            # Unsprung mass
            if slot in ['front_wheel', 'rear_wheel', 'front_tire', 'rear_tire', 'front_rotor', 'rear_rotor']:
                unsprung += w
            # Fork lowers and swingarm are partially unsprung, adding a static ratio for simulation
            if slot == 'fork':
                unsprung += w * 0.3
                
        results['estimated_weight_kg'] = round(total_weight / 1000.0, 2)
        results['unsprung_mass_kg'] = round(unsprung / 1000.0, 2)
        
        if total_weight > 0:
            results['front_bias_percentage'] = round((front_weight / total_weight) * 100, 1)

        # Balance notes
        fb = results['front_bias_percentage']
        if fb > 55:
            results['notes'].append("Extremely front-heavy build. May dive under braking.")
        elif fb < 45:
            results['notes'].append("Rear-heavy build. Easy to manual, but front wheel might wash out in corners.")

        return results

build_physics_engine = BuildPhysicsEngine()

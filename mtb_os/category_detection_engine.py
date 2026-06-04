class CategoryDetectionEngine:
    """
    Infers the overall bike category (DH, Enduro, Trail, XC) based on its components.
    """
    
    def __init__(self):
        self.category_weights = {
            'DH': {'fork_travel_min': 200, 'shock_type': 'Coil', 'brakes': '4-Piston', 'rotor_min': 200},
            'Enduro': {'fork_travel_min': 160, 'fork_travel_max': 190, 'brakes': '4-Piston', 'rotor_min': 200},
            'Trail': {'fork_travel_min': 130, 'fork_travel_max': 150, 'brakes': '2-Piston'},
            'XC': {'fork_travel_max': 120, 'shock_type': 'Air', 'brakes': '2-Piston', 'rotor_max': 180}
        }

    def detect(self, state_dict: dict) -> str:
        scores = {'DH': 0, 'Enduro': 0, 'Trail': 0, 'XC': 0}
        
        fork = state_dict.get('fork', {})
        brakes = state_dict.get('brakes', {})
        shock = state_dict.get('rear_shock', {})
        rotor = state_dict.get('front_rotor', {})
        
        # Fork Travel checks
        ft = fork.get('travel', 0)
        if ft >= 200:
            scores['DH'] += 3
        elif 160 <= ft <= 190:
            scores['Enduro'] += 3
        elif 130 <= ft <= 150:
            scores['Trail'] += 3
        elif 0 < ft <= 120:
            scores['XC'] += 3

        # Shock Type checks
        st = shock.get('type', '')
        if st == 'Coil':
            scores['DH'] += 1
            scores['Enduro'] += 1
        elif st == 'Air':
            scores['Trail'] += 1
            scores['XC'] += 1

        # Rotor checks
        rs = rotor.get('size', 0)
        if rs >= 200:
            scores['DH'] += 1
            scores['Enduro'] += 1
        elif 0 < rs <= 180:
            scores['XC'] += 1
            scores['Trail'] += 1
            
        # If no components, return Unknown
        if sum(scores.values()) == 0:
            return "Unknown"

        # Return the category with the highest score
        return max(scores, key=scores.get)

category_detection_engine = CategoryDetectionEngine()

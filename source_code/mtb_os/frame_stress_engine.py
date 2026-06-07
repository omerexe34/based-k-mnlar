class FrameStressEngine:
    """
    Simulates long-term frame stress and immediate failure risks.
    """
    def __init__(self):
        pass

    def calculate(self, state_dict: dict) -> dict:
        results = {
            'headtube_stress': 'Normal',
            'linkage_stress': 'Normal',
            'overall_fatigue_multiplier': 1.0,
            'warnings': []
        }
        
        frame = state_dict.get('frame', {})
        fork = state_dict.get('fork', {})
        
        frame_max_travel = frame.get('max_travel', 160)
        fork_travel = fork.get('travel', 160)
        fork_type = fork.get('type', 'Single Crown')
        
        # Fork leverage effect on headtube
        travel_diff = fork_travel - frame_max_travel
        
        if travel_diff > 20:
            results['headtube_stress'] = 'Critical'
            results['warnings'].append(f"Fork travel is {travel_diff}mm over frame limits. Extremely high headtube leverage.")
            results['overall_fatigue_multiplier'] += 0.8
        elif travel_diff > 0:
            results['headtube_stress'] = 'Elevated'
            results['warnings'].append(f"Fork over-forked by {travel_diff}mm. Accelerated fatigue expected.")
            results['overall_fatigue_multiplier'] += 0.3
            
        if fork_type == 'Dual Crown' and frame.get('category') != 'DH':
            results['headtube_stress'] = 'Critical/Dangerous'
            results['warnings'].append("Dual crown fork installed on a non-DH frame. Immediate risk of headtube snapping.")
            results['overall_fatigue_multiplier'] += 1.5
            
        return results

frame_stress_engine = FrameStressEngine()

class DynamicRiskAnalysis:
    """
    Simulates long-term risks like frame fatigue, geometry distortion, and stress limits.
    """
    def __init__(self):
        pass

    def analyze(self, state_dict: dict, physics_state: dict) -> dict:
        results = {
            'geometry_distortion': 'None',
            'frame_fatigue_risk': 'Low',
            'warnings': []
        }
        
        # Pull data
        frame = state_dict.get('frame', {})
        fork = state_dict.get('fork', {})
        weight = physics_state.get('estimated_weight_kg', 15.0)
        
        # Geometry distortion from over-forking
        travel_diff = fork.get('travel', 160) - frame.get('max_travel', 160)
        if travel_diff > 10:
            distortion_deg = round(travel_diff / 10.0 * 0.5, 1) # ~0.5 degree per 10mm
            results['geometry_distortion'] = f"-{distortion_deg} deg head angle"
            results['warnings'].append(f"Geometry distorted: Head angle slackened by ~{distortion_deg} degrees. Bottom bracket raised.")
            
        if travel_diff > 20:
            results['frame_fatigue_risk'] = 'High'
            
        if weight > 18.0 and frame.get('category') == 'Trail':
            results['frame_fatigue_risk'] = 'Medium'
            results['warnings'].append("Extremely heavy build for a trail frame. Linkage bearings will wear faster.")
            
        return results

dynamic_risk_analysis = DynamicRiskAnalysis()

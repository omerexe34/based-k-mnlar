from .dsl_parser import dsl_parser

class ReactiveEnginePipeline:
    """
    The orchestrator that recalculates the Digital Twin state whenever it becomes dirty.
    It runs through Compatibility -> Physics -> Kinematics -> Ride Character -> Risk.
    """
    
    def __init__(self):
        # We will initialize sub-engines here as they are built.
        pass

    def recalculate(self, twin):
        """
        Runs the full multi-stage analysis pipeline on the given DigitalTwin object.
        """
        if not twin.is_dirty:
            return
            
        state_dict = twin.get_state_dict()
        
        results = {
            'compatibility': {'status': 'OK', 'warnings': [], 'errors': []},
            'geometry': {},
            'weight': {},
            'suspension': {},
            'stress': {},
            'wear': {},
            'ride_character': {}
        }
        
        # 1. Compatibility Check (DSL execution)
        comp_issues = dsl_parser.evaluate('COMPATIBILITY', state_dict)
        for issue in comp_issues:
            if 'set_status(INCOMPATIBLE)' in issue['actions'] or 'set_status(HIGH_RISK)' in issue['actions']:
                results['compatibility']['status'] = 'INCOMPATIBLE'
                results['compatibility']['errors'].append(issue['reason'])
            else:
                results['compatibility']['warnings'].append(issue['reason'])

        # 2. Risk Check (DSL execution)
        risk_issues = dsl_parser.evaluate('RISK', state_dict)
        for issue in risk_issues:
            results['compatibility']['warnings'].append(f"Risk: {issue['reason']}")

        # 3. Physics & Kinematics (Placeholders, to be implemented in their respective engine files)
        # build_physics_engine.calculate(twin, results)
        # suspension_kinematics_engine.calculate(twin, results)
        # frame_stress_engine.calculate(twin, results)
        
        # 4. Ride Character (Placeholders)
        # ride_character_engine.calculate(twin, results)

        # 5. Wear & Tear (DSL + Placeholders)
        wear_issues = dsl_parser.evaluate('WEAR', state_dict)
        results['wear']['notes'] = [w['reason'] for w in wear_issues]
        
        # Commit back to twin
        twin.update_analysis_states(results)
        
reactive_pipeline = ReactiveEnginePipeline()

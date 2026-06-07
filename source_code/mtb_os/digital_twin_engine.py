import uuid
import time

class DigitalTwin:
    """
    Represents the reactive state of a mountain bike build.
    Any modification triggers dirty flags, prompting pipeline recalculations.
    """
    def __init__(self, user_id):
        self.twin_id = str(uuid.uuid4())
        self.user_id = user_id
        
        # Component State
        self.components = {
            'frame': {},
            'fork': {},
            'rear_shock': {},
            'front_wheel': {},
            'rear_wheel': {},
            'front_tire': {},
            'rear_tire': {},
            'brakes': {},
            'front_rotor': {},
            'rear_rotor': {},
            'drivetrain': {}, # Derailleur, shifter, cassette, chain
            'crankset': {},
            'cockpit': {} # Handlebar, stem
        }
        
        # Analyzed States (Populated by the Pipeline)
        self.geometry_state = {}
        self.weight_state = {}
        self.suspension_state = {}
        self.stress_state = {}
        self.wear_state = {}
        self.compatibility_state = {'status': 'UNKNOWN', 'warnings': [], 'errors': []}
        self.ride_character_state = {}
        
        self.last_updated = int(time.time())
        self.is_dirty = True  # Needs pipeline recalculation

    def add_component(self, slot: str, part_data: dict):
        if slot in self.components:
            self.components[slot] = part_data
            self.is_dirty = True
            self.last_updated = int(time.time())

    def remove_component(self, slot: str):
        if slot in self.components:
            self.components[slot] = {}
            self.is_dirty = True
            self.last_updated = int(time.time())

    def get_state_dict(self):
        """Returns the flat dictionary format required by the DSL Parser and other engines."""
        return self.components

    def update_analysis_states(self, analysis_results: dict):
        """Called by the Reactive Engine Pipeline to commit calculated physical states."""
        self.geometry_state = analysis_results.get('geometry', {})
        self.weight_state = analysis_results.get('weight', {})
        self.suspension_state = analysis_results.get('suspension', {})
        self.stress_state = analysis_results.get('stress', {})
        self.wear_state = analysis_results.get('wear', {})
        self.compatibility_state = analysis_results.get('compatibility', {})
        self.ride_character_state = analysis_results.get('ride_character', {})
        self.is_dirty = False

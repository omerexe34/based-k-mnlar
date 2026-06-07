class MTBKnowledgeGraph:
    """
    Defines relationships, ecosystems, and recommended pairings between different parts.
    """
    def __init__(self):
        # Component to Component pairings
        self.common_pairings = {
            'Fox 38': ['Fox Float X2', 'Fox DHX2', 'Code RSC'],
            'RockShox Zeb': ['RockShox Super Deluxe', 'SRAM Maven'],
            'Shimano XTR': ['Fox 34 Step-Cast', 'Lightweight Carbon Wheels']
        }
        
        # Brand ecosystems (preferring parts from the same brand family)
        self.ecosystems = {
            'SRAM': ['SRAM', 'RockShox', 'Zipp', 'Truvativ'],
            'Shimano': ['Shimano', 'PRO'],
            'Fox': ['Fox', 'RaceFace', 'Marzocchi']
        }
        
        # Intent mappings
        self.intent_mappings = {
            'DH': ['Dual Crown', '200mm+', 'Coil', 'Code', 'Saint'],
            'Enduro': ['170mm', '160mm', 'Piggyback Shock', '4-Piston', 'Super Boost'],
            'Trail': ['140mm', '130mm', 'Inline Shock', 'Lightweight'],
            'XC': ['100mm', '120mm', 'Hardtail', 'Lockout', '2-Piston']
        }

    def check_pairing_synergy(self, part_a: str, part_b: str) -> bool:
        """Returns True if the parts are commonly paired together."""
        for key, pairings in self.common_pairings.items():
            if (key in part_a and any(p in part_b for p in pairings)) or \
               (key in part_b and any(p in part_a for p in pairings)):
                return True
        return False
        
    def get_ecosystem(self, brand: str) -> str:
        for ecosystem_name, brands in self.ecosystems.items():
            if brand in brands:
                return ecosystem_name
        return "Independent"

knowledge_graph = MTBKnowledgeGraph()

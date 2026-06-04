import re

class BikeParser:
    """
    Normalizes raw user input into structured strings or dictionaries,
    stripping noise and standardizing brand/model nomenclature.
    """
    
    BRAND_ALIASES = {
        'rockshox': 'RockShox',
        'rock shox': 'RockShox',
        'rs': 'RockShox',
        'fox': 'Fox',
        'fox racing shox': 'Fox',
        'shimano': 'Shimano',
        'sram': 'SRAM',
        'maxxis': 'Maxxis'
    }

    def __init__(self):
        pass

    def normalize_brand(self, text: str) -> str:
        text_lower = text.lower()
        for alias, actual in self.BRAND_ALIASES.items():
            if alias in text_lower:
                return actual
        return "Unknown"

    def extract_travel(self, text: str) -> int:
        """Extracts suspension travel from text, e.g. '170mm' -> 170"""
        match = re.search(r'(\d{2,3})\s*mm', text.lower())
        if match:
            return int(match.group(1))
        return 0

    def extract_wheel_size(self, text: str) -> str:
        if '29' in text or '29er' in text:
            return '29'
        if '27.5' in text or '650b' in text:
            return '27.5'
        if '26' in text:
            return '26'
        return 'Unknown'

    def parse_part(self, raw_input: str) -> dict:
        """
        Parses a generic input string into a structured dictionary.
        """
        return {
            'original': raw_input,
            'normalized_brand': self.normalize_brand(raw_input),
            'extracted_travel': self.extract_travel(raw_input),
            'extracted_wheel_size': self.extract_wheel_size(raw_input),
            'tokens': raw_input.lower().split()
        }

bike_parser = BikeParser()

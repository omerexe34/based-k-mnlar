# In a real enterprise system, this would integrate with pgvector or an external embedding service.
import difflib

class HybridSearch:
    """
    Search engine that combines exact matching, alias checking, fuzzy string matching,
    and semantic vector space searching (mocked here for the Python layer).
    """
    
    def __init__(self):
        # This would typically connect to Supabase
        self.mock_catalog = [
            {'id': 1, 'exact_model': 'Fox 38 Factory Grip2', 'aliases': ['38 factory', 'fox38', 'fox 38 grip2']},
            {'id': 2, 'exact_model': 'RockShox Zeb Ultimate', 'aliases': ['zeb ult', 'rs zeb', 'zeb ultimate']},
            {'id': 3, 'exact_model': 'Shimano XTR M9120', 'aliases': ['xtr 4 piston', 'm9120', 'xtr enduro brakes']}
        ]

    def search(self, query: str):
        query_lower = query.lower().strip()
        
        # 1. Exact & Alias Match
        for item in self.mock_catalog:
            if query_lower == item['exact_model'].lower() or query_lower in item['aliases']:
                return {'match_type': 'exact', 'confidence': 98, 'item': item}
                
        # 2. Fuzzy Match
        best_ratio = 0
        best_match = None
        for item in self.mock_catalog:
            # Check exact model name
            ratio = difflib.SequenceMatcher(None, query_lower, item['exact_model'].lower()).ratio()
            # Check aliases
            for alias in item['aliases']:
                alias_ratio = difflib.SequenceMatcher(None, query_lower, alias).ratio()
                if alias_ratio > ratio:
                    ratio = alias_ratio
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = item
                
        if best_ratio > 0.75:
            return {'match_type': 'fuzzy', 'confidence': int(best_ratio * 100), 'item': best_match}
            
        # 3. Semantic Vector Search (Placeholder)
        # return self._semantic_search(query_lower)
        
        return {'match_type': 'none', 'confidence': 0, 'item': None}

hybrid_search = HybridSearch()

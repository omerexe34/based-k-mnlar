class CostToPerformanceEngine:
    """
    Analyzes the financial worth of a build or an upgrade.
    Returns 'Worth It' ratings based on msrp vs performance metrics.
    """
    def __init__(self):
        pass

    def evaluate(self, component_name: str, performance_score: int, price: float, baseline_price: float) -> dict:
        """
        Evaluates a single component against a baseline.
        """
        if baseline_price <= 0:
            return {'value_score': 0, 'worth_it': 'Unknown'}
            
        price_ratio = price / baseline_price
        
        # If it costs 50% more but only gives a 5% performance boost...
        if price_ratio > 1.4 and performance_score < 90:
            worth_it = 'Low'
        elif price_ratio < 1.2 and performance_score > 85:
            worth_it = 'High'
        else:
            worth_it = 'Moderate'
            
        return {
            'value_score': round(performance_score / (price_ratio if price_ratio > 0 else 1), 1),
            'worth_it': worth_it
        }

cost_to_performance_engine = CostToPerformanceEngine()

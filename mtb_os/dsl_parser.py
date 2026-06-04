import re
import os

class DSLParser:
    def __init__(self, dsl_path="mtb_os/mtb_rules.dsl"):
        self.rules = {'COMPATIBILITY': [], 'RISK': [], 'WEAR': []}
        self._load_rules(dsl_path)

    def _load_rules(self, dsl_path):
        if not os.path.exists(dsl_path):
            return
            
        with open(dsl_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        current_section = None
        current_rule = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'): continue
            
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
                
            if line.startswith('RULE '):
                rule_name = line.replace('RULE ', '').replace(':', '').strip()
                current_rule = {'name': rule_name, 'conditions': [], 'actions': [], 'reason': ''}
                if current_section:
                    self.rules[current_section].append(current_rule)
                continue
                
            if current_rule is not None:
                if line.startswith('IF '):
                    current_rule['conditions'].append(line[3:].strip())
                elif line.startswith('AND '):
                    current_rule['conditions'].append('AND ' + line[4:].strip())
                elif line.startswith('OR '):
                    current_rule['conditions'].append('OR ' + line[3:].strip())
                elif line.startswith('THEN '):
                    current_rule['actions'].append(line[5:].strip())
                elif line.startswith('REASON '):
                    current_rule['reason'] = line[7:].replace('"', '').strip()

    def evaluate(self, category, state_dict):
        """
        Evaluates a category of rules against a given digital twin state dictionary.
        Returns a list of triggered actions/reasons.
        """
        triggered = []
        rules = self.rules.get(category, [])
        
        for rule in rules:
            if self._check_conditions(rule['conditions'], state_dict):
                triggered.append({
                    'rule': rule['name'],
                    'actions': rule['actions'],
                    'reason': rule['reason']
                })
        return triggered

    def _check_conditions(self, conditions, state_dict):
        # A very basic interpreter for demonstration purposes.
        # In a real enterprise engine, this would use an AST or `eval` with a highly restricted locals dictionary.
        if not conditions: return False
        
        # Flatten conditions into a single string expression
        expr = " ".join(conditions)
        
        # Replace DSL operators with Python operators
        expr = expr.replace(' OR ', ' or ').replace(' AND ', ' and ').replace('=', '==').replace('====', '==')
        expr = expr.replace('false', 'False').replace('true', 'True')
        
        # Simple string replacement for state variables
        # E.g., fork.travel -> state_dict.get('fork', {}).get('travel')
        
        def replacer(match):
            parts = match.group(0).split('.')
            if len(parts) == 2:
                obj, prop = parts
                val = state_dict.get(obj, {}).get(prop, None)
                if isinstance(val, str):
                    return f'"{val}"'
                return str(val) if val is not None else "None"
            return match.group(0)

        # Find patterns like word.word
        try:
            parsed_expr = re.sub(r'[a-zA-Z_]+\.[a-zA-Z_]+', replacer, expr)
            # Safe eval
            return eval(parsed_expr)
        except Exception as e:
            # If parsing fails or attribute missing, condition false
            return False

dsl_parser = DSLParser()

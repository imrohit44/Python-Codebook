import re

class Interpreter:
    def __init__(self):
        self.operators = {
            'add': lambda a, b: a + b,
            'sub': lambda a, b: a - b,
            'mul': lambda a, b: a * b,
            'div': lambda a, b: a / b
        }
    
    def parse(self, expression):
        tokens = re.findall(r'\(|\)|\w+|[+\-*/\d.]+', expression)
        tokens.reverse()
        
        def _parse_expr():
            token = tokens.pop()
            if token == '(':
                op = tokens.pop()
                args = []
                while tokens[-1] != ')':
                    args.append(_parse_expr())
                tokens.pop()
                return (op, args)
            else:
                try:
                    return int(token)
                except ValueError:
                    return float(token)

        return _parse_expr()

    def evaluate(self, ast):
        if isinstance(ast, (int, float)):
            return ast
        
        op, args = ast
        if op in self.operators:
            evaluated_args = [self.evaluate(arg) for arg in args]
            return self.operators[op](*evaluated_args)
        else:
            raise ValueError(f"Unknown operator: {op}")

if __name__ == '__main__':
    interpreter = Interpreter()
    
    expr1 = "(add 10 (mul 2 3))"
    result1 = interpreter.evaluate(interpreter.parse(expr1))
    print(f"Expression '{expr1}' evaluates to {result1}")
    
    expr2 = "(sub 100 (div 50 5))"
    result2 = interpreter.evaluate(interpreter.parse(expr2))
    print(f"Expression '{expr2}' evaluates to {result2}")
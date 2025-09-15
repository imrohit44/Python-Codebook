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
        
        def _parse_expr(tokens_iter):
            token = next(tokens_iter)
            if token == '(':
                op = next(tokens_iter)
                args = []
                while tokens_iter and tokens_iter[0] != ')':
                    args.append(_parse_expr(tokens_iter))
                next(tokens_iter)
                return (op, args)
            else:
                try:
                    return int(token)
                except ValueError:
                    return float(token)

        return _parse_expr(iter(tokens))

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
    ast1 = interpreter.parse(expr1)
    result1 = interpreter.evaluate(ast1)
    print(f"Expression '{expr1}' evaluates to {result1}")
    
    expr2 = "(sub 100 (div 50 5))"
    ast2 = interpreter.parse(expr2)
    result2 = interpreter.evaluate(ast2)
    print(f"Expression '{expr2}' evaluates to {result2}")
import random
import math
import operator

# --- Node Definitions for Expression Tree ---
class Node:
    def __init__(self, value, children=None):
        self.value = value # Operator string, variable name, or constant value
        self.children = children if children is not None else [] # List of child Nodes

    def __repr__(self):
        return f"Node({self.value}, Children={len(self.children)})"

    def to_string(self):
        """Converts the expression tree to a readable string."""
        if not self.children: # Terminal node
            return str(self.value)
        elif len(self.children) == 1: # Unary operator
            return f"{self.value}({self.children[0].to_string()})"
        elif len(self.children) == 2: # Binary operator
            return f"({self.children[0].to_string()} {self.value} {self.children[1].to_string()})"
        return f"UNKNOWN_EXPR({self.value})"

    def evaluate(self, x_val):
        """Evaluates the expression tree for a given 'x' value."""
        if self.value == 'x':
            return x_val
        try:
            return float(self.value) # Constant
        except ValueError:
            pass # Not a constant, must be an operator

        # Operators
        if self.value == '+':
            return self.children[0].evaluate(x_val) + self.children[1].evaluate(x_val)
        elif self.value == '-':
            return self.children[0].evaluate(x_val) - self.children[1].evaluate(x_val)
        elif self.value == '*':
            return self.children[0].evaluate(x_val) * self.children[1].evaluate(x_val)
        elif self.value == '/':
            denominator = self.children[1].evaluate(x_val)
            # Protected division: avoid ZeroDivisionError
            if abs(denominator) < 1e-6: # Very small number, treat as zero
                return 1.0 # Return a default value to avoid infinity/error
            return self.children[0].evaluate(x_val) / denominator
        # Add more functions here if needed (e.g., sin, cos)
        # elif self.value == 'sin':
        #     return math.sin(self.children[0].evaluate(x_val))
        else:
            raise ValueError(f"Unknown operator or terminal: {self.value}")

    def get_all_nodes(self):
        """Returns a flat list of all nodes in the tree (for crossover/mutation)."""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.get_all_nodes())
        return nodes

    def copy(self):
        """Performs a deep copy of the node and its children."""
        return Node(self.value, [child.copy() for child in self.children])

# --- Genetic Programming Implementation ---
class GeneticProgrammer:
    def __init__(self,
                 target_data: list[tuple[float, float]],
                 pop_size: int = 100,
                 max_depth: int = 5,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.8):

        self.target_data = target_data
        self.pop_size = pop_size
        self.max_depth = max_depth
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        # Define the set of available functions (operators) and terminals
        self.functions = ['+', '-', '*', '/'] # Binary operators
        # self.unary_functions = ['sin', 'cos'] # Unary operators
        self.terminals = ['x'] # Variable
        self.constant_range = (-5.0, 5.0) # Range for random constants

        self.population = self._create_initial_population()

    def _create_random_tree(self, current_depth: int, is_root: bool = True) -> Node:
        """
        Recursively creates a random expression tree.
        Uses 'grow' method for initialization (mix of full and grow).
        """
        if current_depth >= self.max_depth or \
           (not is_root and random.random() < 0.5 and current_depth > 0): # Bias towards terminals at depth
            # Create a terminal (variable 'x' or a random constant)
            if random.random() < 0.5:
                return Node('x')
            else:
                return Node(round(random.uniform(*self.constant_range), 2))
        else:
            # Create a function node
            func = random.choice(self.functions)
            node = Node(func)
            
            # Binary operators need two children
            node.children.append(self._create_random_tree(current_depth + 1, False))
            node.children.append(self._create_random_tree(current_depth + 1, False))
            
            return node

    def _create_initial_population(self) -> list[Node]:
        """Generates the initial population of random expression trees."""
        return [self._create_random_tree(0) for _ in range(self.pop_size)]

    def _calculate_fitness(self, individual: Node) -> float:
        """
        Calculates fitness based on Mean Squared Error (MSE).
        Lower MSE (closer to 0) is better.
        """
        total_squared_error = 0.0
        for x_val, true_y in self.target_data:
            try:
                predicted_y = individual.evaluate(x_val)
                error = predicted_y - true_y
                total_squared_error += error ** 2
            except (ValueError, TypeError): # Catch errors during evaluation (e.g., log of negative)
                return float('inf') # Penalize invalid expressions heavily
        
        mse = total_squared_error / len(self.target_data)
        # For selection, we often want higher values for better fitness.
        # So, we can return 1 / (1 + mse) or (some_large_number - mse)
        # Using 1 / (1 + mse) to avoid division by zero and make higher values better.
        return 1.0 / (1.0 + mse)

    def _select_parent(self) -> Node:
        """
        Selects a parent using Tournament Selection.
        Picks 'k' individuals randomly and selects the best among them.
        """
        tournament_size = 5
        competitors = random.sample(self.population, min(tournament_size, len(self.population)))
        best_individual = None
        best_fitness = -1.0

        for individual in competitors:
            fitness = self._calculate_fitness(individual)
            if fitness > best_fitness:
                best_fitness = fitness
                best_individual = individual
        return best_individual

    def _crossover(self, parent1: Node, parent2: Node) -> Node:
        """
        Performs subtree crossover between two parent trees.
        """
        child1 = parent1.copy() # Create a copy to modify
        child2 = parent2.copy() # Also create child2 for potential 2-offspring crossover

        parent1_nodes = child1.get_all_nodes()
        parent2_nodes = child2.get_all_nodes()

        # Select random nodes from each parent
        node1_to_replace = random.choice(parent1_nodes)
        node2_to_swap = random.choice(parent2_nodes)

        # Find the parent of node1_to_replace in child1
        # This is a bit tricky; easier to just replace in the copy directly if structure is simple
        # For simplicity, we'll replace the chosen node in child1 with a copy of node2_to_swap.
        # This effectively creates one child (child1 with a swapped subtree).
        
        # This requires more careful tree manipulation if not doing full-tree replacement.
        # A simple way for learning is to just swap the actual Node objects.
        # Find the node in child1 that matches node1_to_replace by value and structure
        
        # A robust way is to rebuild the tree or directly manipulate parent pointers.
        # For this example, let's use a simpler "replace a random node" approach.
        
        # Simplified Crossover: Replace a random node in child1 with a copy of a random node from child2
        nodes_in_child1 = child1.get_all_nodes()
        # Ensure we pick a node that *can* be swapped, e.g., not the root unless depth allows.
        # For simplicity, pick any node that isn't the root to avoid trivial swaps
        # Or just pick any node and let tree structure handle.
        
        # The easiest way to implement this while maintaining tree integrity is:
        # 1. Pick a random node N1 in parent1.
        # 2. Pick a random node N2 in parent2.
        # 3. Create a copy of parent1 (this is offspring).
        # 4. In offspring, find where N1 was and replace it with a copy of N2.

        # Let's use a utility function to find and replace
        offspring_tree = parent1.copy()
        nodes_in_offspring = offspring_tree.get_all_nodes()
        
        # Pick a random node in offspring_tree to replace
        replace_node_index = random.randint(0, len(nodes_in_offspring) - 1)
        node_to_replace = nodes_in_offspring[replace_node_index]

        # Pick a random node from parent2 to insert
        nodes_in_parent2 = parent2.get_all_nodes()
        node_to_insert = random.choice(nodes_in_parent2).copy() # Use a copy!

        # Now, replace node_to_replace with node_to_insert.
        # This is the tricky part without parent pointers.
        # A common GP approach is to represent trees in an array or list, or
        # pass parent references in node traversal.

        # Simpler approach: If the selected node is the root, replace the whole tree.
        # Otherwise, iterate through parents to find and replace the child.
        
        if node_to_replace == offspring_tree: # If we picked the root to replace
            return node_to_insert # The new offspring is just the swapped subtree

        # Otherwise, find the parent of `node_to_replace` and update its child reference
        # This requires a traversal that keeps track of parent.
        # For simplicity, let's just make `Node.get_all_nodes` return (node, parent) tuples
        # Or, just return a single offspring by directly manipulating the copy of parent1.

        # Let's simplify crossover: pick a subtree from P1, pick a subtree from P2, swap them in P1's copy.
        # This requires finding parent pointers or knowing how to "mutate" a specific child.
        
        # A more common and simpler way for basic implementations:
        # 1. Select a random node in parent1 (P1_node).
        # 2. Select a random node in parent2 (P2_node).
        # 3. Create a *copy* of parent1.
        # 4. Traverse the copied tree to find the *corresponding* node to P1_node.
        # 5. Replace that corresponding node with a copy of P2_node.

        # The `get_all_nodes` method returns a list of Node objects.
        # To replace effectively, we need direct references or a way to traverse and replace.
        # Let's make `get_all_nodes` return (node, parent_node, child_index_in_parent)
        
        nodes_with_info = [] # (node, parent, child_idx_in_parent)
        def _collect_nodes_with_info(current_node, parent=None, child_idx=None):
            nodes_with_info.append((current_node, parent, child_idx))
            for i, child in enumerate(current_node.children):
                _collect_nodes_with_info(child, current_node, i)
        
        _collect_nodes_with_info(offspring_tree)
        
        # Select random node to replace from the offspring copy
        idx_to_replace = random.randint(0, len(nodes_with_info) - 1)
        node_to_replace_info = nodes_with_info[idx_to_replace]
        selected_node_in_offspring, parent_of_selected, child_idx_of_selected = node_to_replace_info

        # Select random node from parent2 (it can be any node)
        nodes_in_parent2_flat = parent2.get_all_nodes()
        node_from_parent2 = random.choice(nodes_in_parent2_flat).copy()

        if parent_of_selected is None: # If the root was selected
            return node_from_parent2
        else:
            parent_of_selected.children[child_idx_of_selected] = node_from_parent2
            return offspring_tree

    def _mutate(self, individual: Node) -> Node:
        """
        Performs point mutation: replaces a random node with a new random subtree.
        """
        mutated_individual = individual.copy()
        
        nodes_with_info = []
        def _collect_nodes_with_info(current_node, parent=None, child_idx=None):
            nodes_with_info.append((current_node, parent, child_idx))
            for i, child in enumerate(current_node.children):
                _collect_nodes_with_info(child, current_node, i)
        
        _collect_nodes_with_info(mutated_individual)

        # Select a random node to mutate
        idx_to_mutate = random.randint(0, len(nodes_with_info) - 1)
        node_to_mutate_info = nodes_with_info[idx_to_mutate]
        selected_node_in_individual, parent_of_selected, child_idx_of_selected = node_to_mutate_info

        # Create a new random subtree
        new_subtree = self._create_random_tree(0) # New tree, can be full depth

        if parent_of_selected is None: # If the root was selected
            return new_subtree
        else:
            parent_of_selected.children[child_idx_of_selected] = new_subtree
            return mutated_individual


    def evolve(self, generations: int):
        """Runs the genetic programming evolution process."""
        for gen in range(generations):
            # Evaluate fitness of the current population
            evaluated_population = [] # (fitness, individual)
            for individual in self.population:
                fitness = self._calculate_fitness(individual)
                evaluated_population.append((fitness, individual))
            
            # Sort by fitness (descending, higher is better)
            evaluated_population.sort(key=lambda x: x[0], reverse=True)

            best_fitness = evaluated_population[0][0]
            best_individual = evaluated_population[0][1]
            best_expression_str = best_individual.to_string()
            
            # Convert fitness back to MSE for reporting
            best_mse = (1.0 / best_fitness) - 1.0 if best_fitness > 0 else float('inf')

            print(f"Gen {gen}: Best Fitness={best_fitness:.4f} (MSE={best_mse:.4f}), Best Expression: {best_expression_str}")

            if best_mse < 0.001: # Threshold for "solved"
                print(f"\nSolution found in Generation {gen}!")
                return best_individual

            # Create new population
            new_population = []
            
            # Elitism: Keep the very best individual(s)
            new_population.append(best_individual.copy()) 

            while len(new_population) < self.pop_size:
                parent1 = self._select_parent()
                parent2 = self._select_parent() # Can be the same as parent1

                offspring = None
                if random.random() < self.crossover_rate:
                    offspring = self._crossover(parent1, parent2)
                else:
                    offspring = parent1.copy() # If no crossover, just copy parent

                if random.random() < self.mutation_rate:
                    offspring = self._mutate(offspring)
                
                new_population.append(offspring)

            self.population = new_population[:self.pop_size] # Ensure population size is maintained

        print(f"\nMax generations reached. Best expression found: {best_individual.to_string()}")
        return best_individual

# --- Main Test ---
if __name__ == "__main__":
    # Define target function: f(x) = x^2 + 2x + 1
    # Generate some data points
    target_function = lambda x: x**2 + 2*x + 1
    data_points = []
    for i in range(-5, 6):
        x = float(i)
        data_points.append((x, target_function(x)))

    print("Target Function Data Points:")
    for dp in data_points:
        print(f"x={dp[0]}, y={dp[1]}")
    print("-" * 50)

    gp = GeneticProgrammer(
        target_data=data_points,
        pop_size=200,
        max_depth=4, # Keep depth small for simple functions
        mutation_rate=0.15,
        crossover_rate=0.8
    )

    final_solution = gp.evolve(generations=100) # Run for a number of generations

    print("\nFinal Best Evolved Expression:")
    print(final_solution.to_string())
    final_mse = (1.0 / gp._calculate_fitness(final_solution)) - 1.0
    print(f"Final MSE: {final_mse:.4f}")

    # Test the final solution
    print("\nTesting Final Expression on Data:")
    for x_val, true_y in data_points:
        predicted_y = final_solution.evaluate(x_val)
        print(f"x={x_val}, True Y={true_y}, Predicted Y={predicted_y:.2f}")
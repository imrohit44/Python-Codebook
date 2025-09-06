import random
import math

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distance(city1, city2):
    return math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

def generate_cities(num_cities):
    return [City(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]

def create_individual(cities):
    individual = list(range(len(cities)))
    random.shuffle(individual)
    return individual

def calculate_fitness(individual, cities):
    total_distance = 0
    for i in range(len(individual)):
        city1_idx = individual[i]
        city2_idx = individual[(i + 1) % len(individual)]
        total_distance += distance(cities[city1_idx], cities[city2_idx])
    
    return 1 / total_distance

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size
    start, end = sorted(random.sample(range(size), 2))
    
    child[start:end] = parent1[start:end]
    
    fill_pos = 0
    for gene in parent2:
        if gene not in child:
            while child[fill_pos] != -1:
                fill_pos += 1
            child[fill_pos] = gene
            
    return child

def swap_mutation(individual):
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def genetic_algorithm(cities, pop_size, generations):
    population = [create_individual(cities) for _ in range(pop_size)]
    
    for gen in range(generations):
        fitness_scores = [(calculate_fitness(ind, cities), ind) for ind in population]
        fitness_scores.sort(key=lambda x: x[0], reverse=True)
        
        best_fitness, best_individual = fitness_scores[0]
        
        if gen % 100 == 0:
            print(f"Generation {gen}, Best distance: {1 / best_fitness}")
        
        new_population = [best_individual]
        
        while len(new_population) < pop_size:
            parent1 = random.choice(fitness_scores)[1]
            parent2 = random.choice(fitness_scores)[1]
            
            if random.random() < 0.8:
                child = ordered_crossover(parent1, parent2)
            else:
                child = parent1
            
            if random.random() < 0.05:
                child = swap_mutation(child)
            
            new_population.append(child)
            
        population = new_population
        
    return best_individual

if __name__ == "__main__":
    num_cities = 20
    cities_list = generate_cities(num_cities)
    
    solution = genetic_algorithm(cities_list, pop_size=100, generations=1000)
    
    print("\nFinal best route (city indices):")
    print(solution)
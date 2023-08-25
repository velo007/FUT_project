import pygad as pg
import pandas as pd
import numpy as np
import json
import random

# Hyperparameters:
sol_per_pop = 100

# Define the custom fitness function
def fitness_func(solution, solution_idx):
    # Calculate the fitness of the team composition
    fitness = ...  # Calculate fitness based on solution (team composition)
    return fitness

# Define the custom function to generate initial population
def init_population(gene_space: list[list[list]]) -> list[list[list]]:
    # Generate and return the entire initial population of teams
    initial_population = []
    for _ in range(sol_per_pop):
        team = [random.choice(players) for players in gene_space]
        initial_population.append(team)
    return initial_population

# Define the custom crossover function
def custom_crossover(parent1, parent2):
    # Implement your own crossover logic here
    child = ...  # Create a new child solution by combining parents
    return child

# Define the custom mutation function
def custom_mutation(offspring, ga_instance):
    # Implement your own mutation logic here
    mutated_offspring = ...  # Mutate the solution
    return mutated_offspring


formations = {'433' : ['GK','LB','CB', 'CB', 'RB', 'CM','CM','CM','LW','ST', 'RW']}

def generate_gene_space() -> list[list]:
    
    with open("position_players_dict.json", "r") as json_file:
        position_players_dict = json.loads(json_file.read())

    gene_space = [None for _ in range(11)]

    for i in range(11):
        positions = set([pos[i] for pos in formations.values()])

        gene_space_i = []
        for pos in positions:
            gene_space_i += position_players_dict[pos]
        
        gene_space[i] = gene_space_i

    return gene_space


# if __name__ == "__main__":    
#     # Create a PyGAD instance
#     sol_per_pop = 10
#     num_generations = 50
#     num_parents_mating = 6
#     num_players = 12

#     ga_instance = pg.GA(num_generations=num_generations,
#                         num_parents_mating=num_parents_mating,
#                         fitness_func=fitness_func,
#                         sol_per_pop=sol_per_pop,
#                         num_genes=num_players,
#                         init_population=init_population,
#                         crossover_func=custom_crossover,
#                         mutation_func=custom_mutation)

#     # Run the optimization process
#     ga_instance.run()

#     # Get the best solution and its fitness
#     best_solution = ga_instance.best_solution()
#     best_fitness = best_solution[1]

#     print("Best fitness:", best_fitness)
#     print("Best team composition:", best_solution[0])


if __name__ == "__main__":    
    gene_space = generate_gene_space()
    initial_population = init_population(gene_space)
    print(initial_population)
# nqueens.py
# Solving the n-queens problem with a genetic algorithm.

import numpy as np
import matplotlib.pyplot as plt
import checkerboard
import time

def initialize(m, N):
    '''Initialize a population of m individuals with genotypes of length N.'''
    return np.random.randint(0, N, size=(m, N))

def fitness(population):
    '''Compute the fitness of every individual in the population.'''
    cols = np.count_nonzero(np.diff(np.sort(population, axis=1))==0, axis=1)
    diags = np.zeros_like(cols)
    for i in range(1, population.shape[1]):
        potential = abs(population - np.roll(population,i))==i
        actual = np.sum(potential[:,i:], axis=1)
        diags += actual
    return cols + diags
    
def selectparents(population, n, k):
    '''Tournament selection (size k) of n parents from a given population.'''
    x = np.random.randint(population.shape[0], size=(n,k))
    indices = x.min(axis=1)
    return population[indices,:]

def crossover(parents, pc):
    '''Perform uniform crossover on pairs of parents with probability pc.'''
    # Extract pairs of parents
    parent1 = parents[::2, :]
    parent2 = parents[1::2, :]
    
    # Determine which pairs should crossover
    nocrossover = np.random.rand(parent1.shape[0]) > pc
    mask = np.random.rand(parent1.shape[0], parent1.shape[1]) > 0.5
    mask[nocrossover,:] = False
    
    # Perform uniform crossover
    child1 = parent1.copy()
    child2 = parent2.copy()
    child1[mask] = parent2[mask]
    child2[mask] = parent1[mask]
    
    return np.r_[child1, child2]


def mutation(children, pm):
    '''Perform random resetting mutation on children with per-gene probability pm.'''
    m, n = children.shape # number of children, number of genes
    mask = np.random.rand(m, n) <= pm
    newvalues = initialize(m, n)
    children[mask] = newvalues[mask]
    
    return children
    
def selectsurvivors(population, mutants):
    '''Fitness-based survivor selection (and sorting) of population + mutated children.'''
    m = population.shape[0]
    candidates = np.r_[population, mutants]
    
    score = fitness(candidates)
    order = np.argsort(score)  # sort fitness in ascending order (we want to minimize it!)
    candidates = candidates[order, :]  # rearrange population based on fitness
    score = score[order]
    
    return candidates[:m, :], score[:m]
    
    
# Setup parameters
N = 8  # size of checkerboard
m = 100  # size of population
n = 100  # number of offspring
k = 5  # size of tournament for parent selection
pc = 0.8  # probability of crossover
pm = 0.2  # probability of mutation
maxiter = 100  # maximum number of iterations
pause = 0.05  # amount of time to pause in between generations

size = 45  # size of each checkerboard square, in pixels (for graphics)
margin = 20  # border around board, in pixels (for graphics)

# Set seed for repeatability
np.random.seed(4)

# Draw blank checkerboard
win = checkerboard.draw(rows=N, cols=N, size=size, margin=margin)

# Run genetic algorithm
population = initialize(m, N)
score = fitness(population)
order = np.argsort(score)  # sort fitness in ascending order (we want to minimize it!)
population = population[order, :]  # rearrange population based on fitness

queens = checkerboard.add(win, population[0, :], rows=N, cols=N, size=size, margin=margin)
time.sleep(pause)

average = np.full(maxiter, np.nan)
best = np.full(maxiter, np.nan)
for i in range(maxiter):
    parents = selectparents(population, n, k)
    children = crossover(parents, pc)
    mutants = mutation(children, pm)
    population, score = selectsurvivors(population, mutants)
    average[i] = score.mean()
    best[i] = score[0]
    print('generation {0}, average {1:0.2f}, best {2:0.2f}'.format(i + 1, average[i], best[i]))
    
    # Update GUI
    checkerboard.move(win, queens, population[0, :], rows=N, cols=N, size=size, margin=margin)
    time.sleep(pause)
    
    # Terminate if perfect solution is found
    if best[i] == 0:
        break

print("best solution:", population[0,:])

# Wait for user input to close the GUI
while True:
    key = win.checkKey()
    if key == 'q':
        break  # exit loop when 'q' is pressed
win.close()


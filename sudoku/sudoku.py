#! /usr/bin/env python
"""Solve a Sudoku puzzle using a genetic algorithm."""
import argparse
import os
import numpy as np
import ipdb

# Command Line info when running
parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle using a genetic algorithm.")
parser.add_argument('-d', '--datafile', help="path to text file containing partially-filled Sudoku puzzle(s)",
                    default=os.path.join(os.getcwd(), 'puzzles.txt'))
parser.add_argument('-i', '--index', help="index of puzzle in data file", type=int, default=1)
parser.add_argument('-s', '--seed', help="seed for random number generator", type=int, default=4)


def main(args):
    # Parse input arguments
    datafile = os.path.expanduser(args.datafile)
    index = args.index
    seed = args.seed

    # Set random number generator
    np.random.seed(seed)
    # Read requested Sudoku puzzle from file
    print("Reading Sudoku puzzle from file:", datafile)

    # Reading in the file
    fb = open(datafile, 'r')
    puzzle = fb.readlines()
    puzzle = int(puzzle[index - 1])
    puzzle = np.array([int(x) for x in str(puzzle)])

    # Run genetic algorithm
    print("Running genetic algorithm...")
    mu = 10  # size of population
    n = 10  # number of offspring
    pc = 0.7 # probability of crossover
    pm = 0.5  # probability of mutation
    k = 5  # tournament size
    maxiter = 10000  # maximum number of iterations

    population = initialize(mu, puzzle)
    score = fitness(population)
    order = np.argsort(score)  # sort fitness in ascending order
    population = population[order, :]  # rearrange population based on fitness

    average = np.full(maxiter, np.nan)
    best = np.full(maxiter, np.nan)

    for i in range(maxiter):
        parents = selectparents(population, n, k)
        children = crossover(parents, pc, n)
        mutants = mutation(children, pm, puzzle)
        population, score = selectsurvivors(population, mutants, n)
        average[i] = score.mean()
        best[i] = score[0]
        print('generation {0}, average {1:0.2f}, best {2:0.2f}'.format(i + 1, average[i], best[i]))
        if best[i] == 0:
            break


def initialize(mu, puzzle):
    '''Initialize a population of mu individuals representing potential Sudoku solutions.'''
    fixed = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])  # all the numbers in a line of sudoku to compare to later
    split = np.split(puzzle, 9)  # splits the puzzle in segments of 9 in length
    pop = np.empty((mu, len(puzzle)))  # holds the number of people to create for the population
    for r in range(mu):
        child = np.empty(0)  # will get filled with the values created for the child
        for i in range(9):
            j = 0  # used to replace 0 with new numbers
            p12 = split[i].copy()  # copying the segment of the puzzle at i
            dif = np.setdiff1d(fixed, p12)  # finding the numbers that are not current in i
            perm = np.random.permutation(dif)  # creating a permutation of those numbers
            for k in range(9):  # looping over the current segment
                if p12[k] == 0:  # if the value is a 0
                    p12[k] = perm[j]  # replace it with the current value at j
                    j += 1  # increment J so that every value in the permutation gets used in the order
            child = np.concatenate((child, p12))  # adding the segment back to the child
        pop[r] = child.astype(int)  # adding the child to the population
    return pop.astype(int)


def fitness(population):
    '''Compute the fitness of every individual in the population.'''
    fixed = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    fitt = np.empty(len(population))
    for i in range(len(population)):
        fit = 0
        child = population[i].copy()
        col1 = np.array(
            [child[0], child[9], child[18], child[27], child[36], child[45], child[54], child[63], child[72]])
        fit += len(np.setdiff1d(fixed, col1))  # finding the numbers that are not in the column
        col2 = np.array(
            [child[1], child[10], child[19], child[28], child[37], child[46], child[55], child[64], child[73]])
        fit += len(np.setdiff1d(fixed, col2))  # finding the numbers that are not in the column
        col3 = np.array(
            [child[2], child[11], child[20], child[29], child[38], child[47], child[56], child[65], child[74]])
        fit += len(np.setdiff1d(fixed, col3))  # finding the numbers that are not in the column
        col4 = np.array(
            [child[3], child[12], child[21], child[30], child[39], child[48], child[57], child[66], child[75]])
        fit += len(np.setdiff1d(fixed, col4))  # finding the numbers that are not in the column
        col5 = np.array(
            [child[4], child[13], child[22], child[31], child[40], child[49], child[58], child[67], child[76]])
        fit += len(np.setdiff1d(fixed, col5))  # finding the numbers that are not in the column
        col6 = np.array(
            [child[5], child[14], child[23], child[32], child[41], child[50], child[59], child[68], child[77]])
        fit += len(np.setdiff1d(fixed, col6))  # finding the numbers that are not in the column
        col7 = np.array(
            [child[6], child[15], child[24], child[33], child[42], child[51], child[60], child[69], child[78]])
        fit += len(np.setdiff1d(fixed, col7))  # finding the numbers that are not in the column
        col8 = np.array(
            [child[7], child[16], child[25], child[34], child[43], child[52], child[61], child[70], child[79]])
        fit += len(np.setdiff1d(fixed, col8))  # finding the numbers that are not in the column
        col9 = np.array(
            [child[8], child[17], child[26], child[35], child[44], child[53], child[62], child[71], child[80]])
        fit += len(np.setdiff1d(fixed, col9))  # finding the numbers that are not in the column
        box1 = np.array(
            [child[0], child[1], child[2], child[9], child[10], child[11], child[18], child[19], child[20]])
        fit += len(np.setdiff1d(fixed, box1))  # finding the numbers that are not in the box
        box2 = np.array(
            [child[3], child[4], child[5], child[12], child[13], child[14], child[21], child[22], child[23]])
        fit += len(np.setdiff1d(fixed, box2))  # finding the numbers that are not in the box
        box3 = np.array(
            [child[6], child[7], child[8], child[15], child[16], child[17], child[24], child[25], child[26]])
        fit += len(np.setdiff1d(fixed, box3))  # finding the numbers that are not in the box
        box4 = np.array(
            [child[27], child[28], child[29], child[36], child[37], child[38], child[45], child[46], child[47]])
        fit += len(np.setdiff1d(fixed, box4))  # finding the numbers that are not in the box
        box5 = np.array(
            [child[30], child[31], child[32], child[39], child[40], child[41], child[48], child[49], child[50]])
        fit += len(np.setdiff1d(fixed, box5))  # finding the numbers that are not in the box
        box6 = np.array(
            [child[33], child[34], child[35], child[42], child[43], child[44], child[51], child[52], child[53]])
        fit += len(np.setdiff1d(fixed, box6))  # finding the numbers that are not in the box
        box7 = np.array(
            [child[54], child[55], child[56], child[63], child[64], child[65], child[72], child[73], child[74]])
        fit += len(np.setdiff1d(fixed, box7))  # finding the numbers that are not in the box
        box8 = np.array(
            [child[57], child[58], child[59], child[66], child[67], child[68], child[75], child[76], child[77]])
        fit += len(np.setdiff1d(fixed, box8))  # finding the numbers that are not in the box
        box9 = np.array(
            [child[60], child[61], child[62], child[69], child[70], child[71], child[78], child[79], child[80]])
        fit += len(np.setdiff1d(fixed, box9))  # finding the numbers that are not in the box

        fitt[i] = fit
    return fitt


def selectparents(population, n, k):
    '''Select n parents from the current population.'''
    x = np.random.randint(population.shape[0], size=(n, k))
    indices = x.min(axis=1)
    return population[indices, :]


def crossover(parents, pc, n):
    '''Perform uniform crossover on Sudoku rows from pairs of parents with probability pc.'''
    tempC = np.empty((n, 81))
    par1 = parents[::2]
    par2 = parents[1::2]
    for l in range(n):
        child = np.empty(0)
        for i in range(9):
            if pc < np.random.rand():
                p1 = par1[np.random.randint(len(par1))]
                p1 = np.split(p1, 9)
                child = np.concatenate((child, p1[i]))
            else:
                p2 = par2[np.random.randint(len(par2))]
                p2 = np.split(p2, 9)
                child = np.concatenate((child, p2[i]))
        tempC[l] = child.astype(int)
    return tempC


def mutation(children, pm, puzzle):
    '''Perform swap mutation on Sudoku rows of children with per-row probability pm.'''
    split = np.split(puzzle, 9)  # splits the puzzle in segments of 9 in length
    for j in range(len(children)):
        for i in range(9):
            if np.random.rand() < pm:
                temprow = split[i].copy()
                tempChild = np.split(children[j], 9)
                position1 = np.random.randint(9)
                position2 = np.random.randint(9)
                while position2 == position1:  # so you cant flip the same position
                    position2 = np.random.randint(9)

                # if the value at the random places are not 0 skip mutation
                if temprow[position1] != 0 or temprow[position2] != 0:
                    break
                # else swap the positions because its legal
                else:
                    childrow = tempChild[i]
                    temp = int(childrow[position1])
                    childrow[position1] = childrow[position2]
                    childrow[position2] = temp
    return children


def selectsurvivors(population, mutants, n):
    '''Fitness-based survivor selection (and sorting) of population + mutated children.'''
    candidates = np.r_[population, mutants]

    score = fitness(candidates)
    order = np.argsort(score)  # sort fitness in ascending order (we want to minimize it!)
    candidates = candidates[order, :]  # rearrange population based on fitness
    score = score[order]
    return candidates[:n, :], score[:n]


if __name__ == '__main__':
    main(parser.parse_args())


#ipdb.set_trace()

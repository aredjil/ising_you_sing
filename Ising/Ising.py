#!/usr/bin/env python3
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
from tqdm import tqdm 
import os 
from numba import njit 
from Ising.vis_utils import * 

cmap = mcolors.ListedColormap(["#99d8c9", "#2ca25f"])

#NOTE: COMMENT THE CLASS and its methods. 
class Ising:
    def __init__(self, n:int, p:float|None, kb:float, J:float, Temp:float, t_max:float, seed:np.int32|None):
        
        self._n = n # Dimension of the lattice of the lattice 
        self._p = p # Probability of a spin being down
        self._kb = kb # Boltzmann constant 
        self._beta = 1 / Temp 
        self._J = J # coupling constant
        self._Temp = Temp # Temperature  
        self._t_max = t_max 
        self._lattice = self.make_lattice()

    def make_lattice(self):
        # Generate a lattice randomly 
        n = self._n
        p = self._p  
        return np.random.choice([-1, 1], size=(n, n), p=[p, 1-p])
    @staticmethod
    @njit 
    def calculate_energy(lattice, J):
        n = lattice.shape[0] 
        energy = 0
        for i in range(n):
            for j in range(n):
                S = lattice[i, j]
                # Nearest neighbors
                neighbors = lattice[(i+1)%n, j] + lattice[i, (j+1)%n] + \
                            lattice[(i-1)%n, j] + lattice[i, (j-1)%n]
                energy += -J * S * neighbors
        return energy / 2  
    @staticmethod
    @njit
    def metropolis_step(lattice, n, beta, J):
        for _ in range(n*n):
            i, j = np.random.randint(0, n, 2)  
            S = lattice[i, j]
            neighbors = lattice[(i+1)%n, j] + lattice[i, (j+1)%n] + \
                        lattice[(i-1)%n, j] + lattice[i, (j-1)%n]
            dE = 2 * J * S * neighbors
            if dE < 0 or np.random.rand() < np.exp(-beta * dE):
                lattice[i, j] *= -1
    @staticmethod
    # @njit
    def simulate(lattice, T, beta, J, t_max):
        lattice = lattice.copy()
        n = lattice.shape[0]
        beta = 1 / T
        magnetization = []
        energy = []
        for step in tqdm(range(t_max), desc="Computing"):
            Ising.metropolis_step(lattice, n, beta, J)
            if step > t_max // 3:  # Collect data after equilibration
                magnetization.append(np.abs(np.sum(lattice)) / (n*n))
                energy.append(Ising.calculate_energy(lattice, J) / (n*n))
        return lattice, np.mean(magnetization), np.mean(energy), np.var(energy) * beta**2, np.var(magnetization) * beta
    def run_simulation(self):
        return Ising.simulate(self._lattice, self._Temp, self._beta, self._J, self._t_max)



#!/usr/bin/env python3
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
from tqdm import tqdm 
import os 
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
    
    def calculate_energy(self, lattice):
        J = self._J 
        n = self._n 
        energy = 0
        for i in range(n):
            for j in range(n):
                S = lattice[i, j]
                # Nearest neighbors
                neighbors = lattice[(i+1)%n, j] + lattice[i, (j+1)%n] + \
                            lattice[(i-1)%n, j] + lattice[i, (j-1)%n]
                energy += -J * S * neighbors
        return energy / 2  
    def metropolis_step(self, lattice):
        n = self._n         
        beta = self._beta 
        J = self._J 
        for _ in range(n**2):
            i, j = np.random.randint(0, n, 2)  
            S = lattice[i, j]

            neighbors = lattice[(i+1)%n, j] + lattice[i, (j+1)%n] + \
                        lattice[(i-1)%n, j] + lattice[i, (j-1)%n]
            dE = 2 * J * S * neighbors
            if dE < 0 or np.random.rand() < np.exp(-beta * dE):
                lattice[i, j] *= -1
    def simulate(self):

        lattice = self._lattice.copy()
        T = self._Temp
        steps = self._t_max
        J = self._J 
        n = self._n
        beta = 1 / T
        magnetization = []
        energy = []
        for step in tqdm(range(steps), desc="Computing"):
            self.metropolis_step(lattice)
            if step > steps // 2:  # Collect data after equilibration
                magnetization.append(np.abs(np.sum(lattice)) / (n*n))
                energy.append(self.calculate_energy(lattice) / (n*n))
        return lattice, np.mean(magnetization), np.mean(energy), np.var(energy) * beta**2, np.var(magnetization) * beta



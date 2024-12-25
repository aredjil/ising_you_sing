#!/usr/bin/env python3
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
from tqdm import tqdm 

cmap = mcolors.ListedColormap(["#99d8c9", "#2ca25f"])
class Ising:

    def __init__(self, n:int, p:float|None, kb:float, J:float, Temp:float, t_max:float, seed:np.int32|None):
        
        self._n = n # Dimension of the lattice of the lattice 
        self._p = p # Probability of a spin being down
        self._kb = kb # Boltzmann constant 
        self._J = J # coupling constant
        self._Temp = Temp # Temperature  
        self._t_max = t_max 
        # if seed is not None:
        #     np.random.seed(seed)
        self._lattice = self.make_lattice()

    def make_lattice(self):
        # Generate a lattice randomly 
        n = self._n
        p = self._p  
        return np.random.choice([-1, 1], size=(n, n), p=[p, 1-p])
    
    def show_lattice(self, lattice, magnetization, iter):
        # Visulize the lattice 
        # lattice = self._lattice # Generated lattice 
        n = self._n 
        padded_lattice = np.pad(lattice, pad_width=1, mode='constant', constant_values=0) # padded lattice to make the visulization pretty  
        
        fig, ax = plt.subplots(figsize=(14, 6), ncols=2, nrows=1)
        cax = ax[0].imshow(lattice, cmap=cmap, origin="upper")

        # cax = ax[0].imshow(padded_lattice[1:n-1, 1:n-1], cmap=cmap, origin="upper")
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        ax[0].grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax[0].tick_params(which='minor', size=0)
        ax[0].set_title(f"Spin Lattice Configuration")
        cbar = plt.colorbar(cax, ax=ax[0], ticks=[-1, 1])
        cbar.ax.set_yticklabels(['-1 (Down)', '1 (Up)'])  # Set labels for the ticks
        # cbar.set_label('$S_i$')

        ax[1].scatter(iter, magnetization[iter], color='#2ca25f', zorder=5, label=f"Lattice magnetization")
        ax[1].plot(range(iter + 1), magnetization[:iter + 1], color='#99d8c9')
        ax[1].set_xlim(0, self._t_max+10)
        ax[1].set_ylim(-1, 1)
        ax[1].set_title("Magnetization Over Time")
        ax[1].set_xlabel("Step")
        ax[1].set_ylabel("Magnetization")
        ax[1].grid()
        ax[1].legend()
        fig.suptitle(f"Spin configuration and Magnetisation of a {n} by {n} square lattice randomly intilized with most spins down, with T={self._Temp}, and J={self._J} for {n*n} steps \n Step: {iter}")
        return fig      
    def compute_magnetization(self, lattice):
        # Compute the magnetisation of the lattice  
        n = self._n 
        return np.sum(lattice) / (n * n)
    
    def solve(self): 
        n = self._n 
        t_max = self._t_max
        lattice = self._lattice.copy()
        magnetization = np.zeros(t_max)
        energy_list = np.zeros(t_max)

        for iter in tqdm(range(0, t_max), desc="Computing..."): 
            lattice, energy = self.metropolis(lattice, energy_list[iter-1])
            magnetization[iter] = self.compute_magnetization(lattice)
            if iter % 10 == 0:
                fig= self.show_lattice(lattice, magnetization, iter)
                fig.savefig(f"./plots/lattice_{iter}.png")
                plt.close(fig)
        return magnetization
    
    def metropolis(self, lattice, old_energy): 
        n = self._n 
        Temp = self._Temp
        i, j = np.random.randint(n, size=2)
        lattice[i, j] *= -1
        # new_energy = self.compute_energy(lattice)
        dE = 2 * self._J * lattice[i, j] * (
        lattice[(i - 1) % n, j] +
        lattice[(i + 1) % n, j] +
        lattice[i, (j - 1) % n] +
        lattice[i, (j + 1) % n]
        )
        # dE = new_energy-old_energy
        if dE < 0 or np.random.rand() < np.exp(-dE / (self._kb * Temp)):
            return lattice, old_energy + dE
        else:
            lattice[i, j] *= -1  # Revert flip
            return lattice, old_energy
    








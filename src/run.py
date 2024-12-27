#!/usr/bin/env python3
import numpy as np 
from Ising.Ising import *
from Ising.vis_utils import * 
from tqdm import tqdm 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
plt.style.use("Solarize_Light2")
cmap = mcolors.ListedColormap(["#99d8c9", "#2ca25f"])
#NOTE: Move the plot_fig function to vis_utils 

def plot_fig(temp, lattice, mag, energies, heat_capacity, iter):
    #NOTE: Create the output folder if it does not already exists. 
    fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(12, 12))
    cax = ax[0, 0].imshow(lattice, cmap=cmap)
    ax[0, 0].set_xticks([])
    ax[0, 0].set_yticks([])
    ax[0, 0].grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax[0, 0].tick_params(which='minor', size=0)
    ax[0, 0].set_title(f"Lattice Configuration")
    cbar = plt.colorbar(cax, ax=ax[0, 0], ticks=[-1, 1])
    cbar.ax.set_yticklabels(['-1 (Down)', '1 (Up)'])

    ax[0, 1].scatter(temp[iter], mag[iter], color="red")
    ax[0, 1].plot(temp[:iter + 1], mag[:iter + 1],  label="$<M>$", color='blue', alpha=0.5)
    ax[0, 1].set_xlim(temp[0], temp[-1])
    ax[0, 1].set_ylim(0, 1.0)
    ax[0, 1].set_title("Magnetization vs Temperature")
    ax[0, 1].set_xlabel("T")
    ax[0, 1].set_ylabel("Magnetization")
    ax[0, 1].grid()
    ax[0, 1].legend()

    ax[1, 0].scatter(temp[iter], energies[iter], color="red")
    ax[1, 0].plot(temp[:iter + 1], energies[:iter + 1], label="E", color='blue', alpha=0.5)
    ax[1, 0].set_xlim(temp[0], temp[-1])
    # ax[1, 0].set_ylim(0, 1.0)
    ax[1, 0].set_title("Energies vs Temperature")
    ax[1, 0].set_xlabel("T")
    ax[1, 0].set_ylabel("Energies")
    ax[1, 0].grid()
    ax[1, 0].legend()

    ax[1, 1].scatter(temp[iter], heat_capacity[iter], color="red")
    ax[1, 1].plot(temp[:iter + 1], heat_capacity[:iter + 1], label="$C_v$", color='blue', alpha=0.5)
    ax[1, 1].set_xlim(temp[0], temp[-1])
    # ax[1, 1].set_ylim(0, 1.0)
    ax[1, 1].set_title("Heat Capacity vs Temperature")
    ax[1, 1].set_xlabel("T")
    ax[1, 1].set_ylabel("Heat Capacity")
    ax[1, 1].grid()
    ax[1, 1].legend()

    fig.suptitle(f"T={temp[iter]:.2f}")
    plt.tight_layout()
    return fig
def main():
    n, seed, p= 32, 42, 0.2
    kb, J = 1.0, 1.0
    t_max = 10000
    temp = np.linspace(1.53, 3.28, 50)
    mag = []
    heat_capacity = []
    energies = []
    chies = []
    lattices = []
    for iter, T in enumerate(temp):
        ising = Ising(n=n, 
            p=p,
            kb=kb, 
            J=J,
            Temp=T,
            t_max = t_max,
            seed=seed)
        lattice, m, e, cv, _ = ising.simulate()
        energies.append(e)
        heat_capacity.append(cv)
        lattices.append(lattice)
        mag.append(m) 
        fig = plot_fig(temp, lattice, mag, energies, heat_capacity, iter)
        fig.savefig(f"./plots/plot_{iter}.png")
        plt.close(fig)
if __name__ =="__main__":
    # path = "./plots" # Path for a temporary directory where to save plots 
    # main()
    path = "./plots"
    input_file_name = "plot_"
    output_file_name ="ising"
    duration = 200 

    gen_gif(50, 0, 1, duration, input_file_name, path, output_file_name)

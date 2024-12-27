#!/usr/bin/env python3
import numpy as np 
from Ising.Ising import *
from Ising.vis_utils import * 
from tqdm import tqdm 
import matplotlib.pyplot as plt 
import time as time 
plt.style.use("Solarize_Light2")
#NOTE: Move the plot_fig function to vis_utils 


def main():
    n, seed, p= 32, 42, 0.1
    kb, J = 1.0, 1.0
    t_max = 100_000
    temp = np.linspace(1.53, 3.28, 50)
    mag = []
    heat_capacity = []
    energies = []
    chies = []
    lattices = []
    start = time.time()
    for iter, T in enumerate(temp):
        ising = Ising(n=n, 
            p=p,
            kb=kb, 
            J=J,
            Temp=T,
            t_max = t_max,
            seed=seed)
        lattice, m, e, cv, _ = ising.run_simulation()
        energies.append(e)
        heat_capacity.append(cv)
        lattices.append(lattice)
        mag.append(m) 
        fig = plot_fig(temp, lattice, mag, energies, heat_capacity, iter)
        fig.savefig(f"./plots/plot_{iter}.png")
        plt.close(fig)
    end = time.time()
    print(f"Computations took: {end-start} s")
if __name__ =="__main__":
    # path = "./plots" # Path for a temporary directory where to save plots 
    main()
    path = "./plots"
    input_file_name = "plot_"
    output_file_name ="ising"
    duration = 200 

    gen_gif(50, 0, 1, duration, input_file_name, path, output_file_name)

#!/usr/bin/env python3
import numpy as np 
from Ising.Ising import *
from Ising.vis_utils import * 
#NOTE: The code needs to be generlized. 
#NOTE: Add magnetisation vs temperature 
def main():
    n, seed, p = 100, 42, 0.8
    kb, J, T = 1.0, 1.0, 1.0
    t_max = n * n 
    ising = Ising(n=n, 
                  p=p,
                  kb=kb, 
                  J=J,
                  Temp=T,
                  t_max = t_max,
                  seed=seed)
    m = ising.solve()
if __name__ =="__main__":
    path = "./plots" # Path for a temporary directory where to save plots 
    main()
    gen_gif(10000, 0, 10, 10, path)
    #NOTE: there is a minro error in the removing file, fix it 
    # remove_plots(1000, 0, 50, path)

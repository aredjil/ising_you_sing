#!/usr/bin/env python3 
import numpy as np 
import matplotlib.pyplot as plt 
from tqdm import tqdm
from PIL import Image 
import matplotlib.colors as mcolors
import os 

cmap = mcolors.ListedColormap(["#99d8c9", "#2ca25f"])

def create_gif(input_files_path:str, input_file_name:str, output_path:str, output_file_name:str, m_range:int, duration:int=100):
    """
    Generate a gif using saved plots. 
    input_files_path: Path of the folder where the plots are stored. 
    input_file_name:  Base name of the files that contain the figures. 
    output_path: Ouput path where to save the generated gif.
    output_file_name: Name of the gif file e.g 'something.gif'
    m_range: Generator of the prefix of the figure files e.g. something_1.png  
    duration: duration per frame in milliseconds 
    """
    images = []
    try:
        os.makedirs(output_path, exist_ok=True)
        print(f"Created {output_path}")
    except Exception as e: 
        print(f"An execption occured {e}")
    try:
        print("Generating the GIF...")
        for m in m_range:
            file_name = input_file_name +f"{m}.png"  
            file_path = os.path.join(input_files_path, file_name)
            if os.path.exists(file_path):
                img = Image.open(file_path)
                images.append(img.copy())
                img.close()
            else:
                print(f"File not found: {file_path}")
        
        if images:
            images[0].save(
                output_path+"/"+output_file_name+".gif",
                save_all=True,
                append_images=images[1:],  
                duration=duration, 
                loop=0  
            )
            print(f"GIF saved at {output_path}")
        else:
            print("No images were found to create a GIF.")
    except Exception as e:
        print(f"An error occurred: {e}")

def gen_gif(max_m:int, min_m:int, step_m:int, duration:int, input_file_name, input_file_path:str, output_file_name:str):
    """
    Helper function to generate the gif
    max_m: Number of plots.
    min_m: Start of numbering.
    step_m: Number between each plot and plot  
    duration: duration per frame in milliseconds. 
    input_file_name: Name of the input file. 
    input_file_path: path for the input files. 
    output_file_name: Ouput file name. 
    """
    output_gif = "./gifs"  
    m_range = range(min_m, max_m, step_m) 
    duration_per_frame = duration  
    create_gif(input_file_path, input_file_name, output_gif,output_file_name,  m_range, duration=duration_per_frame)

def remove_plots(max_m:int, min_m:int, step_m:int, path):
    """
    Helper function to remove the produced plots. 
    """
    for m in range(min_m, max_m, step_m):
        file_path = f"./{path}/plot_{m}.png"
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e: 
                print(f"An error occured while removing {file_path} {e}")
    os.rmdir(path)
    print(f"removed {path}")

def plot_fig(temp, lattice, mag, energies, heat_capacity, iter):
    #NOTE: Create the output folder if it does not already exists. 
    n = lattice.shape[0]
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
    ax[0, 1].set_title("<M> vs T")
    ax[0, 1].set_xlabel("T")
    ax[0, 1].set_ylabel("<M>")
    ax[0, 1].grid()
    ax[0, 1].legend()

    ax[1, 0].scatter(temp[iter], energies[iter], color="red")
    ax[1, 0].plot(temp[:iter + 1], energies[:iter + 1], label="E", color='blue', alpha=0.5)
    ax[1, 0].set_xlim(temp[0], temp[-1])
    ax[1, 0].set_ylim(energies[0], 0.0)
    ax[1, 0].set_title("E vs T")
    ax[1, 0].set_xlabel("T")
    ax[1, 0].set_ylabel("E")
    ax[1, 0].grid()
    ax[1, 0].legend()

    ax[1, 1].scatter(temp[iter], heat_capacity[iter], color="red")
    ax[1, 1].plot(temp[:iter + 1], heat_capacity[:iter + 1], label="$C_v$", color='blue', alpha=0.5)
    ax[1, 1].set_xlim(temp[0], temp[-1])
    # ax[1, 1].set_ylim(0, 1.0)
    ax[1, 1].set_title("$C_v$ vs T")
    ax[1, 1].set_xlabel("T")
    ax[1, 1].set_ylabel("$C_v$")
    ax[1, 1].grid()
    ax[1, 1].legend()

    fig.suptitle(f"{n}*{n} Lattice \nT={temp[iter]:.2f}")
    plt.tight_layout()
    return fig
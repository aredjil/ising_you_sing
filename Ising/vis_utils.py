#!/usr/bin/env python3 
import numpy as np 
import matplotlib.pyplot as plt 
from tqdm import tqdm
from PIL import Image 
import os 

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
                output_path+output_file_name+".gif",
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
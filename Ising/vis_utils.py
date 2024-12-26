#!/usr/bin/env python3 
import numpy as np 
import matplotlib.pyplot as plt 
from tqdm import tqdm
from PIL import Image 
import os 

def create_gif(image_folder, output_path, m_range, duration=100):
    images = []
    try:
        os.makedirs(output_path, exist_ok=True)
        print(f"Created {output_path}")
    except Exception as e: 
        print(f"An execption occured {e}")
    try:
        print("Generating the GIF...")
        for m in m_range:
            file_name = f"plot_{m}.png"  
            file_path = os.path.join(image_folder, file_name)
            if os.path.exists(file_path):
                img = Image.open(file_path)
                images.append(img.copy())
                img.close()
            else:
                print(f"File not found: {file_path}")
        
        if images:
            images[0].save(
                output_path+"/ising.gif",
                save_all=True,
                append_images=images[1:],  
                duration=duration  
            )
            print(f"GIF saved at {output_path}")
        else:
            print("No images were found to create a GIF.")
    except Exception as e:
        print(f"An error occurred: {e}")
def gen_gif(max_m:int, min_m:int, step_m:int, duration:int, hist_path:str):
    output_gif = "./gifs"  
    m_range = range(min_m, max_m, step_m) 
    duration_per_frame = duration  

    create_gif(hist_path, output_gif, m_range, duration=duration_per_frame)

def remove_plots(max_m:int, min_m:int, step_m:int, path):
    for m in range(min_m, max_m, step_m):
        file_path = f"./{path}/lattice_{m}.png"
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e: 
                print(f"An error occured while removing {file_path} {e}")
    os.rmdir(path)
    print(f"removed {path}")
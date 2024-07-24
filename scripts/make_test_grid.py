'''

Goal: Make a test grid composed of random images from 5 test grids with varying image sizes.
Steps:
1. Define Grid and Image Sizes: Set the dimensions for the grids and the individual image sizes.
2. Load Images from MRC Files: The load_images_from_mrc function reads an MRC file and extracts images centered in the grid.
3. Random Image Selection: For each cell in Grid 6, a random image is selected from one of the 5 grids.
4. Create a Large Grid Image: The create_grid_image function assembles the randomly selected images into a single large image.
5. Save grid to .png and .mrc files

'''

import random
import numpy as np
import mrcfile
from PIL import Image

# Function to load images from an MRC file
def load_images_from_mrc(mrc_path, image_size, grid_size):
    """
    Load images from an MRC file and return them as a list of numpy arrays.
    """
    with mrcfile.open(mrc_path, permissive=True) as mrc:
        data = mrc.data

    images = []
    rows, cols = grid_size
    img_h, img_w = image_size
    for i in range(rows):
        for j in range(cols):
            # Calculate the position to extract the image
            y_start = i * img_h
            y_end = y_start + img_h
            x_start = j * img_w
            x_end = x_start + img_w
            image = data[y_start:y_end, x_start:x_end]
            images.append(image)
    return images

# Create a large image for Grid 6
def create_grid_image(images, rows, cols, image_sizes):
    """
    Create a large image composed of smaller images in a grid layout.
    """
    max_width = max(size[0] for size in image_sizes.values())
    max_height = max(size[1] for size in image_sizes.values())
    
    grid_width = cols * max_width
    grid_height = rows * max_height
    
    # Create an empty grid with Gaussian noise background
    grid_image_data = np.random.normal(0.5, 0.1, (grid_height, grid_width)).astype(np.float32)

    for i, img in enumerate(images):
        img_h, img_w = img.shape
        row = i // cols
        col = i % cols
        x = col * max_width + (max_width - img_w) // 2
        y = row * max_height + (max_height - img_h) // 2
        grid_image_data[y:y+img_h, x:x+img_w] = img

    return grid_image_data

# Normalize the image data for PNG
def normalize_image_data(data):
    """
    Normalize the image data to the range 0-255 for PNG saving.
    """
    data_min = np.min(data)
    data_max = np.max(data)
    return ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)

# Save the final Grid 6 image to a PNG file
def save_image_to_png(image_data, path):
    """
    Save numpy array image data to a PNG file.
    """
    image_normalized = normalize_image_data(image_data)
    image_pil = Image.fromarray(image_normalized, mode='L')
    image_pil.save(path)
    image_pil.show()

# Save the Grid 6 image as MRC
def save_to_mrc(image_data, mrc_path):
    """
    Save a numpy array to an MRC file.
    """
    with mrcfile.new(mrc_path, overwrite=True) as mrc:
        mrc.set_data(image_data.astype(np.float32))  # Ensure the data is in float32 format for MRC

# Define the grid size and image sizes
grid_size = (16, 15)
image_sizes = {
    1: (64, 64),
    2: (64, 64),
    3: (80, 80),
    4: (84, 84),
    5: (88, 88)
}

# 1 = apo; #2 beta_gal; #3 = virus; #4 = thg;  #5 = ribo
grid1 = "/hpc/projects/group.czii/phil.smoot/topaz_wrapper/execute_projects/composite/base_composite_micrographs/particles_001.mrc"
grid2 = "/hpc/projects/group.czii/phil.smoot/topaz_wrapper/execute_projects/composite/base_composite_micrographs/particles_002.mrc"
grid3 = "/hpc/projects/group.czii/phil.smoot/topaz_wrapper/execute_projects/composite/base_composite_micrographs/particles_003.mrc"
grid4 = "/hpc/projects/group.czii/phil.smoot/topaz_wrapper/execute_projects/composite/base_composite_micrographs/particles_004.mrc"
grid5 = "/hpc/projects/group.czii/phil.smoot/topaz_wrapper/execute_projects/composite/base_composite_micrographs/particles_005.mrc"

# Load images from each MRC file
grid_images = {
    1: load_images_from_mrc(grid1, image_sizes[1], grid_size),
    2: load_images_from_mrc(grid2, image_sizes[2], grid_size),
    3: load_images_from_mrc(grid3, image_sizes[3], grid_size),
    4: load_images_from_mrc(grid4, image_sizes[4], grid_size),
    5: load_images_from_mrc(grid5, image_sizes[5], grid_size)
}

# Create Grid 6 by randomly selecting images from the first 5 grids
grid_6_images = []    
particles1_data = []
particles2_data = []
particles3_data = []
particles4_data = []
particles5_data = []


# for _ in range(grid_size[0] * grid_size[1]):
for row in range(16):
    for col in range(15):
        
        center_x = col * 88 + 88 // 2
        center_y = row * 88 + 88 // 2
 
        random_grid = random.randint(1, 5)

        if random_grid == 1:
            particles1_data.append(("composite_particles", center_x, center_y))
        elif random_grid == 2:
            particles2_data.append(("composite_particles", center_x, center_y))
        elif random_grid == 3:
            particles3_data.append(("composite_particles", center_x, center_y))
        elif random_grid == 4:
            particles4_data.append(("composite_particles", center_x, center_y))
        else:
           particles5_data.append(("composite_particles", center_x, center_y))
             
        random_image = random.choice(grid_images[random_grid])
        grid_6_images.append(random_image)

# Write data to the output file
with open("apo_composite_particles.txt", 'w') as f:
    # write the header
    var1 = "image_name"
    var2 = "x_coord"
    var3 = "y_coord"
    f.write(f"{var1}\t{var2}\t{var3}\n")
    # write the data
    for item in particles1_data:
        f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

# Write data to the output file
with open("beta_gal_composite_particles.txt", 'w') as f:
    # write the header
    var1 = "image_name"
    var2 = "x_coord"
    var3 = "y_coord"
    f.write(f"{var1}\t{var2}\t{var3}\n")
    # write the data
    for item in particles2_data:
        f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

# Write data to the output file
with open("virus_composite_particles.txt", 'w') as f:
    # write the header
    var1 = "image_name"
    var2 = "x_coord"
    var3 = "y_coord"
    f.write(f"{var1}\t{var2}\t{var3}\n")
    # write the data
    for item in particles3_data:
        f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

# Write data to the output file
with open("thg_composite_particles.txt", 'w') as f:
    # write the header
    var1 = "image_name"
    var2 = "x_coord"
    var3 = "y_coord"
    f.write(f"{var1}\t{var2}\t{var3}\n")
    # write the data
    for item in particles4_data:
        f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

# Write data to the output file
with open("ribo_composite_particles.txt", 'w') as f:
    # write the header
    var1 = "image_name"
    var2 = "x_coord"
    var3 = "y_coord"
    f.write(f"{var1}\t{var2}\t{var3}\n")
    # write the data
    for item in particles5_data:
        f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

# Create the final Grid 6 image
grid_6_image_data = create_grid_image(grid_6_images, grid_size[0], grid_size[1], image_sizes)

# Save the Grid 6 image as PNG
save_image_to_png(grid_6_image_data, 'composite_particles.png')

# Save the Grid 6 image as MRC
save_to_mrc(grid_6_image_data, 'composite_particles.mrc')

print("Grid 6 saved to composite_particles.png and composite_particles.mrc")
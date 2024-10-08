import os

def calculate_centers(grid_size, image_size, project_name, output_file):
    """
    Calculate the center coordinates of each image in a grid and save to a file.

    Parameters:
    - grid_size: Tuple (rows, cols) specifying the number of rows and columns in the grid.
    - image_size: Tuple (width, height) specifying the size of each image in pixels.
    - project_name: String specifying the directory name for the project
    - output_file: String specifying the filename to save the coordinates.

    """
    # Unpack grid_size
    rows, cols = grid_size

    # Unpack image_size
    img_width, img_height = image_size

    # Initialize list to store image identifiers and centers
    data = []

    # Iterate over each file name
    for filename in os.listdir("/home/phil.smoot/projects/phil.smoot/raw_data/curated_ml_challenge/" + project_name ):

        if filename.endswith('.mrc'):
            # Iterate over each grid position
            for row in range(rows):
                for col in range(cols):
                    # Calculate center of current image
                    center_x = col * img_width + img_width // 2
                    center_y = row * img_height + img_height // 2
                
                    base_name = os.path.splitext(filename)[0]
                    # Append to data list
                    data.append((base_name, center_x, center_y))

    # Write data to the output file
    with open(output_file, 'w') as f:
        # write the header
        var1 = "image_name"
        var2 = "x_coord"
        var3 = "y_coord"
        f.write(f"{var1}\t{var2}\t{var3}\n")
        # write the data
        for item in data:
            f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

    print(f"Center coordinates saved to '{output_file}'")

# Example usage:
# calculate_centers((16, 15), (88, 88), 'ml_challenge', 'particles_88x88, ml_challenge.txt')
# calculate_centers((16, 15), (88, 88), 'ml_challenge_with_junk', 'particles_88x88, ml_challenge_with_junk.txt')
calculate_centers((16, 15), (64, 64), 'apo-ferritin', 'particles_64x64_apo.txt')
calculate_centers((16, 15), (64, 64), 'beta-galactosidase', 'particles_64x64_beta_gal.txt')
calculate_centers((16, 15), (80, 80), 'virus-like-particle', 'particles_80x80_virus.txt')
calculate_centers((16, 15), (84, 84), 'thyroglobulin', 'particles_84x84_thg.txt')
calculate_centers((16, 15), (88, 88), 'ribosome_iter1', 'particles_88x88_ribo.txt')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
import glob
import os
import sys
import argparse

#
# print out a plot of predicted and ground truth overlays
# save plots to png files
# 

def main(root_path, dataset_path, predicted_particles_file_path, processed_particles_file_path, \
         processed_images, train_targets, radius, number_of_images_to_visualize, display_plots, score):
    
    root_path = root_path
    dataset_path = dataset_path
    predicted_particles_file_path = predicted_particles_file_path
    processed_particles_file_path = processed_particles_file_path
    processed_images = processed_images + "*.mrc"
    train_targets = train_targets
    radius = int(radius)

    sys.path.append(root_path)
    from topaz.utils.data.loader import load_image

    predicted_particles = pd.read_csv(predicted_particles_file_path, sep='\t')
    predicted_particles.head()

    # plot the distribution of scores (predicted log-likelihood ratios)
    _ = plt.hist(predicted_particles.score, bins=50)
    plt.xlabel('Predicted score (predicted log-likelihood ratio) radius==' + str(radius))
    plt.ylabel('Number of particles')
    plt.savefig(dataset_path + "/scores_distribution_radius_" + str(radius) + ".png")
    if display_plots == "yes":
            plt.show()   

    # print the mumber of particles >= score 
    num_particles =np.sum(predicted_particles.score >= int(score)) # how many particles are predicted with score >= 0
    print("Number of particles with score > " + score + " = " + str(num_particles))

    #
    # Show the overlay of predicted particles and ground truth particles
    #

    ## load the labeled particles
    labeled_particles = pd.read_csv(processed_particles_file_path, sep='\t')

    # print the mumber of ground truth particles
    num_labeled_particles = np.sum(labeled_particles.image_name != "") # number of ground truth particles
    print("Number of labeled particles = " + str(num_labeled_particles))


    ## load the micrographs for visualization
    micrographs = {}
    for path in glob.glob(processed_images):
        im = np.array(load_image(path), copy=False)
        name,_ = os.path.splitext(os.path.basename(path))
        micrographs[name] = im

    images_test = pd.read_csv(train_targets, sep='\t')
    images_test = set(images_test.image_name)
    image_names = list(images_test) # micrograph names for the test set

    for image_name in image_names[:int(number_of_images_to_visualize)]:

        name = image_name
        im = micrographs[name]
        particles = predicted_particles.loc[predicted_particles['image_name'] == name]

        # visualize predicted particles with log-likelihood ratio >= 0 (p >= 0.5)
        particles = particles.loc[particles['score'] >= int(score)]

        #
        # plot the overlay of predicted and truth and show them
        #

        _,ax = plt.subplots(figsize=(16,16))
        ax.imshow(im, cmap='Greys_r', vmin=-3.5, vmax=3.5, interpolation='bilinear')

        # plot the predicted particles in blue
        for x,y in zip(particles.x_coord, particles.y_coord):
            c = Circle((x,y),radius,fill=False,color='b')
            ax.add_patch(c)
        
        # plot the (partial) ground truth particles in red
        ground_truth = labeled_particles.loc[labeled_particles['image_name'] == name]

        for x,y in zip(ground_truth.x_coord, ground_truth.y_coord):
            c = Circle((x,y),radius/2,fill=False,color='r')
            ax.add_patch(c)

        plt.xlabel(name + " predicted==blue(" + str(num_particles) + "); ground_truth==red(" + str(num_labeled_particles) + "); score >= " + score)
        plt.savefig(dataset_path + "/" + name + "_predicted_plus_ground_truth.png")
        if display_plots == "yes":
            plt.show()

    
if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser()
    
    # Add arguments
    parser.add_argument("root_path", type=str)
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("predicted_particles_file_path", type=str)
    parser.add_argument("processed_particles_file_path", type=str)
    parser.add_argument("processed_images", type=str)
    parser.add_argument("train_targets", type=str)
    parser.add_argument("radius", type=str)
    parser.add_argument("number_of_images_to_visualize", type=str)
    parser.add_argument("display_plots", type=str)
    parser.add_argument("score", type=str)  

    # Parse the arguments
    args = parser.parse_args()
    
    # Pass the input strings to the main function
    main(args.root_path, args.dataset_path, args.predicted_particles_file_path, \
         args.processed_particles_file_path, args.processed_images, \
              args.train_targets, args.radius, args.number_of_images_to_visualize, args.display_plots, \
                args.score)


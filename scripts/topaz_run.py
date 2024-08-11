# topaz_run.py
#  - wrapper function around the topaz commands
#   preprocess - downsample and normalize)
#   convert (convert particle coordinates if downsampling > 1)
#   train_test_split (split training and test data sets for model building)
#   train (build model)
#   extract (prediction)
#   visualize (visualize predictions overlaying predictions with ground truth) 

# Usage - $ python topaz_run.py $CONFIG_FILE

import json
import subprocess
import argparse
import os
import time
from logger import Logger

def launch_shell_script(command):

    g_log.loginfo("launch_shell_script", command)    

    # Launch the command in a shell
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # TOOD - figure out why is print statements coming out of stderr versus stdout?
    # Wait for the command to complete and capture output
    stdout, stderr = process.communicate()
    
    # print("Standard Output:")
    print(stdout.decode())
    # print("Standard Error:")
    print(stderr.decode())


def read_json_file(file_path):    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        g_log.loginfo("read_json_file", "Error: File not found: " + file_path)
        return None
    except json.JSONDecodeError:
        g_log.loginfo("read_json_file", "Error: Unable to parse JSON from file" + file_path)
        return None

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        g_log.loginfo("ensure_directory_exists", f"Directory '{directory_path}' created.")
    
def execute_preprocess(params):

    files_path = params['file_paths']
    root_path = files_path['root_path']
    project_name = params['project_name'] 
    project_path = root_path + files_path['projects_path'] + project_name
    processed_images_path = project_path + files_path['processed_images_path']
    rawdata_images = params['rawdata_images']

    preprocess_parameters = params['preprocess_parameters']
    downsampling = str(preprocess_parameters['downsampling'])
    
    command = "topaz preprocess" \
   + "  -v -s " + downsampling \
    + " -o " + processed_images_path \
    + " " + rawdata_images
    
    start_time = time.time()

    launch_shell_script(command) 
    
    end_time = time.time()
    duration = end_time - start_time
    g_log.loginfo("execute_preprocess", f"Function 'execute_preprocess' took {duration:.2f} seconds to complete")
    g_log.logperf(project_name, "execute_preprocess", "duration", f"{duration:.2f}", "seconds")

def execute_convert(params):

    files_path = params['file_paths']
    root_path = files_path['root_path']
    project_name = params['project_name'] 
    project_path = root_path + files_path['projects_path'] + project_name
    processed_particles_file_path = project_path + files_path['processed_particles_file_path']
    rawdata_particles_file_path = params['rawdata_particles']
    preprocess_parameters = params['preprocess_parameters']
    downsampling = str(preprocess_parameters['downsampling'])
    
    command = "topaz convert" \
    + " -s " + downsampling \
    + " -o " + processed_particles_file_path \
    + " " + rawdata_particles_file_path
    
    start_time = time.time()
     
    launch_shell_script(command)

    end_time = time.time()
    duration = end_time - start_time
    g_log.loginfo("execute_convert", f"Function 'execute_convert' took {duration:.2f} seconds to complete")
    g_log.logperf(project_name, "execute_convert", "duration", f"{duration:.2f}", "seconds")

def execute_train_test_split(params):

    files_path = params['file_paths']
    root_path = files_path['root_path']
    project_name = params['project_name'] 
    project_path = root_path + files_path['projects_path'] + project_name
    processed_images_path = project_path + files_path['processed_images_path']
    processed_particles_file_path = project_path + files_path['processed_particles_file_path']
    split_test_train_parameters = params['split_test_train_parameters']
    number_of_held_out_test_images = str(split_test_train_parameters['number_of_held_out_test_images'])
    
    command = "topaz train_test_split" \
    + " -n " + number_of_held_out_test_images \
    + " --image-dir " + processed_images_path \
    + " " + processed_particles_file_path

    start_time = time.time()

    launch_shell_script(command)     

    end_time = time.time()
    duration = end_time - start_time
    g_log.loginfo("execute_train_test_split", f"Function 'execute_train_test_split' took {duration:.2f} seconds to complete")
    g_log.logperf(project_name, "execute_train_test_split", "duration", f"{duration:.2f}", "seconds")

def execute_train(params):

    files_path = params['file_paths']
    root_path = files_path['root_path']
    project_name = params['project_name'] 
    project_path = root_path + files_path['projects_path'] + project_name
    train_images = project_path + files_path['train_images']
    train_targets = project_path + files_path['train_targets']
    test_images = project_path + files_path['test_images']
    test_targets = project_path + files_path['test_targets']
    save_prefix = project_path + files_path['save_prefix']
    model_file_path = project_path + files_path['model_file_path']

    training_parameters = params['training_parameters']
    number_workers = str(training_parameters['number_workers'])
    number_of_predicted_particles = str(training_parameters['number_of_predicted_particles'])
    radius = str(training_parameters['radius'])
    
  
    # command = "python3 " + program_path + 'train.py' \
    command = "topaz train" \
    + " -n " + number_of_predicted_particles \
    + " -r " + radius \
    + " --num-workers=" + number_workers \
    + " --train-images " + train_images \
    + " --train-targets " + train_targets \
    + " --test-images " + test_images \
    + " --test-targets " + test_targets \
    + " --save-prefix " + save_prefix \
    + " -o " + model_file_path

    start_time = time.time()

    launch_shell_script(command)     

    end_time = time.time()
    duration = end_time - start_time
    g_log.loginfo("execute_train", f"Function 'execute_train' took {duration:.2f} seconds to complete")
    g_log.logperf(project_name, "execute_train", "duration", f"{duration:.2f}", "seconds")


def execute_extract(params):

    files_path = params['file_paths']
    root_path = files_path['root_path']
    project_name = params['project_name'] 
    project_path = root_path + files_path['projects_path'] + project_name
    model_path = project_path + files_path['model']
    predicted_particles_file_path = project_path + files_path['predicted_particles_file_path']
    processed_images = project_path + files_path['processed_images']

    extract_parameters = params['extract_parameters']
    radius = str(extract_parameters['radius'])
    
    command = "topaz extract" \
    + " -r " + radius \
    + " -m " + model_path \
    + " -o " + predicted_particles_file_path \
    + " " + processed_images

    start_time = time.time()
   
    launch_shell_script(command)

    end_time = time.time()
    duration = end_time - start_time
    g_log.loginfo("execute_extract", f"Function 'execute_extract' took {duration:.2f} seconds to complete")
    g_log.logperf(project_name, "execute_extract", "duration", f"{duration:.2f}", "seconds")

def execute_visualize_picks(params):

    files_path = params['file_paths']
    root_path = files_path['root_path']
    scripts_path = root_path + files_path['scripts_path']
    project_name = params['project_name'] 
    project_path = root_path + files_path['projects_path'] + project_name
    predicted_particles_file_path = project_path + files_path['predicted_particles_file_path']
    processed_particles_file_path = project_path + files_path['processed_particles_file_path']
    processed_images_path = project_path + files_path['processed_images_path']
    test_images = project_path + files_path['test_images']

    extract_parameters = params['extract_parameters']
    radius = str(extract_parameters['radius'])
    number_of_images_to_visualize = str(extract_parameters['number_of_images_to_visualize'])
    display_plots = extract_parameters['display_plots']
    score = str(extract_parameters['score'])
     
    command = "python3 " + scripts_path + "visualize_picks.py" \
    + " " + root_path \
    + " " + project_path \
    + " " + predicted_particles_file_path \
    + " " + processed_particles_file_path \
    + " " + processed_images_path \
    + " " + test_images \
    + " " + radius \
    + " " + number_of_images_to_visualize \
    + " " + display_plots \
    + " " + score

    start_time = time.time()

    launch_shell_script(command) 

    end_time = time.time()
    duration = end_time - start_time
    g_log.loginfo("execute_visualize_picks", f"Function 'execute_visualize_overlay' took {duration:.2f} seconds to complete")
    g_log.logperf(project_name, "execute_visualize_picks", "duration", f"{duration:.2f}", "seconds")
  
   
def main(config_file):

    global g_log 
    g_log = Logger("topaz_event.log", "topaz_perf.log", 1)

    
    if config_file == "" :
        g_log.loginfo("main", "config_file is missing")
        g_log.loginfo("main", "Usage: $ python topaz_run.py absolute_path_to_config_file")
        exit(1)
    
    params = read_json_file(config_file)

    if params == None:
        exit(1)

    files_paths = params['file_paths']
    root_path = files_paths['root_path']
    projects_path = files_paths['projects_path']
    project_name = params['project_name']
    directory_path = root_path + projects_path + project_name
    ensure_directory_exists(directory_path)
    ensure_directory_exists(directory_path + '/micrographs')
    
    # TODO - handle subprocess exceptions

    pipeline_steps = params['pipeline_steps']

    if pipeline_steps['run_preprocess'] == "true":
        execute_preprocess(params)

    if pipeline_steps['run_convert'] == "true":
        execute_convert(params)

    if pipeline_steps['run_split_test_train'] == "true":
        execute_train_test_split(params)

    if pipeline_steps['run_train'] == "true":
        execute_train(params)

    if pipeline_steps['run_extract'] == "true":
        execute_extract(params)

    if pipeline_steps['run_visualize_picks'] == "true":
        execute_visualize_picks(params)

    g_log.loginfo("topaz_run.py main", "All done...")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Process a string argument.")
    
    # Add an argument
    parser.add_argument("input_string", type=str, help="The input string to be processed.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Pass the input string (the configuration filenmame) to the main function
    main(args.input_string)

# topaz_run.py
#  - wrapper function around the topaz commands
#   preprocess - (downsample and normalize)
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
from scripts import parameters_factory as pf

def launch_shell_script(command):

    g_log.loginfo("launch_shell_script", command)    

    # Launch the command in a shell
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    std_output = stdout.decode()
    std_error = stderr.decode()

    if std_output != "":
        g_log.loginfo("shell output", "\n" + std_output)
    if std_error != "":
        g_log.loginfo("shell output", "\n" + std_error)

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
        os.makedirs(directory_path, exist_ok = True)
        g_log.loginfo("ensure_directory_exists", f"Directory '{directory_path}' created.")
    
def execute_preprocess(sys_params, user_params):
   
    downsampling = str(user_params.parameters.downsampling)
     
    rawdata_images = user_params.input.rawdata_images
    formatted_rawdata_images = rawdata_images.format(base_project_path = user_params.input.base_project_path,
                                                    session=user_params.experiment.session,  
                                                    slabPickRun=user_params.experiment.slabPickRun)
    
    sys_file_paths = sys_params['file_paths']
    processed_images_path = user_params.output.dir + sys_file_paths['processed_images_path']
    formatted_processed_images_path = processed_images_path.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    ensure_directory_exists(formatted_processed_images_path)

    # output_dir
    output_dir = user_params.output.dir
    formatted_output_dir = output_dir.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)

   
    command = "topaz preprocess" \
   + "  -v -s " + downsampling \
    + " -o " + formatted_processed_images_path \
    + " " + formatted_rawdata_images
    
    start_time = time.time()
    launch_shell_script(command)    
    end_time = time.time()
    duration = end_time - start_time

    g_log.loginfo("execute_preprocess", f"Function 'execute_preprocess' took {duration:.2f} seconds to complete")
    g_log.logperf(formatted_output_dir, "execute_preprocess", "duration", f"{duration:.2f}", "seconds")


def execute_convert(sys_params, user_params):

    downsampling = str(user_params.parameters.downsampling)
     
    rawdata_particles_path = user_params.input.rawdata_particles
    formatted_rawdata_particles_path = rawdata_particles_path.format(base_project_path = user_params.input.base_project_path, 
                                                        session=user_params.experiment.session,
                                                        slabPickRun=user_params.experiment.slabPickRun)

    processed_particles_path = user_params.output.dir 
    formatted_processed_particles_path = processed_particles_path.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    ensure_directory_exists(formatted_processed_particles_path)
    sys_file_paths = sys_params['file_paths']
    formatted_processed_particles_file_path = formatted_processed_particles_path + sys_file_paths['processed_particles']

    # output_dir
    output_dir = user_params.output.dir
    formatted_output_dir = output_dir.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
 
    command = "topaz convert" \
    + " -s " + downsampling \
    + " -o " + formatted_processed_particles_file_path \
    + " " + formatted_rawdata_particles_path
    
    start_time = time.time()     
    launch_shell_script(command)
    end_time = time.time()
    duration = end_time - start_time

    g_log.loginfo("execute_convert", f"Function 'execute_convert' took {duration:.2f} seconds to complete")
    g_log.logperf(formatted_output_dir, "execute_convert", "duration", f"{duration:.2f}", "seconds")

def execute_train_test_split(sys_params, user_params):

    
    number_of_held_out_test_images = str(user_params.parameters.number_of_held_out_test_images)
      
    sys_files_path = sys_params['file_paths']

    # processed_images_path
    processed_images_path = user_params.output.dir + sys_files_path['processed_images_path']
    formatted_processed_images_path = processed_images_path.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # processed_particles'
    processed_particles_path = user_params.output.dir + sys_files_path['processed_particles']
    formatted_processed_particles_path = processed_particles_path.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # output_dir
    output_dir = user_params.output.dir
    formatted_output_dir = output_dir.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)

    command = "topaz train_test_split" \
    + " -n " + number_of_held_out_test_images \
    + " --image-dir " + formatted_processed_images_path \
    + " " + formatted_processed_particles_path

    start_time = time.time()
    launch_shell_script(command)     
    end_time = time.time()
    duration = end_time - start_time

    g_log.loginfo("execute_train_test_split", f"Function 'execute_train_test_split' took {duration:.2f} seconds to complete")
    g_log.logperf(formatted_output_dir, "execute_train_test_split", "duration", f"{duration:.2f}", "seconds")

def execute_train(sys_params, user_params):
 
    radius = str(user_params.parameters.train_radius)
    number_of_predicted_particles= str(user_params.parameters.number_of_predicted_particles)
    number_workers= str(user_params.parameters.number_workers)

    sys_file_paths = sys_params['file_paths']
    sys_parameters = sys_params['parameters']
 
    # train_images
    train_images = user_params.output.dir + sys_file_paths['train_images']
    formatted_train_images = train_images.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # train_targets
    train_targets = user_params.output.dir + sys_file_paths['train_targets']
    formatted_train_targets = train_targets.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # test_images
    test_images = user_params.output.dir + sys_file_paths['test_images']
    formatted_test_images = test_images.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # test_targets
    test_targets = user_params.output.dir + sys_file_paths['test_targets']
    formatted_test_targets = test_targets.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
     # save_prefix
    # save_prefix = user_params.output.dir + sys_file_paths['save_prefix']
    save_prefix = user_params.output.model_file_save_path + sys_file_paths['save_prefix']
    formatted_save_prefix = save_prefix.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # model_file_path
    model_file_path = user_params.output.model_file_save_path + sys_file_paths['model_file_path']
    formatted_model_file_path= model_file_path.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # output_dir
    output_dir = user_params.output.dir
    formatted_output_dir = output_dir.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)

    # hack until I can figure out torch is not a module bug on mac
    if sys_parameters["system"] == "macos":
        command_str = "python3 " + user_params.input.base_program_path + "/topaz/topaz/commands/train.py" 
    else:
        command_str = "topaz train" 
        
    command = command_str \
    + " -n " + number_of_predicted_particles \
    + " -r " + radius \
    + " --num-workers=" + number_workers \
    + " --train-images " + formatted_train_images \
    + " --train-targets " + formatted_train_targets \
    + " --test-images " + formatted_test_images \
    + " --test-targets " + formatted_test_targets \
    + " --save-prefix " + formatted_save_prefix \
    + " -o " + formatted_model_file_path

    start_time = time.time()
    launch_shell_script(command)     
    end_time = time.time()
    duration = end_time - start_time

    g_log.loginfo("execute_train", f"Function 'execute_train' took {duration:.2f} seconds to complete")
    g_log.logperf(formatted_output_dir, "execute_train", "duration", f"{duration:.2f}", "seconds")


def execute_extract(sys_params, user_params):
   
    radius = str(user_params.parameters.extract_radius)

    sys_file_paths = sys_params['file_paths']
    
    # predicted_particles'
    predicted_particles = user_params.output.dir + sys_file_paths['predicted_particles']
    formatted_predicted_particles = predicted_particles.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # model
    model = user_params.output.model_file_save_path  + sys_file_paths['model']
    formatted_model = model.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # processed_images
    processed_images = user_params.output.dir + sys_file_paths['processed_images']
    formatted_processed_images = processed_images.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)   
    # output_dir
    output_dir = user_params.output.dir
    formatted_output_dir = output_dir.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    
    command = "topaz extract" \
    + " -r " + radius \
    + " -m " + formatted_model \
    + " -o " + formatted_predicted_particles \
    + " " + formatted_processed_images

    start_time = time.time()  
    launch_shell_script(command)
    end_time = time.time()
    duration = end_time - start_time

    g_log.loginfo("execute_extract", f"Function 'execute_extract' took {duration:.2f} seconds to complete")
    g_log.logperf(formatted_output_dir, "execute_extract", "duration", f"{duration:.2f}", "seconds")

def execute_visualize_picks(sys_params, user_params):

    sys_file_paths = sys_params['file_paths']

    radius = str(user_params.parameters.extract_radius)
    number_of_images_to_visualize = str(user_params.parameters.number_of_images_to_visualize)
    display_plots = user_params.parameters.display_plots
    score = str(user_params.parameters.score)

    base_program_path = user_params.input.base_program_path
    scripts_path = base_program_path + sys_file_paths['scripts_path']
    
    # output_dir
    output_dir = user_params.output.dir
    formatted_output_dir = output_dir.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # predicted_particles
    predicted_particles = user_params.output.dir + sys_file_paths['predicted_particles']
    formatted_predicted_particles = predicted_particles.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
 
    # processed_particles
    processed_particles = user_params.output.dir + sys_file_paths['processed_particles']
    formatted_processed_particles = processed_particles.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)

    # processed_images_path
    processed_images = user_params.output.dir + sys_file_paths['processed_images_path']
    formatted_processed_images = processed_images.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)
    # test_images
    test_images = user_params.output.dir + sys_file_paths['test_images']
    formatted_test_images = test_images.format(base_project_path = user_params.input.base_project_path,
                                                                    session=user_params.experiment.session,
                                                                    specimen=user_params.experiment.specimen,
                                                                    run=user_params.experiment.run)

    command = "python3 " + scripts_path + "visualize_picks.py" \
    + " " + base_program_path \
    + " " + formatted_output_dir \
    + " " + formatted_predicted_particles \
    + " " + formatted_processed_particles \
    + " " + formatted_processed_images \
    + " " + formatted_test_images \
    + " " + radius \
    + " " + number_of_images_to_visualize \
    + " " + display_plots \
    + " " + score

    start_time = time.time()
    launch_shell_script(command) 
    end_time = time.time()
    duration = end_time - start_time

    g_log.loginfo("execute_visualize_picks", f"Function 'execute_visualize_overlay' took {duration:.2f} seconds to complete")
    g_log.logperf(formatted_output_dir, "execute_visualize_picks", "duration", f"{duration:.2f}", "seconds")  
 
def main(config_file):

    global g_log 

    # TODO FIX THE HARDCODED PATH
    # sys_params = read_json_file('/Users/philsmoot/Repos/topaz_wrapper/scripts/sys_params.json')
    sys_params = read_json_file('sys_params.json')   
    if sys_params == None:
        g_log = Logger("topaz_event.log", "topaz_perf.log", 1)
        g_log.loginfo("main", "sys_file_paths.json is missing")
        exit(1)

    sys_params_parameters = sys_params["parameters"]
    g_log = Logger("topaz_event.log", "topaz_perf.log", sys_params_parameters["verbosity"])

    if config_file == "" :
        g_log.loginfo("main", "config_file is missing")
        g_log.loginfo("main", "Usage: $ python topaz_run.py absolute_path_to_config_file")
        exit(1)

    # TODO FIX THE HARDCODED PATH    
    # user_params = pf.read_topaz_parameters('/Users/philsmoot/Repos/topaz_wrapper/scripts/' + config_file)
    user_params = pf.read_topaz_parameters(config_file)
    if user_params == None:
        g_log.loginfo("main", "Error: Unable to read " + config_file)
        exit(1)

    # TODO - handle subprocess exceptions

    pipeline_steps = user_params.pipeline
 
    if pipeline_steps.run_preprocess == "yes":
        execute_preprocess(sys_params, user_params)
    
    if pipeline_steps.run_convert == "yes":
        execute_convert(sys_params, user_params)
    
    if pipeline_steps.run_split_test_train == "yes":
        execute_train_test_split(sys_params, user_params)
    
    if pipeline_steps.run_train == "yes":
        execute_train(sys_params, user_params)
    
    if pipeline_steps.run_extract == "yes":
        execute_extract(sys_params, user_params)
    
    if pipeline_steps.run_visualize_picks == "yes":
        execute_visualize_picks(sys_params, user_params)

    g_log.loginfo("topaz_run.py main", "All done... good bye")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Process a string argument.")
    
    # Add an argument for user config file
    parser.add_argument("input_string", type=str, help="The input string to be processed.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Pass the input string (the configuration filenmame) to the main function
    main(args.input_string)

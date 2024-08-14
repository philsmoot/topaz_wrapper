from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import json, click

@click.group()
@click.pass_context
def cli(ctx):
    pass

class ProcessingInput(BaseModel):
    session: str
    run: str
    slabPickRun: str
    boxSize: str
    rawdata_images: str,
    rawdata_particles: str        

class ProcessingOutput(BaseModel):
    model_file_save_path: str
    predicted_particles_file_path: str

class PipelineSteps(BaseModel):
    run_preprocess: str
    run_convert: str
    run_split_test_train: str
    run_train: str
    run_extract: str
    run_visualize_picks: str

class TopazParameters(BaseModel):
    downsampling: int
    number_of_held_out_test_images: int
    number_of_predicted_particles: int
    number_workers: int
    train_radius: int    
    extract_radius: int
    number_of_images_to_visualize: int
    display_plots: str
    score: int  
    input: ProcessingInput
    output: ProcessingOutput     

class ProcessingConfig(BaseModel):
    input: ProcessingInput
    output: ProcessingOutput
    pipeline: PipelineSteps
    parameters: TopazParameters

def create_boilerplate_json(file_path: str = 'example_parameter.json',
                            box_size: int = 64):
    default_config = ProcessingConfig( 
        input = ProcessingInput(
            session="24jun10a",
            run="run001",
            slabPickRun="run001"
            boxSize = box_size
        )
        output=ProcessingOutput(
            dir="{baseProjectPath}/topaz/{session}/specimen/{run}"
        )
        pipeline=PipelineSteps(
            run_preprocess="yes"
            run_convert: "yes"
            run_split_test_train: "no"
            run_train: "yes"
            run_extract: "yes"
            run_visualize_picks: "yes"
        )
        parameters=TopazParameters(
            downsampling: 1
            number_of_held_out_test_images: 30 
            number_of_predicted_particles: 240 
            number_workers: 1
            train_radius: 3
            extract_radius: 14
            number_of_images_to_visualize: 2
            display_plots: true
            score: 0
        )

def read_topaz_parameters(json_path):

    # Read file
    with open(json_path, "r") as f:
        data = json.load(f)
        config = ProcessingConfig(**data)
    return config    

# Create the boilerplate JSON file with a default file path
@click.command(context_settings={"show_default": True})
@click.option(
    "--file-path",
    type=str,
    required=False,
    default='example_parameter.json',
    help="The Name for the Saved Parameter File",
)
def create_parameter_file(
    ctx, 
    file_path: str
    ):

    create_boilerplate_json(file_path)

if __name__ == "__main__":
    cli()    
# Topaz Wrapper Environment Setup

# clone the topaz wrapper source code in a working directory

$ git clone https://github.com/philsmoot/topaz_wrapper.git

# create and activate the topaz conda enivronment

$ cd topaz_wrapper

$ ml anaconda/latest

$ conda create --prefix=/{working_directory_path}/topaz_wrapper/pytopaz 

$ conda activate /{working_directory_path}/topaz_wrapper/pytopaz

# numpy has to be < 2.0 in order to prevent int overflow bug in training.  1.24.3, 1.24.4 and 1.26.4 have worked
# do this first so conda solving environment doesn't take forever later

$ pip install numpy==1.24.4 

# for Bruno and 3400 enviroments install cuda dependencies
$ conda install pytorch torchvision torchaudio pytorch-cuda=12.1 cupy cudnn cutensor nccl -c conda-forge -c pytorch -c nvidia

# clone the topaz source code

$ git clone https://github.com/tbepler/topaz

# install topaz

$ cd topaz

$ pip install .

# for visualizations, install matplotlib

$ conda install matplotlib

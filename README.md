# Topaz Wrapper Enviroment Setup

# clone the topaz wrapper source code in a working directory

$ git clone https://github.com/philsmoot/topaz_wrapper.git

# create and activate the topaz conda enviroment

$ cd topaz_wrapper

$ ml anaconda/latest

$ conda create --prefix=/{working_directory_path}/topaz_wrapper/pytopaz 

$ conda activate /{working_directory_path}/topaz_wrapper/pytopaz

# for Bruno and 3400 enviroments install cuda dependencies

# for Bruno (pytorch 2.3.1 py3.8cpu_0 pytorch;  pytorch-mutex 1.0 cpu pytorch)
$ conda install pytorch torchvision
# for 3400...
$ conda install pytorch torchvision torchaudio pytorch-cuda=12.1 cupy cudnn cutensor nccl -c conda-forge -c pytorch -c nvidia

# clone the topaz source code

$ git clone https://github.com/tbepler/topaz

# install topaz

$ cd topaz

$ pip install .

# roll back numpy to be less then version 2.0 for an overflow bug

$ pip install numpy==1.26.4

# install matplotlib for graphic output

$ conda install matplotlib


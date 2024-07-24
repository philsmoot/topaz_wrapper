# Topaz Wrapper Environment Setup

# clone the topaz wrapper source code in a working directory

$ git clone https://github.com/philsmoot/topaz_wrapper.git

# create and activate the topaz conda enivronment

$ cd topaz_wrapper

$ ml anaconda/latest

$ conda create --prefix=/{working_directory_path}/topaz_wrapper/pytopaz -c pytorch torchvision python=3.8

$ conda activate /{working_directory_path}/topaz_wrapper/pytopaz

# clone the topaz source code

$ git clone https://github.com/tbepler/topaz

# install topaz

$ cd topaz

$ pip install .

# for visualizations, install matplotlib

$ conda install matplotlib

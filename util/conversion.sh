#!/bin/bash

### DATA FROM TOUVRONETAL2019
wget https://dl.fbaipublicfiles.com/FixRes_data/contest/Herbarium_data/herbarium_fixresnet50.pth
wget https://dl.fbaipublicfiles.com/FixRes_data/contest/Herbarium_data/herbarium_fixsenet154.pth

### INSTALL PYTORCH2KERAS ON UBUNTU 19.10
sudo apt install python3-pip python3-venv
python3 -m venv pytorch2keras
source pytorch2keras/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
python3 -m pip install wheel
python3 -m pip install pytorch2keras
python3 -m pip install torchsummary
deactivate

### INSTALL TENSORFLOWJS
python3 -m venv tensorflowjs
source tensorflowjs/bin/activate
python3 -m pip install tensorflowjs
deactivate

### CONVERT TOUVRONETAL2019 RESNET50
#
### modify lib/python3.7/site-packages/onnx2keras/pooling_layers.py to eliminate lambda layers in convert_global_avg_pool
### pytorch2keras/lib/python3.7/site-packages/onnx2keras/linear_layers.py to add softmax activation to dense layers
#
source pytorch2keras/bin/activate
./pth2keras.py -i herbarium_fixresnet50.pth -o herbarium_fixresnet50
deactivate
./predict.py -i 00007.jpg -n herbarium_fixresnet50
source tensorflowjs/bin/activate
tensorflowjs_converter --quantization_bytes 1 --input_format keras herbarium_fixresnet50.hdf5 herbarium_fixresnet50/ ### 24 MB
deactivate

#!/usr/bin/env python3

### IMPORT
from pytorch2keras.converter import pytorch_to_keras
from torch.autograd import Variable
from torchsummary import summary
import getopt
import numpy as np
import os
import sys
import torch
import torch.nn as nn
import torchvision
import torchvision.models as models

### SET DEFAULT
def eprint(*args, **kwargs):
	print(*args, file = sys.stderr, **kwargs)
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")
i = ''
o = ''

### PARSE ARGUMENTS
try:
	arguments, values = getopt.getopt(sys.argv[1:], 'hi:o:', ['input=', 'output='])
except getopt.error as err:
	eprint(str(err))
	sys.exit(2)
for argument, value in arguments:
	if argument in ('-h', '--help'):
		eprint('A Python3 script to convert PyTorch resnet50 (pth) to Keras (hdf5) files.')
		eprint('input: -i file | --input=file')
		eprint('output: -o file | --output=file')
		sys.exit(0)
	elif argument in ('-i', '--input'):
		if os.path.isfile(value) == True:
			i = value
		else:
			eprint('input file does not exist (%s)' % (value))
			sys.exit(2)
	elif argument in ('-o', '--output'):
		if os.path.isfile(value) == False:
			o = value
		else:
			eprint('output file exist (%s)' % (value))
			sys.exit(2)

### START/END
if not i:
	eprint('input: -i file | --input=file')
	sys.exit(2)
elif not o:
	eprint('output: -o file | --output=file')
	sys.exit(2)
else:
	eprint('started')
	eprint('input = %s' % (i))
	eprint('output = %s' % (o))

### INPUT
model = models.resnet50(pretrained = False)
model.fc = nn.Linear(2048, 683)
pretrained = torch.load(i)['model']
modelDictionary = model.state_dict()
for k in modelDictionary.keys():
	if(('module.'+k) in pretrained.keys()):
		modelDictionary[k] = pretrained.get(('module.'+k))
model.load_state_dict(modelDictionary)
for name, child in model.named_children():
	for name2, params in child.named_parameters():
		params.requires_grad = False
summary(model, (3, 224, 224), device = 'cpu')

### CONVERT TO KERAS JSON (TO AVOID PYTHON 3.7.5 VS 3.6.9 OPTCODE CONFLICTS... WTF)
input_np = np.random.uniform(0, 1, (1, 3, 224, 224))
input_var = Variable(torch.FloatTensor(input_np))
kmodel = pytorch_to_keras(model, input_var, (3, 224, 224,), verbose = False)
kmodel.summary()
kmodel.save(o + '.hdf5')
kmodelJSON = kmodel.to_json()
with open(o + '.json', 'w') as JSON:
	JSON.write(kmodelJSON)
kmodel.save_weights(o + '-weights.hdf5')

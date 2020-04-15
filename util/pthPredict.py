#!/usr/bin/env python3

### IMPORT
from PIL import Image
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
import torchvision.transforms.functional as F
from torchvision import transforms

### SET DEFAULT
def eprint(*args, **kwargs):
	print(*args, file = sys.stderr, **kwargs)
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")
d = False
i = ''
n = ''

### PARSE ARGUMENTS
try:
	arguments, values = getopt.getopt(sys.argv[1:], 'dhi:n:', ['debug', 'help', 'image=', 'network='])
except getopt.error as err:
	eprint(str(err))
	sys.exit(2)
for argument, value in arguments:
	if argument in ('-d', '--debug'):
		d = True
	elif argument in ('-h', '--help'):
		eprint('A Python3 script to predict from an image using a PyTorch neural network.')
		eprint('input: -i file | --image=file')
		eprint('debug messages: -d | --dubug')
		eprint('network: -n file | --network=file')
		sys.exit(0)
	elif argument in ('-i', '--image'):
		if os.path.isfile(value) == True:
			i = value
		else:
			eprint('image file does not exist (%s)' % (value))
			sys.exit(2)
	elif argument in ('-n', '--network'):
		if os.path.isfile(value) == True:
			n = value
		else:
			eprint('network file does not exist (%s)' % (value))
			sys.exit(2)

### START/END
if not i:
	eprint('input: -i file | --image=file')
	sys.exit(2)
elif not n:
	eprint('output: -n file | --network=file')
	sys.exit(2)
else:
	eprint('started')
	eprint('image = %s' % (i))
	eprint('network = %s' % (n))

### NETWORK
model = models.resnet50(pretrained = False)
model.fc = nn.Linear(2048, 683)
pretrained = torch.load(n)['model']
modelDictionary = model.state_dict()
for k in modelDictionary.keys():
	if(('module.'+k) in pretrained.keys()):
		modelDictionary[k] = pretrained.get(('module.'+k))
model.load_state_dict(modelDictionary)
for name, child in model.named_children():
	for name2, params in child.named_parameters():
		params.requires_grad = False
summary(model, (3, 224, 224), device = 'cpu')

### PREDICT
p = Image.open(i)
transformer = transforms.Compose([
	transforms.Resize(tuple([int(x*float(224)/max(p.size)) for x in p.size])),
	transforms.ToTensor(),
	transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
p = transformer(p)
p = Variable(p, requires_grad = True)
p = p.unsqueeze(0)
print(torch.nn.functional.softmax(model(p)))

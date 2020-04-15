#!/usr/bin/env python3

### IMPORTS
import getopt
import multiprocessing
import numpy as np
import os
import random
import sys
import tensorflow as tf

### SET OPTIONS
def eprint(*args, **kwargs):
	print(*args, file = sys.stderr, **kwargs)
settings = {}
settings['batch'] = 64
settings['cores'] = multiprocessing.cpu_count()
settings['dimension'] = 224
settings['dimensions3'] = 3*settings['dimension']*settings['dimension']
settings['gpu'] = True
settings['epochSteps'] = 16
settings['inputDirectory'] = ''
settings['network'] = ''
settings['outputDirectory'] = ''
settings['validationDirectory'] = ''

### READ OPTIONS
inputDirectoryError = 'input directory of tfr files required (' + str(settings['batch']) + ' records per file; must have at least ' + str(settings['epochSteps']) + ' files; class,data,...): -i directory | --input=directory'
networkError = 'network required; -n file | --network=file'
outputDirectoryError = 'output directory required: -o directory | --output=directory'
validationDirectoryError = 'validation directory of tfr files required (' + str(settings['batch']) + ' records per file; must have at least ' + str(settings['epochSteps']) + ' files; class,data,...): -v directory | --validation=directory'
try:
	arguments, values = getopt.getopt(sys.argv[1:], 'c:ghi:n:o:v:', ['cores=', 'gpu', 'help', 'input=', 'network=', 'output=', 'validation='])
except getopt.error as err:
	eprint(str(err))
	sys.exit(2)
for argument, value in arguments:
	if argument in ('-c', '--cores'):
		if int(value) > 0:
			settings['cores'] = int(value)
	elif argument in ('-g', '--gpu'):
		settings['gpu'] = False
	elif argument in ('-h', '--help'):
		eprint('A Python3 script to train a neural network using TensorFlow v2.1.0.')
		eprint('cores optional: -c int | --cores=int (default = %i)' % (settings['cores']))
		eprint('ignore gpu optional: -g | --gpu (default = %s)' % (not settings['gpu']))
		eprint(inputDirectoryError)
		eprint(networkError)
		eprint(outputDirectoryError)
		eprint(validationDirectoryError)
		sys.exit(0)
	elif argument in ('-i', '--input'):
		if os.path.isdir(value):
			settings['inputDirectory'] = value
		else:
			eprint('input directory does not exist (%s)' % (value))
			sys.exit(2)
	elif argument in ('-n', '--network'):
		if os.path.isfile(value) == True:
			settings['network'] = value
		else:
			eprint('network file does not exist (%s)' % (value))
			sys.exit(2)
	elif argument in ('-o', '--output'):
		if os.path.isdir(value):
			settings['outputDirectory'] = value
		else:
			eprint('output directory does not exist (%s)' % (value))
			sys.exit(2)
	elif argument in ('-v', '--validation'):
		if os.path.isdir(value):
			settings['validationDirectory'] = value
		else:
			eprint('validation directory does not exist (%s)' % (value))
			sys.exit(2)

### START/END
if not settings['inputDirectory']:
	eprint(inputDirectoryError)
	sys.exit(2)
elif not settings['network']:
	eprint(networkError)
	sys.exit(2)
elif not settings['outputDirectory']:
	eprint(outputDirectoryError)
	sys.exit(2)
elif not settings['validationDirectory']:
	eprint(validationDirectoryError)
	sys.exit(2)
else:
	eprint('started')
	eprint('cores = %i' %(settings['cores']))
	eprint('gpu = %s' % (not settings['gpu']))
	eprint('input = %s' % (settings['inputDirectory']))
	eprint('network = %s' % (settings['network']))
	eprint('output = %s' % (settings['outputDirectory']))
	eprint('validation = %s' % (settings['validationDirectory']))

### TF GPU
if settings['gpu'] == True:
	gpus = tf.config.experimental.list_physical_devices('GPU')
	if gpus:
		try:
			for gpu in gpus:
				tf.config.experimental.set_memory_growth(gpu, True)
			logical_gpus = tf.config.experimental.list_logical_devices('GPU')
			eprint('physical GPUs = %i; logical GPUs = %i' % (len(gpus), len(logical_gpus)))
		except RuntimeError as e:
			eprint(e)
else:
	os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
	eprint('CPU only, any GPUs will be ignored')

### TF RECORD PARSER
def parser(tfr):
	r = tf.io.parse_single_example(tfr, features = {
		'label': tf.io.FixedLenFeature([1], tf.int64, default_value = [0]),
		'features': tf.io.FixedLenFeature([settings['dimensions3']], tf.float32, default_value = [0]*settings['dimensions3'])
	})
#
# fix to use a lookup
#
	w = 1
	if r['label'] == 1:
				w = 16
	return r['features'], r['label'], w

### TF DATASETS
tainingDataset = (
	tf.data.TFRecordDataset(trainingFile).apply(
		tf.data.experimental.map_and_batch(
				map_func = parser,
				batch_size = settings['batch'],
				num_parallel_batches = settings['cores']
		)
	).prefetch(batch)
)
validationDataset = (
	tf.data.TFRecordDataset(validationFile).apply(
		tf.data.experimental.map_and_batch(
				map_func = parser,
				batch_size = settings['batch'],
				num_parallel_batches = settings['cores']
		)
	).prefetch(batch)
)

### NEURAL NETWORK
model = tf.keras.models.load_model(settings['network'])
model.summary()

### TRAIN NEURAL NETWORK
model.fit_generator(
	callbacks = [
		tf.keras.callbacks.ModelCheckpoint(os.path.join(settings['outputDirectory'], 'training-e{epoch:04d}-l{loss:.4f}-a{sparse_categorical_accuracy:.4f}.tfm'), verbose = 1)
	],
#	class_weight = {0: 0.0625, 1: 1.0},
	epochs = 512,
	generator = trainingGenerator,
	steps_per_epoch = settings['epochSteps'],
	use_multiprocessing = True,
	validation_data = testingGenerator,
	validation_steps = 1,
	verbose = 1,
	workers = settings['cores']
)
model.save(os.path.join(settings['outputDirectory'], 'final.tfm'))

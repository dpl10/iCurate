#!/usr/bin/env python3

### IMPORT
import getopt
import numpy as np
# import matplotlib.pyplot as plt
import os
import sys
import tensorflow as tf
from tensorflow import keras

### SET DEFAULT
def eprint(*args, **kwargs):
	print(*args, file = sys.stderr, **kwargs)
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")
d = False
i = ''
n = ''

### TF GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
	try:
		for gpu in gpus:
			tf.config.experimental.set_memory_growth(gpu, True)
		logical_gpus = tf.config.experimental.list_logical_devices('GPU')
		eprint('physical GPUs = %i; logical GPUs = %i' % (len(gpus), len(logical_gpus)))
	except RuntimeError as e:
		eprint(e)

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
		eprint('A Python3 script to predict from an image using a Keras neural network.')
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
		if os.path.isfile(value + '.json') == True and os.path.isfile(value + '-weights.hdf5') == True:
			n = value
		else:
			eprint('network files do not exist (%s)' % (value))
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
json = open(n + '.json', 'r')
model = keras.models.model_from_json(json.read())
json.close()
model.load_weights(n + '-weights.hdf5')
model.summary()

### IMAGE
f = tf.io.read_file(
	i
)
p = tf.io.decode_jpeg(
	f,
	channels = 3,
	ratio = 1,
	fancy_upscaling = True,
	try_recover_truncated = False,
	acceptable_fraction = 1,
	dct_method = ''
)
if d == True:
	eprint('\n\n\nstarting:')
	eprint('raw image min = %i; max = %i' % (tf.math.reduce_min(p), tf.math.reduce_max(p)))
	# plt.figure(
	# 	num = 'raw',
	# 	figsize = [10.24, 10.24],
	# 	dpi = 100
	# 	)
	# plt.imshow(p.numpy())
	# plt.show()

c = tf.image.convert_image_dtype(
	p,
	dtype = tf.float32,
	saturate = False
)
if d == True:
	eprint('converted to float: min = %f; max = %f' % (tf.math.reduce_min(c), tf.math.reduce_max(c)))
	# plt.figure(
	# 	num = 'converted to float',
	# 	figsize = [10.24, 10.24],
	# 	dpi = 100
	# 	)
	# plt.imshow(np.multiply(c.numpy(), 255))
	# plt.show()

r = tf.image.resize_with_pad(
	c,
	224,
	224,
	method = tf.image.ResizeMethod.BILINEAR,
	antialias = True
)
if d == True:
	eprint('resized: min = %f; max = %f' % (tf.math.reduce_min(r), tf.math.reduce_max(r)))
	# plt.figure(
	# 	num = 'resized',
	# 	figsize = [3.39, 3.39],
	# 	dpi = 72
	# )
	# plt.imshow(r.numpy())
	# plt.show()

t = tf.transpose(
	r,
	perm = [2, 0, 1]
)
e = tf.expand_dims(
	t,
	axis = 0
)

### PREDICT
prediction = model.predict(e)
print(prediction)

### SAVE
model.save( n + '.hdf5')


# ./predict.py -i 00000.jpg -n herbarium_fixresnet50.hdf5 -d
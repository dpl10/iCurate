#!/usr/bin/env python3

### IMPORT
import getopt
import numpy as np
import os
import sys
import random
import tensorflow as tf

### SET DEFAULT
def eprint(*args, **kwargs):
	print(*args, file = sys.stderr, **kwargs)
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")
c = False
d = False
i = ''
o = ''

### PARSE ARGUMENTS
try:
	arguments, values = getopt.getopt(sys.argv[1:], 'cdhi:o:', ['cpu', 'debug', 'help', 'images=', 'output='])
except getopt.error as err:
	eprint(str(err))
	sys.exit(2)
for argument, value in arguments:
	if argument in ('-c', '--cpu'):
		c = True
	if argument in ('-d', '--debug'):
		d = True
		import matplotlib.pyplot as plt
	elif argument in ('-h', '--help'):
		eprint('A Python3 script to create tfrecords from images with TensorFlow 2.1.0.')
		eprint('cpu: -c | --cpu')
		eprint('debug messages: -d | --dubug')
		eprint('input: -i directory | --images=directory')
		eprint('output: -o: directory | --output=directory')
		sys.exit(0)
	elif argument in ('-i', '--images'):
		if os.path.isdir(value) == True:
			i = value
		else:
			eprint('image directory does not exist (%s)' % (value))
			sys.exit(2)
	elif argument in ('-o', '--output'):
		if os.path.isdir(value) == True:
			o = value
		else:
			eprint('output directory does not exist (%s)' % (value))
			sys.exit(2)

### START/END
if not i:
	eprint('input: -i directory | --images=directory')
	sys.exit(2)
elif not o:
	eprint('output: -o: directory | --output=directory')
	sys.exit(2)
else:
	eprint('started')
	eprint('cpu = %s' % (c))
	eprint('debug = %s' % (d))
	eprint('images = %s' % (i))
	eprint('output = %s' % (o))

### TF GPU
if c == True:
	os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
	eprint('CPU only, any GPUs will be ignored')
else:
	gpus = tf.config.experimental.list_physical_devices('GPU')
	if gpus:
		try:
			for gpu in gpus:
				tf.config.experimental.set_memory_growth(gpu, True)
			logical_gpus = tf.config.experimental.list_logical_devices('GPU')
			eprint('physical GPUs = %i; logical GPUs = %i' % (len(gpus), len(logical_gpus)))
		except RuntimeError as e:
			eprint(e)

### IMAGES
inputFiles = []
for r, x, f in os.walk(i):
	for j in f:
		if '.jpg' in j or '.jpeg' in j:
			inputFiles.append(os.path.join(r, j))
random.seed(os.urandom(64))
random.shuffle(inputFiles)
if d == True:
	eprint('input files:')
	eprint(inputFiles)
O = tf.io.TFRecordOptions(
	compression_type = 'ZLIB' ### '' = 1.2M; GZIP = 584K (1.349s); ZLIB = 585K (1.296s)
)
n = 0
t = 0
w = tf.io.TFRecordWriter(os.path.join(o, '%0*d.tfr' % (4, t)), O)
eprint('started tf record file %0*d' % (4, t))
for f in inputFiles:
	r = random.randint(1, 10000)
	if d == True:
		eprint('random number: %i' % (r))
	if r > 3679: ### jackknife removal
		j = tf.io.read_file(
			f
		)
		x = tf.io.decode_jpeg(
			j,
			channels = 3,
			ratio = 1,
			fancy_upscaling = True,
			try_recover_truncated = False,
			acceptable_fraction = 1,
			dct_method = ''
		)
		x = tf.image.convert_image_dtype(
			x,
			dtype = tf.float32,
			saturate = False
		)
		if d == True:
			eprint('raw image %s: min = %i; max = %i' % (f, tf.math.reduce_min(x), tf.math.reduce_max(x)))
			plt.figure(
				num = 'raw',
				figsize = [10.24, 10.24],
				dpi = 100
				)
#			plt.imshow(x.numpy())
#			plt.show()
		x = tf.image.resize_with_pad(
			x,
			256,
			256,
			method = tf.image.ResizeMethod.BILINEAR,
			antialias = True
		)
		x = tf.image.random_flip_left_right(x)
		x = tf.image.random_flip_up_down(x)
		x = tf.image.rot90(
			x,
			k = random.randint(1, 4)
		)
#
# add 10% zoom
#
		if r <= 5786:
			if d == True:
				eprint('random rectangle erased')
			y0 = random.randint(0, 225)
			y1 = random.randint(y0, 255)
			x0 = random.randint(0, 225)
			x1 = random.randint(x0, 255)
			# m = tf.concat(
			# 	[
			# 		tf.zeros([256, y0]),
			# 		tf.concat(
			# 			[
			# 				tf.zeros([x0, y1-y0]),
			# 				tf.ones([x1-x0, y1-y0]),
			# 				tf.zeros([256-x1, y1-y0])
			# 			],
			# 		axis = 0),
			# 		tf.zeros([256, 256-y1])
			# 	],
			# 	axis = 1)
			# m = tf.stack(
			# 	[m, m, m],
			# 	axis = 2
			# )
			# x = tf.boolean_mask(x, m)
			# x = tf.reshape(
			# 	x,
			# 	[256, 256, 3]
			# )
			# x = tf.image.convert_image_dtype(
			# 	x,
			# 	dtype = tf.float32,
			# 	saturate = False
			# )
		elif r > 5786 and r <= 7893:
			if d == True:
				eprint('random color shift')
			x = tf.image.random_hue(x, 0.08)
			x = tf.image.random_saturation(x, 0.6, 1.6)
			x = tf.image.random_brightness(x, 0.05)
			x = tf.image.random_contrast(x, 0.7, 1.3)
		x = tf.image.crop_to_bounding_box(
			x,
			random.randint(0, 31),
			random.randint(0, 31),
			224,
			224
		)
		if d == True:
			eprint('final: min = %f; max = %f' % (tf.math.reduce_min(x), tf.math.reduce_max(x)))
			plt.figure(
				num = 'final',
				figsize = [3.11, 3.11],
				dpi = 72
			)
#			plt.imshow(x.numpy())
#			plt.show()
		x = tf.transpose(
			x,
			perm = [2, 0, 1]
		)
		F = f.split('/')
		if d == True:
			eprint('file %s' % (F[len(F)-2]))
		n += 1
		if n > 63:
			n = 0
			w.flush()
			w.close()
			w = tf.io.TFRecordWriter(os.path.join(o, '%0*d.tfr' % (4, t)), O)
			eprint('started tf record file %0*d' % (4, t))
			t += 1
		w.write(tf.train.Example(features = tf.train.Features(feature = {
			'image': tf.train.Feature(float_list = tf.train.FloatList(value = x.numpy().flatten())),
			'label': tf.train.Feature(int64_list = tf.train.Int64List(value = [int(len(F)-2)]))
		})).SerializeToString())
w.flush()
w.close()





		# x = tf.expand_dims(
		# 	x,
		# 	axis = 0
		# )

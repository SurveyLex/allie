'''
Import all the featurization scripts and allow the user to customize what embedding that
they would like to use for modeling purposes.

AudioSet is the only embedding that is a little bit wierd, as it is normalized to the length
of each audio file. There are many ways around this issue (such as normalizing to the length 
of each second), however, I included all the original embeddings here in case the time series
information is useful to you.
'''

################################################
##              IMPORT STATEMENTS             ##
################################################
import json, os, sys, time, random
import numpy as np 
# import helpers.transcribe as ts
# import speech_recognition as sr
from tqdm import tqdm

def prev_dir(directory):
	g=directory.split('/')
	dir_=''
	for i in range(len(g)):
		if i != len(g)-1:
			if i==0:
				dir_=dir_+g[i]
			else:
				dir_=dir_+'/'+g[i]
	# print(dir_)
	return dir_

################################################
##              Helper functions              ##
################################################

def csv_augment(augmentation_set, csvfile, basedir):

	# only load the relevant featuresets for featurization to save memory
	if augmentation_set=='augment_tgan':
		augment_tgan.augment_tgan(csvfile, basedir)
	elif augmentation_set=='augment_ctgan_classification':
		augment_ctgan_classification.augment_ctgan_classification(csvfile)
	elif augmentation_set=='augment_ctgan_regression':
		augment_ctgan_regression.augment_ctgan_regression(csvfile)
		
################################################
##              Load main settings            ##
################################################

# directory=sys.argv[1]
basedir=os.getcwd()
settingsdir=prev_dir(basedir)
settingsdir=prev_dir(settingsdir)
settings=json.load(open(settingsdir+'/settings.json'))
os.chdir(basedir)

csv_transcribe=settings['transcribe_csv']
default_csv_transcribers=settings['default_csv_transcriber']
try:
	# assume 1 type of feature_set 
	augmentation_sets=[sys.argv[2]]
except:
	# if none provided in command line, then load deafult features 
	augmentation_sets=settings['default_csv_augmenters']

################################################
##          Import According to settings      ##
################################################

# only load the relevant featuresets for featurization to save memory
if 'augment_tgan' in augmentation_sets:
	import augment_tgan
elif 'augment_ctgan_classification' in augmentation_sets:
	import augment_ctgan_classification
elif 'augment_ctgan_regression' in augmentation_sets:
	import augment_ctgan_regression

################################################
##          Get featurization folder          ##
################################################

foldername=sys.argv[1]
os.chdir(foldername)
listdir=os.listdir() 
random.shuffle(listdir)
cur_dir=os.getcwd()
help_dir=basedir+'/helpers/'

# get class label from folder name 
labelname=foldername.split('/')
if labelname[-1]=='':
	labelname=labelname[-2]
else:
	labelname=labelname[-1]

################################################
##                NOW AUGMENT!!               ##
################################################

listdir=os.listdir()
random.shuffle(listdir)

# featurize all files accoridng to librosa featurize
for i in tqdm(range(len(listdir)), desc=labelname):
	if listdir[i][-4:] in ['.csv']:
		for j in range(len(augmentation_sets)):
			augmentation_set=augmentation_sets[j]
			csv_augment(augmentation_set, listdir[i], basedir)
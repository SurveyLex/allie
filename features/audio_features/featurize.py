'''
Import all the featurization scripts and allow the user to customize what embedding that
they would like to use for modeling purposes.

AudioSet is the only embedding that is a little bit wierd, as it is normalized to the length
of each audio file. There are many ways around this issue (such as normalizing to the length 
of each second), however, I included all the original embeddings here in case the time series
information is useful to you.
'''

import json, os, sys

################################################
##	    	Import According to settings      ##
################################################

import librosa_features as lf 
import standard_features as sf 
import audioset_features as af 
import sox_features as soxf 
import pyaudio_features as pf 
import sa_features as saf
import spectrogram_features as specf
import meta_features as mf 
import praat_features as prf
import pspeech_features as psf
import specimage_features as sif
import specimage2_features as sif2
import myprosody_features as mpf
import helpers.transcribe as ts

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
	
# import to get image feature script 
directory=os.getcwd()
prevdir=prev_dir(directory)
sys.path.append(prevdir+'/image_features')
haar_dir=prevdir+'image_features/helpers/haarcascades'
import image_features as imf
sys.path.append(prevdir+'/text_features')
import nltk_features as nf 
os.chdir(directory)

################################################
##	    		Helper functions      		  ##
################################################

def transcribe(file, default_audio_transcriber):
	# get transcript 
	if file[-4:]=='.wav':
		transcript=ts.transcribe_sphinx(file)
	elif file[-4] == '.mp3':
		os.system('ffmpeg -i %s %s'%(file, file[0:-4]+'.wav'))
		transcript=ts.transcribe_sphinx(file)
		os.remove(file[-4:]+'.wav')
	else:
		transcript=file

	# 3 types of transcripts = audio, text, and image 
	transcript_dict={'transcript': transcript,
					'transcript_type': 'audio',
					'audio_transcriber': default_audio_transcriber}

	return transcript_dict, transcript 

def audio_featurize(feature_set, audiofile, transcript):

	# long conditional on all the types of features that can happen and featurizes accordingly.
	if feature_set == 'librosa_features':
		features, labels = lf.librosa_featurize(audiofile, False)
	elif feature_set == 'standard_features':
		features, labels = sf.standard_featurize(audiofile)
	elif feature_set == 'audioset_features':
		features, labels = af.audioset_featurize(audiofile, basedir, foldername)
	elif feature_set == 'sox_features':
		features, labels = soxf.sox_featurize(audiofile)
	elif feature_set == 'sa_features':
		features, labels = saf.sa_featurize(audiofile)
	elif feature_set == 'pyaudio_features':
		features, labels = pf.pyaudio_featurize(audiofile, basedir)
	elif feature_set == 'spectrogram_features':
		features, labels= specf.spectrogram_featurize(audiofile)
	elif feature_set == 'meta_features':
		features, labels = mf.meta_featurize(audiofile, cur_dir, help_dir)
	elif feature_set == 'praat_features':
		features, labels = prf.praat_featurize(audiofile)
	elif feature_set == 'pspeech_features':
		features, labels = psf.pspeech_featurize(audiofile)
	elif feature_set == 'specimage_features':
		features, labels = sif.specimage_featurize(audiofile,cur_dir, haar_dir)
	elif feature_set == 'specimage2_features':
		features, labels = sif2.specimage2_featurize(audiofile,cur_dir, haar_dir)
	elif feature_set == 'myprosody_features':
		features, labels = mpf.myprosody_featurize(audiofile)
	elif feature_set == 'nltk_features':
		features, labels = nf.nltk_featurize(transcript)

	return features, labels 

def make_features(sampletype):

	# only add labels when we have actual labels.
	features={'audio':dict(),
			  'text': dict(),
			  'image':dict(),
			  'video':dict(),
			  'csv': dict(),
			  }

	data={'sampletype': sampletype,
		  'transcripts': [],
		  'features': features,
		  'labels': []}

	return data


################################################
##	    		Load main settings    		  ##
################################################

# directory=sys.argv[1]
basedir=os.getcwd()
settingsdir=prev_dir(basedir)
settingsdir=prev_dir(settingsdir)
settings=json.load(open(settingsdir+'/settings.json'))
os.chdir(basedir)

audio_transcribe=settings['transcribe_audio']
default_audio_transcriber=settings['default_audio_transcriber']
feature_set=settings['default_audio_features']

################################################
##	   		Get featurization folder     	  ##
################################################

foldername=input('what is the name of the folder?')
os.chdir(foldername)
listdir=os.listdir() 
cur_dir=os.getcwd()
help_dir=basedir+'/helpers/'

################################################
##	    	Load feature set                  ##
################################################

# if set to 'all', then featurizes all audio features...

# feature_set='librosa_features'
# feature_set='standard_features'
# feature_set='audioset_features'
# feature_set='sox_features'
# feature_set='sa_features'
# feature_set='pyaudio_features'
# feature_set='spectrogram_features'
# feature_set = 'meta_features'
# feature_set='praat_features'
# feature_set='pspeech_features'
# feature_set='specimage_features'
# feature_set='specimage2_features'
# feature_set='myprosody_features'
# feature_set = 'nltk_features'

# all_ features ..
# feature_set=['librosa_features', 'standard_features', 'audioset_features', 'sox_features',
		# 	  'sa_features', 'pyaudio_features', 'spectrogram_features', 'meta_features',
		# 	  'praat_features', 'pspeech_features', 'specimage_features', 'specimage2_features',
		# 	  'myprosody_features', 'nltk_features']

# for i in range(len(feature_set)):
# 	audio_featurize(all_[i], audiofile, transcript)

## can also do custom multi-featurizations
# feature_set= ['meta_features', 'librosa_features']
# ---> will iteratuer through ehre 

################################################
##	    	Now go featurize!                 ##
################################################

# featurize all files accoridng to librosa featurize
for i in range(len(listdir)):
	if listdir[i][-4:] in ['.wav', '.mp3']:
		#try:

		sampletype='audio'

		# may want to determine if transcript exists if doesn't then transcribe...
		if audio_transcribe==True:
			transcript_dict, transcript = transcribe(listdir[i], default_audio_transcriber)

		# I think it's okay to assume audio less than a minute here...
		features, labels = audio_featurize(feature_set, listdir[i], transcript)
		print(features)

		try:
			data={'features':features.tolist(),
				  'labels': labels}
		except:
			data={'features':features,
				  'labels': labels}

		if listdir[i][0:-4]+'.json' not in listdir:
			# make new .JSON if it is not there with base array schema.
			basearray=make_features(sampletype)
			audio_features=basearray['features']['audio']
			audio_features[feature_set]=data
			basearray['features']['audio']=audio_features
			basearray['labels']=[foldername]
			transcript_list=basearray['transcripts']
			basearray['transcripts']=transcript_dict
			jsonfile=open(listdir[i][0:-4]+'.json','w')
			json.dump(basearray, jsonfile)
			jsonfile.close()
		elif listdir[i][0:-4]+'.json' in listdir:
			# overwrite existing .JSON if it is there.
			basearray=json.load(open(listdir[i][0:-4]+'.json'))
			basearray['features']['audio'][feature_set]=data
			basearray['labels']=[foldername]
			transcript_list=basearray['transcripts']
			transcript_list.append(transcript_dict)
			basearray['transcripts']=transcript_list
			jsonfile=open(listdir[i][0:-4]+'.json','w')
			json.dump(basearray, jsonfile)
			jsonfile.close()

		#except:
			#print('error')
	



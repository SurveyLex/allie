'''
               AAA               lllllll lllllll   iiii                      
              A:::A              l:::::l l:::::l  i::::i                     
             A:::::A             l:::::l l:::::l   iiii                      
            A:::::::A            l:::::l l:::::l                             
           A:::::::::A            l::::l  l::::l iiiiiii     eeeeeeeeeeee    
          A:::::A:::::A           l::::l  l::::l i:::::i   ee::::::::::::ee  
         A:::::A A:::::A          l::::l  l::::l  i::::i  e::::::eeeee:::::ee
        A:::::A   A:::::A         l::::l  l::::l  i::::i e::::::e     e:::::e
       A:::::A     A:::::A        l::::l  l::::l  i::::i e:::::::eeeee::::::e
      A:::::AAAAAAAAA:::::A       l::::l  l::::l  i::::i e:::::::::::::::::e 
     A:::::::::::::::::::::A      l::::l  l::::l  i::::i e::::::eeeeeeeeeee  
    A:::::AAAAAAAAAAAAA:::::A     l::::l  l::::l  i::::i e:::::::e           
   A:::::A             A:::::A   l::::::ll::::::li::::::ie::::::::e          
  A:::::A               A:::::A  l::::::ll::::::li::::::i e::::::::eeeeeeee  
 A:::::A                 A:::::A l::::::ll::::::li::::::i  ee:::::::::::::e  
AAAAAAA                   AAAAAAAlllllllllllllllliiiiiiii    eeeeeeeeeeeeee  

|  \/  |         | |    | |    
| .  . | ___   __| | ___| |___ 
| |\/| |/ _ \ / _` |/ _ \ / __|
| |  | | (_) | (_| |  __/ \__ \
\_|  |_/\___/ \__,_|\___|_|___/

Creates an excel sheet of all currently trained models with their model performances; 
useful to summarize all modeling sessions quickly; outputs to current directory.

Usage: python3 model2csv.py
'''

import os, json
import pandas as pd

def id_folder():
	curdir=os.getcwd()
	directories=['audio_models', 'text_models', 'image_models', 'video_models', 'csv_models']
	metrics_list=list()
	model_names=list()

	for i in range(len(directories)):
		try:
			os.chdir(curdir)
			os.chdir(directories[i])
			listdir=os.listdir()

			folders=list()
			for j in range(len(listdir)):
				if listdir[j].find('.') < 0:
					folders.append(listdir[j])

			curdir2=os.getcwd()

			for j in range(len(folders)):
				os.chdir(curdir2)
				os.chdir(folders[j])
				os.chdir('model')
				listdir2=os.listdir()
				jsonfile=folders[j]+'.json'
				for k in range(len(listdir2)):
					if listdir2[k] == jsonfile:
						g=json.load(open(jsonfile))
						metrics_=g['metrics']
						metrics_list.append(metrics_)
						model_names.append(jsonfile[0:-5])
		except:
			pass 
			# print(directories[i])
			# print('does not exist...')

	return metrics_list, model_names

metrics_list, model_names=id_folder()
accuracies=list()
roc_curve=list()
for i in range(len(model_names)):
	accuracies.append(metrics_list[i]['accuracy'])
	roc_curve.append(metrics_list[i]['roc_auc'])

data={'model names': model_names,
	  'accuracies': accuracies,
	  'roc_auc': roc_curve}

print(model_names)
print(accuracies)
print(roc_curve)

df=pd.DataFrame.from_dict(data)
df.to_csv('models.csv')

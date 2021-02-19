import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import tensorflow as tf
import os 
from scipy import signal 
from matplotlib.colors import LogNorm
from PIL import Image
import tensorflow_io as tfio
import random
random.seed(111)






def spec_augment(spec: np.ndarray, num_mask=2, 
                 freq_masking_max_percentage=0.1, time_masking_max_percentage=0.1):

    spec = spec.copy()
    for i in range(num_mask):
        all_frames_num, all_freqs_num = spec.shape
        freq_percentage = random.uniform(0.0, freq_masking_max_percentage)
        
        num_freqs_to_mask = int(freq_percentage * all_freqs_num)
        f0 = np.random.uniform(low=0.0, high=all_freqs_num - num_freqs_to_mask)
        f0 = int(f0)
        spec[:, f0:f0 + num_freqs_to_mask] = 0

        time_percentage = random.uniform(0.0, time_masking_max_percentage)
        
        num_frames_to_mask = int(time_percentage * all_frames_num)
        t0 = np.random.uniform(low=0.0, high=all_frames_num - num_frames_to_mask)
        t0 = int(t0)
        spec[t0:t0 + num_frames_to_mask, :] = 0
    
    return spec
    




classes = os.listdir('../classes')
for classe in classes :
    files = os.listdir("../classes/"+classe)
    if not os.path.exists("../classes/"+classe+'/spectro'):
        os.makedirs("../classes/"+classe+'/spectro')
    for img in files :
        if not os.path.exists("../classes/"+classe+'/spectro/augment/'):
            os.makedirs("../classes/"+classe+'/spectro/augment/')
        try :
            print(classe)
            nb_img =int(img.replace(".png",""))
            print(nb_img)
            ts = np.array(pd.read_csv(str(nb_img)+".csv")["engergy"])    
            fs  = 10e12
            #powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(ts, Fs=fs)
            """"plt.gca().set_axis_off()
            plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                        hspace = 0, wspace = 0)
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.savefig("../classes/"+classe+'/spectro/'+str(nb_img)+".png",frameon='false')"""

            f, t, s = signal.spectrogram(ts,fs,noverlap=int(len(ts)/8)-1,nperseg=int(len(ts)/8) )

            plt.figure()
            plt.imshow(10*np.log(s),aspect= 'auto')
            plt.gca().set_axis_off()
            plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                        hspace = 0, wspace = 0)
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
            plt.savefig("../classes/"+classe+'/spectro/'+str(nb_img)+".png",frameon='false')
            plt.show()
            plt.close()
            for i in range(3):
                plt.figure()
                plt.imshow(spec_augment(10*np.log(s)),aspect= 'auto')
                plt.gca().set_axis_off()
                plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                            hspace = 0, wspace = 0)
                plt.margins(0,0)
                plt.gca().xaxis.set_major_locator(plt.NullLocator())
                plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
                plt.savefig("../classes/"+classe+'/spectro/augment/'+str(nb_img)+"_"+str(i)+".png",frameon='false')
                plt.close()

            
        except Exception as e :
            print(e)
        """f, t, s = signal.spectrogram(ts, fs,noverlap=128 )

        plt.pcolormesh(t, f, 10*np.log(s), shading='gist_earth')
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                    hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
        plt.show()
        u, s, vh = np.linalg.svd( 10*np.log(s), full_matrices=True)
        smat = np.diag(s)
        for i in range(np.shape(smat)[1]) :
            matr =  np.dot(np.array(u[:len(s)-1,i] * smat[0,0]).reshape(-1,1), np.reshape(vh[i,:len(s)-1],(1,-1)))
            print(np.shape(matr))
            plt.pcolormesh(np.transpose(matr), shading='gist_earth')
            plt.colorbar()
            plt.show(block=True)
            plt.specgram(matr, Fs=fs)"""

                
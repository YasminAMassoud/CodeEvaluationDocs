
# coding: utf-8

# In[16]:


import scipy.io as sio
import numpy as np
import glob
import os
import scipy.misc as misc
from sklearn import preprocessing
import scipy as sp
import scipy.signal as spsig
import pandas as pd
import scipy.stats as spstat
import json
import time
from pandas import DataFrame, read_csv
import os
import glob
import time
from os import path
import scipy.io as io
from pathlib import Path


# In[27]:


def get_data(file, dataset):
    matfile = sio.loadmat(file)
    if dataset == 1:
        data = (matfile['data']).T
    elif dataset == 0:
         data = (matfile['Data']).T
    return data



def long_features(pat, outfile, datapath,dataset):
    df1 = pd.read_csv(datapath)
    #print(df1)
    #pat_num = pat
    #print(pat_num)
    #ff = glob.glob(f)
    #print(ff)

    #label = [str(os.path.basename(n)) for n in ff]
    #print(label)
    
    output = []
    featureList = []
    mydata = []
    mytimer = []
    bands = [0.1, 4, 8, 12, 30, 70]

    for row in range(len(df1)):

        for root, dirs, files in os.walk("."):
            #print(files)
            # print(files[2])
            if len(root.split('/')) == 1:
                for fil in files:
                    if dataset == 1:
                    #print(fil)
                        if fil[0] == '3' and df1.image.iloc[row][0:9] == 'Pat3Train':
                            if fil[1:] == df1.image.iloc[row][9:]:
                                #print(df1.image.iloc[row])
                                # print(fil)
                                f = root + '/' + fil
                                pat_num == 3
                                # matfile = sio.loadmat(f)
                                # data = (matfile['data']).T
                        elif fil == df1.image.iloc[row] :
                                #print(df1.image.iloc[row])
                                f = root + '/' + fil
                                pat_num = df1.image.iloc[row][3]
                                
                    elif dataset == 0:
                         if fil == df1.image.iloc[row][-16:]:
                                #print(df1.image.iloc[row][-16:])
                                f = root + '/' + fil
                                pat_num = pat
                                label= df['class'].iloc[row]
                                
                        # matfile = sio.loadmat(f)
                        # data = (matfile['data']).T
        print('finish')
        #pat_num = pat
                        ##ff = glob.glob(f)

                        ##label = [str(os.path.basename(n)) for n in ff]
                        ##print(label)

#         output = []
#         featureList = []
#         mydata = []
#         mytimer = []
#         bands = [0.1, 4, 8, 12, 30, 70]
                        # for i in range(len(ff)):
                        # print(float(i)/float(len(ff)))
        output = []
        outputtimer = []
        featureList = []
        featureListimer = []
        #if os.path.basename(fil) == '1_45_1.mat' :
         #      continue
        data = get_data(f, dataset)
                        # print(data)
        data = preprocessing.scale(data, axis=1, with_std=True)
        featureList.append('image')
                        # featureListimer.append('File')
                        ##output.append(label[i])
        output.append(df1.image.iloc[row])
                        # outputtimer.append(label[i])
        featureList.append('pat')
                        # featureListimer.append('pat')
        output.append(pat_num)
                        # outputtimer.append(pat_num)
        if dataset == 0:
            featureList.append('class')
            output.append(label)
            
        welsh = []

        for j in range(16) :
            hold = spsig.decimate(data[j, :], 5, zero_phase=True)

            start = time.time()
            total_time = time.time() - start
            featureListimer.append('sigma%i' % (j))
            outputtimer.append(total_time)

                            # start = time.time()
            featureList.append('kurt%i' % (j))
            output.append(spstat.kurtosis(hold))

            featureList.append('skew%i' % (j))
            output.append(spstat.skew(hold))

            diff = np.diff(hold, n=1)
            diff2 = np.diff(hold, n=2)

            featureList.append('zerod%i' % (j))
            output.append(((diff[:-1] * diff[1 :]) < 0).sum())

            featureList.append('RMS%i' % (j))
            output.append(np.sqrt((hold ** 2).mean()))

            f, psd = spsig.welch(hold, fs=80)
            print(f)
            print(psd)
            print('yes')

            psd[0] = 0

            featureList.append('MaxF%i' % (j))
            output.append(psd.argmax())

            featureList.append('SumEnergy%i' % (j))
            output.append(psd.sum())

            psd /= psd.sum()
            for c in range(1, len(bands)) :
                featureList.append('BandEnergy%i%i' % (j, c))
                output.append(psd[(f > bands[c - 1]) & (f < bands[c])].sum())

            featureList.append('Mobility%i' % (j))
            output.append(np.std(diff) / hold.std())

            featureList.append('Complexity%i' % (j))
            output.append(np.std(diff2) * np.std(hold) / (np.std(diff) ** 2.))

        mydata.append(pd.DataFrame({'Features' : output}, index=featureList).T)

                    # welsh_df = pd.DataFrame(welsh, columns=["value"])

    trainSample = pd.concat(mydata, ignore_index=True)
    #trainSample = pd.concat(mydata, sort=True)

    trainSample.to_csv(outfile)

    return 1


def main() :
    feat = json.load(open('SETTINGSWB.json'))
    #print('zhin')
    #print(feat)
    keys = list(feat.keys())

    pat = feat['pat']
    #print(pat)
    dataset = feat['run_on_contest_data']
    #print(dataset)
    subtract_mean = feat['subtract_mean']
    # pat = '1'
    #print(pat)
    
    newpath = feat['feat'] +'/feat' + '_dataset' + '[' + str(dataset) + ']' + '_pat' + '[' + str(pat) + ']' + '_subtract' + '[' + str(subtract_mean) + ']'
    if not os.path.exists(newpath):
            os.makedirs(newpath)

    if feat['run_on_contest_data'] == 1 :


        if feat['mode'] == 1 :
             
            print('train')
            outfile = newpath + '/trainWB.csv'
            #outfile = feat['feat'] +'/feat' + '_dataset' + '[' + str(dataset) + ']' + '_pat' + '[' + str(pat) + ']' + '_subtract' + '[' + str(subtract_mean) + ']' + '_trainWB.csv'
            l = long_features(pat, outfile, feat['CSV'], feat['run_on_contest_data'])

        elif feat['mode'] == 3 :
            # starting = time.time()
            print('test')
            outfile = newpath + '/testWB.csv'
            #outfile = feat['feat'] + '/feat_' + 'dataset' + '['+str(dataset) +']'+ '_pat' + '['+ str(pat) + ']'+ '_subtract' + '['+ str(subtract_mean) + ']'+'_traintestWB.csv'
            # timer = 'C:/Users/zhino/Documents/MelbourneUniversity-Research/Matthias_Docker/Singularity-Sheng/ContestData/Pat1/' + 'pat_' + str(pat) + '_long_train_timer.csv'
            l = long_features(pat, outfile, feat['CSV'], feat['run_on_contest_data'])
            # outfile = 'C:/Users/zhino/PycharmProjects/sheng' + 'pat_' + str(pat) + '_short_train.csv'

    elif feat['run_on_contest_data'] == 0 :

        if feat['mode'] == 1 :
            print('train')
            outfile = newpath + '/' + str(pat)+'_train.csv'
            #outfile = feat['feat'] +'/feat_' + 'dataset' + '['+str(dataset) +']'+ '_pat' +'['+ str(pat) +']'+ '_subtract' +'['+ str(subtract_mean) + ']'+ '_train.csv'
            l = long_features(pat, outfile, feat['CSV'],feat['run_on_contest_data'])

        elif feat['mode'] == 2 :
            print('validation')
            outfile = newpath + '/' + str(pat)+'_validation.csv'
            #outfile = feat['feat'] +'/feat_' + 'dataset' + '['+ str(dataset) +']'+ '_pat' + '['+str(pat) +']'+ '_subtract' + '['+str(subtract_mean) +']'+ '_validation.csv'
            l = long_features(pat, outfile, feat['CSV'],feat['run_on_contest_data'])

        elif feat['mode'] == 3 :
            print('test')
            outfile = newpath + '/' + str(pat)+'_test.csv'
            #outfile = feat['feat'] +'/feat_' + 'dataset' + '['+ str(dataset) + ']'+'_pat' + '['+ str(pat) + ']'+'_subtract' + '['+str(subtract_mean) +']'+ '_test.csv'
            l = long_features(pat, outfile, feat['CSV'],feat['run_on_contest_data'])


if __name__ == "__main__" :
    main()



# coding: utf-8

# In[1]:


import pdb
import numpy as np
import os
import pandas as pd
from sklearn import metrics
from sklearn import preprocessing
import random
from sklearn.ensemble import ExtraTreesClassifier
import csv
#import matplotlib as plt
import pickle
import json


# In[55]:




def trained_model(outfile, settings):   

pat_indx = settings['pat']
mode = settings['mode']
subtract_mean = settings['subtract_mean']
dataset = settings['run_on_contest_data']

if mode == 1 :

    data = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+']'+'_pat'+'['+str(pat_indx)+']'+'_subtract'+'['+str(subtract_mean)+']'+'/'+'trainWB.csv')
    test = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+']'+'_pat'+'['+str(pat_indx)+']'+'_subtract'+'['+str(subtract_mean)+']'+'/'+'traintestWB.csv')
 

elif mode == 2 :
    
    data = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+']'+'_pat'+'['+str(pat_indx)+']'+'_subtract'+'['+str(subtract_mean)+']'+'/trainWB.csv')
    test = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+']'+'_pat'+'['+str(pat_indx)+']'+'_subtract'+'['+str(subtract_mean)+']'+'/validationWB.csv')
 
    
elif mode == 3:  
    
    data = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+']'+'_pat'+'['+str(pat_indx)+']'+'_subtract'+'['+str(subtract_mean)+']'+'/trainWB.csv')
    test = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+']'+'_pat'+'['+str(pat_indx)+']'+'_subtract'+'['+str(subtract_mean)+']'+'/testWB.csv')
    #print(data)
    #print(test)
 #data = pd.concat([data,data2], axis=1)
#test = pd.concat([test,test2], axis=1)
#print('yes')
## clean the training data by removing nans

data.dropna(thresh=data.shape[1]-3, inplace=True)

data.replace([np.inf, -np.inf], np.nan, inplace=True)
test.replace([np.inf, -np.inf], np.nan, inplace=True)

data.fillna(0, inplace=True)
test.fillna(0, inplace=True)

data_file = data.image.values
test_file = test.image.values

  # get labels  
if dataset == 1:
    
    labela=[int(((str(os.path.basename(n)).split('_'))[2]).split('.')[0]) for n in data_file]
    #print(labela)
    labelt=[int(((str(os.path.basename(n)).split('_'))[2]).split('.')[0]) for n in test_file]
    #print(labelt)
    
elif dataset == 0: 
    
    labela= data['class'].values
    labelt= test['class'].values    
        

data['L'] = labela
#print(data)
test['L'] = labelt

data.sort_values(['L'], inplace=True, ascending=False)
#print(data)
test.sort_values(['L'], inplace=True, ascending=False)

   

if dataset == 1:  
  
# generate model using ExtraTrees
        #if data[data['pat'] == 1]:
            clf1 = ExtraTreesClassifier(n_estimators=3000, random_state=0, max_depth=11, n_jobs=2)
            data1= data[data['pat'] == 1]
            #print(data1)
            test1= test[test['pat']==1]
            #print(test1)
            
            labela1 = data1.L.values
            #print(labela1)
            labelt1 = test1.L.values
            #print(labelt1)
            
            data_feat1 = data1.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
            test_feat1 = test1.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
            
            feat_names1 = data_feat1.columns
            data_feat1 = data_feat1.values
            test_feat1 = test_feat1.values
            #print(test_feat1)
            
            clf1.fit(data_feat1, labela1)
            y_pred_prob1 = clf1.predict_proba(test_feat1)
           # print(y_pred_prob1)
            
            #mytest1=pd.DataFrame()
            
            #mytest1.insert(1, 'class', y_pred_prob1)
            test1.insert(1, 'class', y_pred_prob1)
            #newtest1= mytest1[['image', 'class']]
            newtest1= test1[['image', 'class']]
            
            labelt1[1] = 1
        
            this_AUC1 = metrics.roc_auc_score(labelt1, y_pred_prob1)
       
        #elif data[data['pat'] == 2]:
            clf2 = ExtraTreesClassifier(n_estimators=5000, random_state=0, max_depth=15, n_jobs=2,criterion='entropy')
            data2= data[data['pat'] == 2]
            #print(data2)
            test2= test[test['pat']==2]
            
            
            labela2 = data2.L.values
            labelt2 = test2.L.values
            
            data_feat2 = data2.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
            test_feat2 = test2.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
            
            feat_names2 = data_feat2.columns
            data_feat2 = data_feat2.values
            test_feat2 = test_feat2.values  
            
            clf2.fit(data_feat2, labela2)
            y_pred_prob2 = clf2.predict_proba(test_feat2)
            
            #mytest2=pd.DataFrame()
            test2.insert(1, 'class', y_pred_prob2)
            #mtest2.insert(1, 'class', y_pred_prob2)
            newtest2= test2[['image', 'class']]
            
            labelt2[1] = 1
            
            this_AUC2 = metrics.roc_auc_score(labelt2, y_pred_prob2)
       
            clf3 = ExtraTreesClassifier(n_estimators=4500, random_state=0, max_depth=15,criterion='entropy', n_jobs=2)
            data3= data[data['pat'] == 3]
            test3= test[test['pat']==3]
            
            labela3 = data3.L.values
            labelt3 = test3.L.values
            
            data_feat3 = data3.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
            test_feat3 = test3.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
            
            feat_names3 = data_feat3.columns
            data_feat3 = data_feat3.values
            test_feat3 = test_feat3.values
            
            clf3.fit(data_feat3, labela3)
            y_pred_prob3 = clf3.predict_proba(test_feat3)
            
            #mytest3=pd.DataFrame()
            
            #mytest3.insert(1, 'class', y_pred_prob3)
            #newtest3= mytest3[['image', 'class']]
            test3.insert(1, 'class', y_pred_prob3)
            newtest3= test3[['image', 'class']]
            
            labelt3[1] = 1
            
            this_AUC3 = metrics.roc_auc_score(labelt3, y_pred_prob3)
            
            test = [newtest1, newtest2, newtest3]
            testcontest = pd.concat(test, sort=False)
            
            testcontest.to_csv(settings['solutions']+'/contest_data_solution_'+'['+str(Seer_Username)+']'+'_mode'+'['+str(mode)+'].csv')
           

        #lr = LogisticRegression()
        #rf = RandomForestClassifier(n_estimators=4500, random_state=0, max_depth=15,criterion='gini', n_jobs=2,min_samples_split=7)
        #lda = LinearDiscriminantAnalysis()
elif dataset ==0: 
    
    labela = data.L.values
    labelt = test.L.values

    
    data_feat = data.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
    test_feat = test.drop(['image', 'pat', 'Unnamed: 0', 'L'], axis=1)
    feat_names = data_feat.columns
    data_feat = data_feat.values
    test_feat = test_feat.values   
    
    if pat == 1:
        clf = ExtraTreesClassifier(n_estimators=3000, random_state=0, max_depth=11, n_jobs=2)
        #lr = LogisticRegression()
        #rf = RandomForestClassifier(n_estimators=5000, random_state=0, max_depth=15, n_jobs=2,criterion='gini', min_samples_split=7)
        #lda=LinearDiscriminantAnalysis()
    elif pat == 2:
        clf = ExtraTreesClassifier(n_estimators=5000, random_state=0, max_depth=15, n_jobs=2,criterion='entropy')
        #lr = LogisticRegression()
        #rf = RandomForestClassifier(n_estimators=5000, random_state=0, max_depth=15, n_jobs=2,criterion='gini', min_samples_split=7)
        #lda = LinearDiscriminantAnalysis()
    elif pat == 3:
        clf = ExtraTreesClassifier(n_estimators=4500, random_state=0, max_depth=15,criterion='entropy', n_jobs=2)
        #lr = LogisticRegression()
        #rf = RandomForestClassifier(n_estimators=4500, random_state=0, max_depth=15,criterion='gini', n_jobs=2,min_samples_split=7)
        #lda = LinearDiscriminantAnalysis()
    elif pat in range(4,16):
        clf = ExtraTreesClassifier(n_estimators=3000, random_state=0, max_depth=11, n_jobs=2)
    
        
    clf.fit(data_feat, labela)
    y_pred_prob = clf.predict_proba(test_feat) 


    
    test.insert(1, 'class', y_pred_prob[:,1])
    newtest= test[['image', 'class']]
    newtest.to_csv(settings['solutions']+'/solution_'+'['+str(Seer_Username)+']'+'_pat'+'['+str(pat)+']'+'_mode'+'['+str(mode)+']'+'_subtract'+'['+str(subtract_mean)+']'+'.csv')
    
    
    this_AUC = metrics.roc_auc_score(labelt, y_pred_prob[:,1])
     
def main():

Seer_Username = 'Sheng'
settings = json.load(open('SETTINGSWB.json'))
pat = settings['pat']
mode = settings['mode']
subtract_mean = settings['subtract_mean']
dataset = settings['run_on_contest_data']

 

if settings['run_on_contest_data'] == 1 :

    if settings['mode'] == 1 :
        print('train')
        outfile = settings['solutions']+'/contest_data_solution_'+'['+str(Seer_Username)+']'+'_mode'+'['+str(mode)+']'+ '.csv'
        #data = pd.read_csv(settings['feat']+'/feat_dataset'+'['+str(dataset)+'_pat'+'['+str(pat)+']'+'_subtract'+'['+str(subtract_mean)+']'+str(mode)+'/train.csv')
        #test = pd.read_csv(settings['feat']+'/feat_dataset'+'/'+'['+str(dataset)+'_pat'+'['+str(pat)+']'+'_subtract'+'['+str(subtract_mean)+']'+str(mode)+'/traintest.csv')
        l = trained_model(outfile, settings)
        #l = trained_model(outfile, settings['feat'])

    elif settings['mode'] == 3 :
        # starting = time.time()
        print('test')
        outfile = settings['solutions']+'/contest_data_solution_'+'['+str(Seer_Username)+']'+'_mode'+'['+str(mode)+']'+'.csv'
        l = trained_model(outfile,settings)
        # outfile = 'C:/Users/zhino/PycharmProjects/sheng' + 'pat_' + str(pat) + '_short_train.csv'

elif settings['run_on_contest_data'] == 0 :

    if settings['mode'] == 1 :
        print('train')
        #solution_[Seer_Username]_pat[patient_index]_mode[mode]_subtract[subtract_mean].csv’
        outfile= settings['solutions']+ '/solution_'+'['+str(Seer_Username)+']'+'_pat'+'['+str(pat)+']'+'_mode'+'['+str(mode)+']'+'_subtract'+'['+str(subtract_mean)+']'+'.csv'
        l = trained_model(outfile,settings)

    elif settings['mode'] == 2 :
        print('validation')
        outfile= settings['solutions']+ '/solution_'+'['+str(Seer_Username)+']'+'_pat'+'['+str(pat)+']'+'_mode'+'['+str(mode)+']'+'_subtract'+'['+str(subtract_mean)+']'+'.csv'
        l = trained_model(outfile,settings)

    elif settings['mode'] == 3 :
        print('test')
        outfile= settings['solutions']+ '/solution_'+'['+str(Seer_Username)+']'+'_pat'+'['+str(pat)+']'+'_mode'+'['+str(mode)+']'+'_subtract'+'['+str(subtract_mean)+']'+'.csv'
        l = trained_model(outfile,settings)


if __name__ == "__main__" :
main()


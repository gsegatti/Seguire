#!/usr/bin/env python
# coding: utf-8

# In[1]:


def CountLines(GoodOrBad):
    
    filepath = "/home/gabriel/Documentos/Seguire/"
    if(GoodOrBad == 'good'):
        filepath += 'good.txt'
    else:
        filepath += 'bad.txt'
    
    with open(filepath) as file:
        count = 0
        for line in file:
            count += 1
            
    return count


# In[2]:


def Init():
    
    rows = []
    column = []
    filepath = "/home/gabriel/Documentos/Seguire/"
    
    with open(filepath + 'good.txt') as file:
        for line in file:
            column = []
            for i in range(0, 2):
                if i == 0:
                    column.append(line.strip('\n'))
                else:
                    column.append('good')
            rows.append(column)
            
    with open(filepath + 'bad.txt') as file:
        for line in file:
            column = []
            for i in range(0, 2):
                if i == 0:
                    column.append(line.strip('\n'))
                else:
                    column.append('bad')
            rows.append(column)
    
    return rows


# In[12]:


from sklearn.feature_extraction.text import CountVectorizer

def ComputeTDM(GoodOrBad, training_data):
    docs = [row['term'] for index,row in training_data.iterrows() if row['class'] == GoodOrBad]
    
    vec = CountVectorizer()
    X = vec.fit_transform(docs)
    tdm = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    
    return (tdm, X, vec)


# In[15]:


#LaPlace smoothing
from sklearn.feature_extraction.text import CountVectorizer

def ComputeTotal(training_data):
    docs = [row['term'] for index,row in training_data.iterrows()]

    vec = CountVectorizer()
    X = vec.fit_transform(docs)
    
    total_features = len(vec.get_feature_names())
    return total_features


# In[5]:


def ComputeFreq(vec, X):
    word_list = vec.get_feature_names();    
    count_list = X.toarray().sum(axis=0) 
    freq_s = dict(zip(word_list,count_list))
    return freq_s, word_list, count_list


# In[6]:


def Prob(tags, freq, total_count_feat, total_feat):
    prob = []
    for tag in tags:
        if tag in freq.keys():
            count = freq[tag]
        else:
            count = 0
        prob.append((count + 1)/(total_count_feat + total_feat))
        
    return dict(zip(tags,prob))


# In[16]:


import pandas as pd
import import_ipynb
import tmblr

def Training(tags):
    if not tags:
        return False
    
    rows = Init()
    columns = ['term', 'class']

    training_data = pd.DataFrame(rows, columns=columns)

    tdm_g, X_g, vec_g = ComputeTDM('good', training_data)
    tdm_b, X_b, vec_b = ComputeTDM('bad', training_data)

    freq_g, word_list_g, count_list_g = ComputeFreq(vec_g, X_g)
    freq_b, word_list_b, count_list_b = ComputeFreq(vec_b, X_b)

    prob_g = []
    for count in count_list_g:
        prob_g.append(count/len(word_list_g))
    #dict(zip(word_list_g, prob_g))

    prob_b = []
    for count in count_list_b:
        prob_b.append(count/len(word_list_b))
    #dict(zip(word_list_b, prob_b))

    total_feat = ComputeTotal(training_data)
    total_cnt_feat_g = count_list_g.sum(axis=0)
    total_cnt_feat_b = count_list_b.sum(axis=0)

    dg = Prob(tags, freq_g, total_cnt_feat_g, total_feat)
    db = Prob(tags, freq_b, total_cnt_feat_b, total_feat)


    lineG = CountLines('good')
    lineB = CountLines('bad')
    mult=1
    for tag in tags:
        mult *= dg[tag]
    good = mult * (lineG/(lineG+lineB))

    mult = 1
    for tag in tags:
        mult *= db[tag]
    bad = mult * (lineB/(lineG+lineB))

    print (str(good) + ' x ' + str(bad))

    if good > bad:
        return True
    else:
        return False


# In[18]:


Training(['me','hi'])


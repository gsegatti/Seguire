#!/usr/bin/env python
# coding: utf-8

# In[11]:


def GoodWord(index):
    filepath = "/home/gabriel/Documentos/Seguire/good.txt"
    with open(filepath) as file:
        count = 0
        for line in file:
            if(count == index):
                return line
            else:
                count += 1


# In[12]:


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


# In[13]:


import datetime as dt

def CheckDate(year, month, day):
    correctDate = None
    try:
        newDate = dt.datetime(year, month, day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate


# In[14]:


import random
import datetime as dt

def ItemNTimestamp():
    count = CountLines('good') - 1           #count number of lines, 0-indexed
    Nth = (random.randint(0, count))   #get a random number between number of lines
    item = GoodWord(Nth)

    #generate random month and year
    day = month = year = 0
    while(CheckDate(year, day, month) is False):
        day = (random.randint(1, 31))
        month = (random.randint(1, 12)) 
        year = (random.randint(14, 20))
        CheckDate(year, month, day)

    #convert generated date to datetime and get timestamp
    datetime_str = str(month) + '/' + str(day) + '/' + str(year)
    datetime_object = dt.datetime.strptime(datetime_str, '%m/%d/%y')

    if datetime_object > dt.datetime.now():
        datetime_object = dt.datetime.now()   
    timestamp = int(dt.datetime.timestamp(datetime_object))

    return item, timestamp

#precisa ter o campo "photos no json"
#TYPE = PHOTO


# In[15]:


def GetUrl():
    item, timestamp = ItemNTimestamp()
    item = item.strip('\n')
    limit = '1'

    key = 'api_key=V1ljqZjlhuHqlt4DtC4LeJm5izcBZWdDVbmrUYIgyWpwJrvfHB'
    url = 'http://api.tumblr.com/v2/tagged?tag=' + item + '&before=' + str(timestamp) + '&limit=' + limit
    url += '&' + key

    #req_url = 'http://api.tumblr.com/v2/tagged?tag=alexturner&limit=1&api_key=V1ljqZjlhuHqlt4DtC4LeJm5izcBZWdDVbmrUYIgyWpwJrvfHB'
    #tumblr_response = requests.get(req_url).json()

    return url, item


# In[2]:


import requests
import json

def returnResponse():
    response = None

    while not response:  
        url, item = GetUrl()
        #url = 'http://api.tumblr.com/v2/taged?tag=alexturner&limit=1&api_key=V1ljqZjlhuHqlt4DtC4LeJm5izcBZWdDVbmrUYIgyWpwJrvfHB'


        response = requests.get(url).json()
        if not response['response']:
            response = None
        elif response['response'][0]['type'] != 'photo':
            response = None
        else:
            response['response'][0]

    #print (url)        
    return (response['response'][0], item, url)


# In[17]:


def parseTags(tags): #tranformar em minusculo, sem espacos
    res = []
    
    for tag in tags:
        temp = tag.lower()
        temp = temp.replace(" ", "")
        res.append(temp)
    return res


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import import_ipynb
import tmblr
import Seguire
import requests


post,caption, url = None, None, None
tags = []


while not Seguire.Training(tags):
    post,caption,url = tmblr.returnResponse()
    tags = tmblr.parseTags(post['tags'])
#print (url)


# In[1]:


from telegram.ext import Updater
from telegram.ext import CommandHandler
import import_ipynb
import tmblr
import Seguire
import requests


updater = Updater(token='1159213896:AAGubBWb16oCfb5EYpIjxGZiY_9Xz-BMwsA', use_context=True)


dispatcher = updater.dispatcher

def start(update, context):
    post,caption,url = None, None, None
    tags = []


    while not Seguire.Training(tags):
        post,caption,url = tmblr.returnResponse()
        tags = tmblr.parseTags(post['tags'])
    context.bot.send_message(chat_id=update.effective_chat.id, text=url)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()


# In[2]:


from telegram.ext import Updater
from telegram.ext import CommandHandler

updater = Updater(token='1159213896:AAGubBWb16oCfb5EYpIjxGZiY_9Xz-BMwsA', use_context=True)
updater.stop()


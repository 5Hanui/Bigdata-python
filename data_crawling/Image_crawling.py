#!/usr/bin/env python
# coding: utf-8

# In[60]:


import requests
import time
import urllib
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from multiprocessing import Pool
from lxml.html import fromstring
import os, sys
import wget

no=1


# In[61]:


def search(url):

    browser = wd.Chrome('./tool/chromedriver.exe')
    browser.get(url)
    time.sleep(0.5)
    element=browser.find_element_by_tag_name('body')
    
    for i in range(40):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        
    browser.execute_script('window.scrollBy(0,1000)')
    
    for i in range(10):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
    
    time.sleep(1)
    
    source=browser.page_source
    
    return source


# In[62]:


def download_image(link):
    global no
    headers={"User_Agent":ua.random}
    
    try:
        r=requests.get(link, headers=headers)
    except:
        print("Cannot get link")

    wget.download(link,str(os.getcwd()) + "/"+query+ "/"+str(no)+".png")
#     사진 이름 카운트 no
    no=no+1 


# In[63]:


sys.setrecursionlimit(100000000)
query  = urllib.parse.quote('Armillaria mellea') #안에다 버섯이름 또는 영어 버섯 학명 기입!!!
# url="https://www.google.com/search?q="+query+"&as_st=y&tbs=itp:photo,ift:png&tbm=isch&tbas=0&source=lnt&sa=X&ved=0ahUKEwjM28fYx4jhAhWkIqYKHe_dA6AQpwUIHQ&biw=1036&bih=529&dpr=1.5"
url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjPiILx84vhAhVTIqYKHYowC6kQ_AUIDigB&biw=1280&bih=610"
source=search(url)
count=500 # 카운트 지정 500개할거면 그 이상 500+a 적기!

page_text=source.encode('utf-8').decode('ascii','ignore')
soup=BeautifulSoup(page_text,"html.parser")
ua=UserAgent()

if not os.path.isdir(query):
    os.makedirs(query)
    
# links=soup.find_all('a',class_='rg_l')
links=soup.find_all('img',class_='rg_ic')
# print(links[0])
for a in links[0:count]:
    print(a.get("data-src"))
    try:
        download_image(a.get("data-src"))
    except:
        pass


# In[ ]:





# In[ ]:





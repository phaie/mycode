#!/usr/bin/env python
# coding: utf-8

# In[183]:


from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import time,re
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import numpy as np


# In[184]:


os.chdir('F:\\新建文件夹\\test')


# In[185]:


#连接网页
option = FirefoxOptions()
option.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
option.add_argument("--headless")  # 不弹出浏览器
browser = Firefox(executable_path='geckodriver',options=option)
url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
browser.get(url)
time.sleep(5)


# In[186]:


#获取每页所有链接
def get_currenturl():
    alls = browser.find_elements(By.CSS_SELECTOR,"li a")
    curl =[i.get_attribute('href') for i in alls]
    utext =[i.text for i in alls]#链接标题
    #cu=zip(curl,utext)
    return curl,utext
#print(get_currenturl()[0])


# In[187]:


#获取卫健委网站20页通告信息
def get_page():
    page=['http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml']
    n=np.arange(2,21)
    for i in n:
        url ="http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_"+str(i)+".shtml"
        page.append(url)
    return page


# In[188]:


#获取通告
def get_news(url):
    browser.get(url)
    news = browser.page_source
    news = str(bs(news,"lxml").find_all(class_="con"))
    h=re.compile('<.*?>')
    news=h.sub('',news).split('\n\n\n')[0].strip('[\n')
    return news


# In[189]:


#获取全部链接和通告
temp1=[]
temp2=[]
temp3=[]
df=pd.DataFrame()
for url in get_page():
    browser.get(url)
    time.sleep(3)
    temp1=temp1 + get_currenturl()[0]
    temp2=temp2 + get_currenturl()[1]
    for u in get_currenturl()[0]:
        temp3.append([get_news(u)])
df['url']=temp1
df['text']=temp2
df['news']=temp3


# In[190]:


df.to_csv('./weijianwei.csv',encoding='utf-8_sig')
browser.quit()


# In[193]:

'''
browser.get('http://www.nhc.gov.cn/xcs/yqtb/202202/be4b2a0a70494c43863407ad17816f63.shtml')
time.sleep(5)
news = browser.page_source
news = str(bs(news,"lxml").find_all(class_="con"))
h=re.compile('<.*?>')
news=h.sub('',news).split('\n\n\n')[0].strip('[\n')
news
'''

# In[ ]:





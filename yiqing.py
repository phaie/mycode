from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import time,re
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
os.chdir('F:\\新建文件夹\\test')
option = FirefoxOptions()
option.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
option.add_argument("--headless")  # 隐藏浏览器
# option.add_argument('--no-sandbox')
browser = Firefox(executable_path='geckodriver',options=option)
url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
browser.get(url)
time.sleep(5)   #火狐需要人为等待，设置等待时间为5s
# print(browser.page_source)     #查看源码
c=0
df=pd.DataFrame()
#new_url = browser.find_element(By.CSS_SELECTOR,"li a").get_attribute('href')   #以一个为例
def meigeurl(new_url):
    browser.get(new_url)
    time.sleep(3)
    news = browser.page_source.replace('</font>','')

    #news = str(bs(news,"lxml")) #html.parser 是一个固定的值，是一个解析器

    # print(news)   #每页全部信息
    ch_all_dict = {}
    all_dict = {}
    gat_dict = {}   #港澳台
    #group(0)代表匹配的整句话


    '''我国31个省（自治区、直辖市）和新疆生产建设兵团（不包括港澳台）'''
    all_dict['pub_time'] = re.search('截至(.*?)24时',news).group(1)   #group(1)代表括号里的内容
    #time = re.search('截至(.*?)24时',news).group(1)
    #累计确诊（tx已有）
    all_dict['confirm_all'] = re.search('据31个省（自治区、直辖市）和新疆生产建设兵团.*?累计报告确诊病例(.*?)例.*?，',news).group(1)
    #现有确诊
    all_dict['confirm_now'] = re.search('据31个省（自治区、直辖市）和新疆生产建设兵团报告，现有确诊病例(.*?)例.*?，',news).group(1)
    #新增确诊
    all_dict['confirm_add'] = re.search('31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例(.*?)例。',news).group(1)
    #现有疑似（tx已有）
    all_dict['suspect_now'] = re.search('据31个省（自治区、直辖市）和新疆生产建设兵团.*?现有疑似病例(.*?)(例|\u3002)',news).group(1)
    #新增疑似
    all_dict['suspect_add'] = re.search('31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例.*?新增疑似病例(.*?)(例|\u3002)',news).group(1)
    #累计死亡（tx已有）
    all_dict['dead_all'] = re.search('据31个省（自治区、直辖市）和新疆生产建设兵团.*?累计死亡病例(.*?)例',news).group(1)
    #新增死亡
    all_dict['dead_add'] = re.search('31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例.*?新增死亡病例(.*?)',news).group(1)  #???
    #累计治愈（tx已有）
    all_dict['heal_all'] = re.search('据31个省（自治区、直辖市）和新疆生产建设兵团.*?累计治愈出院病例(.*?)例',news).group(1)
    #新增治愈
    all_dict['heal_new'] = re.search('当日新增治愈出院病例(.*?)例',news).group(1)
    #上海新增
    all_dict['sh_add'] = re.search('本土.*?上海(.*?)例',news).group(1)
    all_dict['sh_heal'] = re.search('治愈.*?上海(.*?)例',news).group(1)
    # for k,v in all_dict.items():
    #     print(k,v)


    '''港澳台'''
    #香港
    #香港累计确诊
    gat_dict['hk_confirm_all'] = re.search('香港特别行政区(\d+)例', news).group(1)
    #香港出院
    gat_dict['hk_heal_all'] = re.search('香港特别行政区.*?出院(\d+)例', news).group(1)
    #香港死亡
    gat_dict['hk_dead_all'] = re.search('香港特别行政区.*?死亡(.*?)例）', news).group(1)
    # 香港现有确诊
    gat_dict['hk_confirm_now'] = int(gat_dict['hk_confirm_all']) - int(gat_dict['hk_heal_all']) - int(gat_dict['hk_dead_all'])
    
    #澳门
    #澳门累计确诊
    gat_dict['om_confirm_all'] = re.search('澳门特别行政区(\d+)例', news).group(1)
    #澳门出院
    gat_dict['om_heal_all'] = re.search('澳门特别行政区.*?出院(.*?)例.*?死亡',news).group(1)
    # 澳门现有确诊
    gat_dict['om_confirm_now'] = int(gat_dict['om_confirm_all']) - int(gat_dict['om_heal_all'])
    
    #台湾
    #台湾累计确诊
    gat_dict['tw_confirm_all'] = re.search('台湾地区(\d+)例',news).group(1)
    #台湾出院
    gat_dict['tw_heal_all'] = re.search('台湾地区.*?出院(.*?)例.*?死亡',news).group(1)
    # 台湾死亡
    gat_dict['tw_dead_all'] = re.search('台湾地区.*?死亡(.*?)例）',news).group(1)
    # 台湾现有确诊
    gat_dict['tw_confirm_now'] = int(gat_dict['tw_confirm_all']) - int(gat_dict['tw_heal_all']) - int(gat_dict['tw_dead_all'])
    
    #三地汇总
    #港澳台累计确诊
    gat_dict['got_confirm_all'] = re.search('累计收到港澳台地区通报确诊病例(.*?)例。', news).group(1)
    # 港澳台现有确诊
    gat_dict['got_confirm_now'] = int(gat_dict['tw_confirm_now']) + int(gat_dict['hk_confirm_now']) + int(gat_dict['om_confirm_now'])
    # 港澳台累计治愈
    gat_dict['got_heal_all'] = int(gat_dict['hk_heal_all']) +int(gat_dict['om_heal_all']) +int(gat_dict['tw_heal_all'])
    # 港澳台累计死亡
    gat_dict['got_dead_all'] = int(gat_dict['hk_dead_all']) + int(gat_dict['tw_dead_all'])
    # for k,v in gat_dict.items():
    #     print(k,v)
    
    
    '''全国总数（含港澳台）'''
    # 全国总累计确诊
    ch_all_dict['ch_confirm_all'] = int(all_dict['confirm_all']) + int(gat_dict['got_confirm_all'])
    # 全国总现有确诊
    ch_all_dict['ch_confirm_now'] = int(all_dict['confirm_now']) + int(gat_dict['got_confirm_now'])
    # 全国总累计治愈
    ch_all_dict['ch_heal_all'] = int(all_dict['heal_all']) + int(gat_dict['got_heal_all'])
    # 全国总累计死亡
    ch_all_dict['ch_dead_all'] = int(all_dict['dead_all']) + int(gat_dict['got_dead_all'])
    # for k,v in ch_all_dict.items():
    #     print(k,v)
    df=pd.DataFrame(all_dict,index=[0])
    return df
#全部连接
alls = browser.find_elements(By.CSS_SELECTOR,"li a")
allurl=[]
for i in alls:
    urlnew=i.get_attribute('href')   
    allurl.append(urlnew)
#meigeurl(urlnew)
for i in allurl:
    print(i)
    df=pd.concat([df,meigeurl(i)],ignore_index=True)
print(df)
df.to_csv('./all.csv',encoding='utf-8_sig')
browser.quit()



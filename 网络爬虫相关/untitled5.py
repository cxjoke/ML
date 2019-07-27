# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:28:40 2018

@author: chenxi
"""

import requests
from bs4 import BeautifulSoup
import time



headers1 = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    'Cookie':'ll="108088"; gr_user_id=72be189a-6d24-4b66-8852-60ee5b347ef8; __utma=223695111.1753724081.1435500786.1451701876.1453725292.10; __utmz=223695111.1453725292.10.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; viewed="6962285_24753651"; bid="G6DEStA1WyY"; __utma=30149280.586657833.1424611223.1457245867.1457318642.32; __utmz=30149280.1454333768.29.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.4282; ps=y; ue="453908469@qq.com"; dbcl2="42824569:/o0ASefXQ5E"; ck="FEU7"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1458032271%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D8SixKdmwxL90_AAkojg-EO7bfBM5cXm_ijcfKJwfhvmevsp6lFZb4CJegjU60da5%26wd%3D%26eqid%3Dc16338b2000217060000000356e7ce8a%22%5D; push_noty_num=0; push_doumail_num=4; _pk_id.100001.4cf6=6a661f05ec4bb828.1435500786.22.1458032587.1458029671.; ap=1'}

headers2 = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    'Cookie':'ll="108088"; gr_user_id=72be189a-6d24-4b66-8852-60ee5b347ef8; __utma=223695111.1753724081.1435500786.1451701876.1453725292.10; __utmz=223695111.1453725292.10.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; viewed="6962285_24753651"; bid="G6DEStA1WyY"; __utma=30149280.586657833.1424611223.1457245867.1457318642.32; __utmz=30149280.1454333768.29.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.4282; ps=y; ue="453908469@qq.com"; dbcl2="42824569:/o0ASefXQ5E"; ck="FEU7"; ap=1; push_noty_num=0; push_doumail_num=4; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1458035474%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D8SixKdmwxL90_AAkojg-EO7bfBM5cXm_ijcfKJwfhvmevsp6lFZb4CJegjU60da5%26wd%3D%26eqid%3Dc16338b2000217060000000356e7ce8a%22%5D; _pk_id.100001.4cf6=6a661f05ec4bb828.1435500786.23.1458035474.1458032587.; _pk_ses.100001.4cf6=*'}

def get_links_from():
    urls = []
    list_urls = ['https://movie.douban.com/top250?start={}&filter=#!/i!/ckDefault'.format(str(i)) for i in range(0,250,25)]
    for list_url in list_urls:
        wb_data = requests.get(list_url,headers = headers2)
        soup = BeautifulSoup(wb_data.text,'lxml')
        for link in soup.select('div.hd a'):
            urls.append(link.get('href'))
    return (urls)


def get_item_info():
    time.sleep(1)
    urls = get_links_from()
    for url in urls:

        wb_data = requests.get(url,headers=headers1)
        soup = BeautifulSoup(wb_data.text,'lxml')


        title = soup.select('span[property="v:itemreviewed"]')[0].text,
        rank = soup.select('span.top250-no')[0].text,
        director = soup.select('a[rel="v:directedBy"]')[0].text,
        score = soup.select('strong[property="v:average"]')[0].text,
        imgs = soup.select('a.nbgnbg img')[0].get('src')
        print('电影名称:%s,排名:%s,评分:%s,导演:%s,海报:%s' % (title,rank,score,director,imgs))

get_item_info()






































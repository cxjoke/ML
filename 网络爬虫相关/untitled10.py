# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 20:23:29 2018

@author: chenxi
"""

url = "http://www.mtime.com/"  
soup = BeautifulSoup(requests.get(url).content, 'html.parser')  
#获取热门资讯  
news_list = soup.find_all('div', attrs={'class': 'newsitem'})  
for news in news_list:  
    title=news.find('a')['title']  
    content=news.find('a')['href']  
     #将热点资讯放在字典中，key值为资讯标题，value为资讯链接  
    news_dic[title]=content  
#获取热点图片  
hotpicture_list = soup.find_all('div', attrs={'class': 'over-a'})  
for hotpicture in hotpicture_list:  
    picture_url = re.findall("(?<=[(])[^()]+\.[^()]+(?=[)])", hotpicture['style'])[0].replace(' ', '')  
    urllib.urlretrieve(picture_url, picture_path)  
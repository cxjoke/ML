# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:53:32 2018

@author: chenxi
# -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    #以CSDN为例，CSDN不更改User Agent是无法访问的
    url = 'http://www.csdn.net/'
    head = {}
    #写入User Agent信息
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
 #创建Request对象
    req = request.Request(url, headers=head)
    #传入创建好的Request对象
    response = request.urlopen(req)
    #读取响应信息并解码
    html = response.read().decode('utf-8')
    #打印信息
    print(html)
import beautifulsoup



soup = BeautifulSoup('<div aria-label="5星, 747 份评分" class="rating" role="img" tabindex="-1">
 <div>
 <span class="rating-star">
 </span>
 <span class="rating-star">
 </span>
 <span class="rating-star">
 </span>
 <span class="rating-star">
 </span>
 <span class="rating-star">
 </span>
 </div>
 <span class="rating-count">
 747 份评分
 </span>
</div>')

soup.findAll("div", attrs={"class": rating-star});

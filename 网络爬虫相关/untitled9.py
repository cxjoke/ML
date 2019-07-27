# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 18:42:56 2018

@author: chenxi
"""
import scrapy
class lianjia(scrapy.Spider):
    name="lianjia"
    allowed_domains=["bj.lianjia.com"]
    start_urls=['https://bj.lianjia.com/ershoufang/']
    def start_request(self):
        user_agent='Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
        headers={'User_Agent':user_agent}
        for url in start_urls:
            yield scrapy.Request(url=url,headers=headers,method='GET',callback=self.parse)
    def parse(self,response):
        print(response)
        user_agent='Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
        headers={'User_Agent':user_agent}
        lists=response.body.decode('utf-8')
        selector=etree.HTML(lists)
        area_list=selector.xpath('/html/body/div[3]/div[1]/div[2]/dd/div[1]/div/a')
        print(area_list)
        for area in area_list:
            try:
                area_han=area.xpath('text()').pop()
                area_pin=area.xpath('@href').pop().split('/')[2]
                area_url='https://bj.lianjia.com/ershoufang/{}/'.format(area_pin)
                print(area_url)
                yield scrapy.Request(url=url,headers=headers,callback=self.detail_url,meta={"id1":area_han,"id2":area_pin})
            except Exception:
                pass
    def detail_url(self,response):
        'https://bj.lianjia.com/ershoufang/dongcheng/pg2/'
        for i in range(1,101):
            url='https://bj.lianjia.com/ershoufang/{}/pg{}/'.format(response.meta["id2"],str(i))
            time.sleep(random.randint(1,5))
            try:
                contents=request.get(url)
                content=etree.HTML(contents.content.decode('utf-8'))
                houselist=content.xpath('/html/body/div[4]/div[1]/ul/li')
                for house in houselist:
                    try:
                        item=LianjiaItem()
                        item['page']=i
                        item['title']=house.xpath('div[1]/div[1]/a/text()').pop()
                        item['community']=house.xpath('div[1]/div[2]/div/a/text()').pop()
                        item['model']=house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                        item['area']=house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2]
                        item['focus_num']=house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                        item['watch_num']=house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                        item['time']=house.xpath('div[1]/div[2]/text()').pop().split('/')[2]
                        item['price']=house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                        item['average_price']=house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                        self.url_detail=house.xpath('div[1]/div[1]/a/@href').pop()
                        item['Latitude']=self.get_latitude(self.url_detail)
                    except Exception:
                        pass
                    yield item
            except Exception:
                pass
class lianjiaItem(scrapy.Item):
    page=scrapy.Field()
    title=scrapy.Field()
    community=scrapy.Field()
    model=scrapy.Field()
    area=scrapy.Field()
    focus_num=scrapy.Field()
    watch_num=scrapy.Field()
    time=scrapy.Field()
    price=scrapy.Field()
    average_price=scrapy.Field()

        
    
lianjia()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
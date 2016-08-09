import scrapy
from items import CrawlebusItem
import crawlebus_api

class MySpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ['shanghai.8684.cn']
    start_urls = ['http://shanghai.8684.cn/']

    def parse(self, response):
        # # We want to inspect one specific response.
        # if ".org" in response.url:
        #     from scrapy.shell import inspect_response
        #     inspect_response(response, self)

        # Rest of parsing code.
        self.log('Hi, this is an item page! %s' % response.url)
        self._items = []
        
        for sel in response.xpath('//a'):
            item = CrawlebusItem()
            item['link'] = sel.xpath('@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            self._items.append(item)

            print item['link']
            if len(item['link']) >= 0 and len(item['desc']) >= 0:
                print 'save_crawlebus'
                crawlebus_api.save_crawlebus('', item['link'][0], item['desc'][0])
                print 'save_crawlebus succ'

        print self._items
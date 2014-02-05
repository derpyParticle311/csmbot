from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from csmbot.itemloaders import ParkLoader
from csmbot.util import absurl

class CCSParksSpider(Spider):
    name = "ccs-parks"
    allowed_domains = ["smgov.net"]
    start_urls = ["http://www.smgov.net/departments/ccs/content.aspx?id=32599"]

    def parse(self, response):
        """
        A spider contract:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        
        @url http://www.smgov.net/departments/ccs/content.aspx?id=32599
        @returns items 0 0
        @returns requests 1 50
        """
        sel = Selector(response)
        parks = sel.xpath("//a[@title='Parks']/following-sibling::*//a[contains(@title,'Park') and not(contains(@title,'Parks'))]")
        
        for park in [p.xpath("@href").extract()[0] for p in parks]:
            yield Request(absurl(park), callback=self.parse_park)

    def parse_park(self, response):
        """
        A spider contract:
        http://doc.scrapy.org/en/latest/topics/contracts.html
    
        @url http://www.smgov.net/departments/ccs/content.aspx?id=32744
        @returns items 1 1
        @returns requests 0 0
        @scrapes url name description address gmap features
        """
        sel = Selector(response)
        parkname = sel.xpath("//h2[@class='contentTitle']/text()").extract()
        content = sel.xpath("//td[contains(@class,'bodyContent')]/div")[0]

        loader = ParkLoader(selector=content)
        loader.add_value("url", response.url)
        loader.add_value("name", parkname) 
        loader.add_xpath("address", "p[1]/text()", re="^(.+)\s\($")
        loader.add_xpath("gmap", "p[1]/a/@href", re="^(http://maps\.google\.com.+)")
        loader.add_xpath("description", "p[position()>1]")

        loader.add_xpath("features", "ul[1]/li")

        h3s = content.xpath("h3")
        for h3 in h3s:
            li = h3.xpath("following-sibling::ul[1]/li")
            if len(li) > 0:
                loader.add_value("features", h3.extract())
                loader.add_value("features", li.extract())
            else:
                p = h3.xpath("following-sibling::p")
                if len(p) > 0:
                    loader.add_value("description", h3.extract())
                    loader.add_value("description", p.extract())
        
        return loader.load_item()

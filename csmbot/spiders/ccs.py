import urlparse

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

class CCSSpider(BaseSpider):
    name = "ccs"
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
            yield Request(urlparse.urljoin("http://www.smgov.net", park), callback=self.parse_park)

    def parse_park(self, response):
        """
        A spider contract:
        http://doc.scrapy.org/en/latest/topics/contracts.html
    
        @url http://www.smgov.net/departments/ccs/content.aspx?id=31699
        @returns items 1 1
        @returns requests 0 0
        @scrapes url name description address gmap features
        """
        pass

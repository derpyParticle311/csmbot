from scrapy.spider import BaseSpider

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
        pass

from scrapy.spider import BaseSpider

class CCSSpider(BaseSpider):
    name = "ccs"
    allowed_domains = ["smgov.net"]
    start_urls = ["http://www.smgov.net/departments/ccs/content.aspx?id=32599"]

    def parse(self, response):
        pass

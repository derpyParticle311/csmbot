# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Park(Item):
    url = Field()
    name = Field()
    address = Field()
    gmap = Field()
    features = Field()
    description = Field()

class FeatureSet(Item):
    name = Field()
    features = Field()

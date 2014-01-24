# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, TakeFirst

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

class ParkLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = Park

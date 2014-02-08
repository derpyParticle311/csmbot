from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst

from csmbot.items import Park

class ParkLoader(ItemLoader):
    default_item_class = Park
    default_output_processor = TakeFirst()

    images_out = Identity()
    description_out = Identity()
    features_out = Identity()

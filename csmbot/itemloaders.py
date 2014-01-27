import re

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, MapCompose, TakeFirst

from csmbot.items import Park

class ParkLoader(ItemLoader):
    default_item_class = Park
    default_output_processor = TakeFirst()
    lire = re.compile(r"<li.*?>(.+)</li>")

    description_out = MapCompose(shave)

    features_out = MapCompose(shave)

from scrapy.item import Field, Item

class Park(Item):
    url = Field()
    name = Field()
    address = Field()
    gmap = Field()
    latlong = Field()
    features = Field()
    description = Field()
    images = Field()

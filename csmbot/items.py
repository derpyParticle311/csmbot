from scrapy.item import Field, Item

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

import re
from urlparse import urljoin

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, MapCompose, TakeFirst, Compose

from csmbot.items import Park

def shave(s):
    return re.sub(r"((&nbsp;)|\s|\\xa0\<br/?>)+", " ", s).strip()

def absurl(url):
    return re.sub(r"^/", "http://www.smgov.net/", url)

def getkids(s, loader_context):
    match = re.match(r"<(h3|4)>(.+)</\1>", s)
    if match:
        featsname = match.group(2)
        kids = loader_context.dicts["selector"].xpath("ul/li")
    return s

def getparts(s):
    s1 = shave(s)
    match = re.match(r"(.*?)\(?<a.*?href=(\"|')(.+?)\2.*?>(.+?)</a>\)?(.*?)", s1)
    if match:
        link = {"text": match.group(4), "url": absurl(match.group(3))}
        ret = link
        if match.group(1):
            ret = match.group(1), ret
        if match.group(5):
            ret = ret, match.group(5)
        return ret
    return s1

class ParkLoader(ItemLoader):
    default_item_class = Park
    default_output_processor = TakeFirst()
    lire = re.compile(r"<li.*?>(.+)</li>")

    description_out = MapCompose(shave)

    features_out = MapCompose(shave)

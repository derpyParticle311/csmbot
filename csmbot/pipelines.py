# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

from csmbot.util import absurl

_emptyRegx = re.compile("((&nbsp;)|\s|<br/?>)+", re.I|re.U)
_unwrapRegx = re.compile(r"<(\w+?)>(.*?)</\1>", re.I|re.U)

class ParkDescriptionPipeline(object):
    """
    An item pipeline to clean up a Park item's description field
    """
    key = "description"

    def process_item(self, item, spider):
        values = []
        if self.key in item:
            for v in item[self.key]:
                m = _unwrapRegx.match(v)
                if m:
                    v = m.group(2)
                v = _emptyRegx.sub(" ", v).strip()
                if v:
                    values.append(v)
        item[self.key] = values
        return item

_catRegx = re.compile(r"<h3>(.+?)</h3>", re.I|re.U)
_linkRegx = re.compile(r"(.*?)\(?<a.*?href=(\"|')(.+?)\2.*?>(.+?)</a>\)?(.*?)", re.I|re.U)
_acreRegx = re.compile(r"^(\d*\.?\d*?)[\s-]+acres?", re.I|re.U)

class ParkFeaturesPipeline(object):
    """
    An item pipeline that categorizes a Park item's features
    and extracts links (<a href>) into a tuple structure
    """
    key = "features"

    def process_item(self, item, spider):
        cat = "General"
        features = {}
        features[cat] = []
        for v in item[self.key]:
            c = _catRegx.match(v)
            if c:
                cat = c.group(1)
                features[cat] = []
            else:
                m = _unwrapRegx.match(v)
                if m:
                    v = m.group(2)
                a = _acreRegx.match(v)
                if a:
                    item["acres"] = float(a.group(1))
                else:
                    features[cat].append(self.partition(v))
        item[self.key] = features
        return item
            
    def partition(self, text):
        parts = text
        m = _linkRegx.match(text)
        if m:
            parts = m.group(4)
            if m.group(1):
                parts = "{}{}".format(m.group(1), parts)
            if m.group(5):
                parts = "{}{}".format(parts, m.group(5))
            parts = {"text": _emptyRegx.sub(" ", parts), "url": absurl(m.group(3))}
        return parts

class ParkLatLongPipeline(object):
    """
    An item pipeline to split a Park item's latlong field
    """
    key = "latlong"

    def process_item(self, item, spider):
        latlong = {}
        if self.key in item:
            ll = item[self.key].split(",")
            latlong = {"lat": float(ll[0]), "long": float(ll[1])}
        item[self.key] = latlong
        return item

class ParkImagesPipeline(object):
    """
    An item pipeline to make absolute a Park item's image URLs
    """
    key = "images"

    def process_item(self, item, spider):
        images = []
        if self.key in item:
            for i in item[self.key]:
                images.append(absurl(i))
        item[self.key] = images
        return item

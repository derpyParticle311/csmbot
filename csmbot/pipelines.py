# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

from csmbot.util import absurl

_emptyRegx = re.compile(r"((&nbsp;)|\s|<br/?>|\\r|\\n|\\xa0)+", re.I|re.U)
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

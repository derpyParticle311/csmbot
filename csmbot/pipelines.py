# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from csmbot.util import absurl

class UnwrapOuterHTMLPipeline(object):
    """
    An item pipeline that removes the outer layer of HTML
    """
    keys = ["description", "features"]
    regx = re.compile(r"<(\w+?)>(.+?)</\1>", re.I|re.U)

    def process_item(self, item, spider):
        for key in self.keys:
            values = []
            if key in item:
                for v in item[key]:
                    m = regx.match(v)
                    if m: values.append(m.group(2))
            item[key] = values
        return item

class CleanExtendedWSPipeline(object):
    """
    An item pipeline that removes all manner of empty junk
    """
    keys = ["description", "features"]
    regx = re.compile(r"((&nbsp;)|\s|<br/?>)+", re.I|re.U)

    def process_item(self, item, spider):
        for key in self.keys:
            values = []
            if key in item:
                for v in item[key]:
                    values.append(m.sub(" ", v).strip())
            item[key] = values
        return item

class PartitionTextPipeline(object):
    """
    An item pipeline that extracts links (<a href>) into a tuple structure
    """
    catregx = re.compile(r"<h3>(.+?)</h3>", re.I|re.U)
    lnkregx = re.compile(r"(.*?)\(?<a.*?href=(\"|')(.+?)\2.*?>(.+?)</a>\)?(.*?)", re.I|re.U)

    def process_item(self, item, spider):
        for key in self.keys:
            values = []
            if key in item:
                for v in item[key]:
                    m = regx.match(v)
                    if m:
                        text = m.group(4)
                        if m.group(1):
                            text = "{} {}".format(m.group(1), text)
                        if m.group(5):
                            text = "{} {}".format(text, m.group(5))
                        values.append({"text": text, "url": absurl(m.group(3))})
                    else:
                        values.append(v)
            item[key] = values
        return item

import re

def absurl(url):
    return re.sub(r"^/", "http://www.smgov.net/", url)

def shave(s):
    return re.sub(r"((&nbsp;)|\s|\\xa0\<br/?>)+", " ", s).strip()

def getlinkparts(s):
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

import re

def absurl(url):
    return re.sub(r"^/", "http://www.smgov.net/", url)

def shave(s):
    return re.sub(r"((&nbsp;)|\s|\\xa0\<br/?>)+", " ", s).strip()

def getlinkparts(s):
    s1 = shave(s)
    match = re.match(r"(.*?)\(?<a.*?href=(\"|')(.+?)\2.*?>(.+?)</a>\)?(.*?)", s1)
    if match:
        text = match.group(4)
        if match.group(1):
            text = "{} {}".format(match.group(1), text)
        if match.group(5):
            text = "{} {}".format(text, match.group(5))
        return {"text": text, "url": absurl(match.group(3))}
    return s1

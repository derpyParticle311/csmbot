import re

def absurl(url):
    return re.sub(r"^/", "http://www.smgov.net/", url)

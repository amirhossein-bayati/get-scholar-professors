import requests
from requests.structures import CaseInsensitiveDict


def get_headers():
    headers = CaseInsensitiveDict()
    headers["Host"] = "scholar.google.com"
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["DNT"] = "1"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "none"
    headers["Sec-Fetch-User"] = "?1"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"
    return headers
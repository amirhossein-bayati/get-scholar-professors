import requests
from requests.structures import CaseInsensitiveDict


def get_headers():
    headers = CaseInsensitiveDict()
    headers["cache-control"] = "max-age=0"
    headers["content-encoding"] = "gzip"
    headers["content-type"] = "text/html; charset=UTF-8"
    headers["date"] = "Sat, 12 Mar 2022 22:23:07 GMT"
    headers["expires"] = "Fri, 01 Jan 1990 00:00:00 GMT"
    headers["pragma"] = "no-cache"
    headers["server"] = "citations"
    headers["set-cookie"] = "__Secure-3PSIDCC=AJi4QfGrOWtWhNESX1pBuIPWN6RtFm9Jo-g9necTbUVc8-p8f2Pxv9ohm1JHbn7NdR_vO2WxYvk; expires=Sun, 12-Mar-2023 22:23:07 GMT; path=/; domain=.google.com; Secure; HttpOnly; priority=high; SameSite=none"
    headers["x-content-type-options"] = "nosniff"
    headers["x-frame-options"] = "SAMEORIGIN"
    headers["x-xss-protection"] = "0"
    headers["authority"] = "scholar.google.com"
    headers["method"] = "GET"
    headers["path"] = "/citations?view_op=view_org&hl=en&org=4833850012421173011"
    headers["scheme"] = "https"
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["accept-language"] = "en-US,en;q=0.9,fa;q=0.8"
    headers["cookie"] = "GSP=LM=1639520170:S=vceLh_Ub8ZczlrXb; CONSENT=YES+srp.gws-20211208-0-RC2.zh-CN+FX+145; SID=HQhTTpjjIJDIadg-5ffEWefKV5vD7Qk2Ol70OzeHHUcqtIXDqrIAD56aLK8z6EAqAfrepg.; __Secure-1PSID=HQhTTpjjIJDIadg-5ffEWefKV5vD7Qk2Ol70OzeHHUcqtIXDqNZ9ohFSjBthsF8VEBfrwg.; __Secure-3PSID=HQhTTpjjIJDIadg-5ffEWefKV5vD7Qk2Ol70OzeHHUcqtIXDQk4IdNfxoKefSOxSlVZWvw.; HSID=Ai79QraieJFRvqCL1; SSID=Ao3Fyuxp2Zj_5sKWV; APISID=Js4HyQRdLiTD3B5J/A3TLifP876LT_n59e; SAPISID=dwsCypySZJt05pmd/AfQxUqCo8jW-n6mMr; __Secure-1PAPISID=dwsCypySZJt05pmd/AfQxUqCo8jW-n6mMr; __Secure-3PAPISID=dwsCypySZJt05pmd/AfQxUqCo8jW-n6mMr; SEARCH_SAMESITE=CgQI6JQB; AEC=AVQQ_LCMZHU1-H8bzyRWQOyGACmCQyeHEVU50odNVNdMh3r96XXjfxpwRA; 1P_JAR=2022-03-11-23; NID=511=l4y7JZ3NR3x-srodbAblAUewzoR0-7RTsZzpuNuJQBay9V_w9lz6WTob8ZK640cwizGf3FnkggF1adtkydyYbXEaQPiiBEA_Yr-tWQ4abQ6_j57RjtKYyG5zeRIQkA_e1pQKYJTu0IzQ28BhOnD3D83odx_zyTOZf2GOLpl9NgHC3MVUcw99bPMfzLwUlS_9TCKXfLTs2atXBxuqqBgP_4LF84UdPnIeZCNy-BlCuwBIvwi9ci1UT3sGGQEyF3WLTOf4h4E6moXwCeVFEGZviqYQ_Mr-stoXr-Kc4w9ZefVJ6K6W9gsXX6VPpJTFkSLpEzwf; SIDCC=AJi4QfFEd6yuz7aSiWx8W3cyEl7zc2oCl__jtqTOmdCZJkfIvMPwdiHYhpuExY8k-GvLAR6DnhQ; __Secure-3PSIDCC=AJi4QfEYvIgO-mSq7t9z9-5ue20WrL1LmA6tz5_gWZP4FT7UW4DamQkvtMaetNlXKk2JsbMQY6A"
    # headers["sec-ch-ua"] = "" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99""
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-ch-ua-platform"] = "Linux"
    headers["sec-fetch-dest"] = "document"
    headers["sec-fetch-mode"] = "navigate"
    headers["sec-fetch-site"] = "none"
    headers["sec-fetch-user"] = "?1"
    headers["upgrade-insecure-requests"] = "1"
    headers["user-agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"

    return headers



if __name__ == '__main__':
    get_headers()



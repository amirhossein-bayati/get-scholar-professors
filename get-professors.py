import json
import re
import time

import requests
from bs4 import BeautifulSoup

from get_scholar_headers import get_headers


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


def get_title(domain):
    index = requests.get(domain).text
    soup = BeautifulSoup(index, 'html.parser')
    uni_title = soup.find(id='gs_bdy').find(id='gs_bdy_ccl', role="main").find(id='gsc_sa_ccl').find('h2', class_='gsc_authors_header')
    uni_title = [text for text in uni_title.stripped_strings][0]

    return uni_title

def main():

    # try:
    #     with open('professors_urls.json', 'r') as file:
    #         professors_links = json.load(file)
    # except:
    #     professors_links = {}
    results = []
    # professors_links = {}
    req_counter = 0
    headers = get_headers()
    # with open(r'Universities-URL.yml') as file:
    #     urls = Find(file.read())

    with open('universities_urls.json', 'r') as file:
        data = json.load(file)

    for item in data:
        domain = item['url']
        country = item['country']
        global_score = item['global score']
        local_score = item['local score']
        university = item['university']

        if not domain:
            continue

        print("========================")
        print(domain)
        before_author = ""
        prof_count = 0
        # uni_title = get_title(domain)
        uni_title = university

        # professors_links[uni_title] = {}
        # time.sleep(random.randint(60, 120))

        while prof_count < 100:
            url = f"{domain}&after_author={before_author}"
            req = requests.get(url, headers=headers)
            req_counter += 1
            print(req)
            print(req_counter)

            index = req.text
            soup = BeautifulSoup(index, 'html.parser')

            main_div = soup.find(id='gs_bdy').find(id='gs_bdy_ccl', role="main").find(id='gsc_sa_ccl')


            professors = main_div.find_all(class_='gsc_1usr')
            for prof in professors:
                prof_count += 1
                url = prof.find('a', class_='gs_ai_pho').get('href')
                url = 'https://scholar.google.com/'+url
                # professors_links[uni_title][prof_count] = url

                res = {
                    'url': url,
                    'university_url': domain,
                    'country': country,
                    'university': university,
                    'global score': global_score,
                    'local score': local_score,
                    'positin in top 100 pages': prof_count
                }
                results.append(res)

                print(f'{prof_count}: {url}')

            try:
                footer = main_div.find('div', id='gsc_authors_bottom_pag', class_='gs_scl').find('div', class_='gsc_pgn').find('button', attrs={'aria-label': "Next"})
            except Exception as e:
                pass
            else:
                footer = main_div.find('div', id='gsc_authors_bottom_pag', class_='gs_scl').find('div', class_='gsc_pgn').find('button', class_='gs_btnPR')

            next_key = footer.get('onclick')

            before_author = next_key.split('\\')[-3][3:]
        time.sleep(100)

    with open('professors_urls.json', 'w') as file:
        json.dump(results, file)
    print("\n\n\nDONE")


if __name__ == '__main__':
    s_time = time.time()
    main()
    e_time = time.time()
    print("Time:", e_time-s_time)



##########################################################
# class_is_multi= { '*' : 'class'}
# xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml', multi_valued_attributes=class_is_multi)
# xml_soup.p['class']
# # [u'body', u'strikeout']


# XZRm_wXXAAAJ
# RFYDAK8f__8J
# jwkGAAV7__8J


# https://scholar.google.com//citations?hl=en&user=uC8sffYAAAAJ
# https://scholar.google.com//citations?hl=en&user=uC8sffYAAAAJ

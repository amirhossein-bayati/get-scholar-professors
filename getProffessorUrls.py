import json
import re
import time

import requests

from bs4 import BeautifulSoup

from getScholarHeaders import get_headers


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


def get_title(domain):
    index = requests.get(domain).text
    soup = BeautifulSoup(index, "html.parser")
    uni_title = (
        soup.find(id="gs_bdy")
        .find(id="gs_bdy_ccl", role="main")
        .find(id="gsc_sa_ccl")
        .find("h2", class_="gsc_authors_header")
    )
    uni_title = [text for text in uni_title.stripped_strings][0]

    return uni_title


def make_request_to_google(headers, domain, before_author):
    url = f"{domain}&after_author={before_author}"
    req = requests.get(url, headers=headers)
    print(req)

    index = req.text
    soup = BeautifulSoup(index, "html.parser")

    main_div = soup.find(id="gs_bdy").find(id="gs_bdy_ccl", role="main").find(id="gsc_sa_ccl")
    return main_div


def get_next_page(main_div):
    try:
        footer = (
            main_div.find("div", id="gsc_authors_bottom_pag", class_="gs_scl")
            .find("div", class_="gsc_pgn")
            .find("button", attrs={"aria-label": "Next"})
        )
    except:
        pass
    else:
        footer = (
            main_div.find("div", id="gsc_authors_bottom_pag", class_="gs_scl")
            .find("div", class_="gsc_pgn")
            .find("button", class_="gs_btnPR")
        )

    next_key = footer.get("onclick")

    try:
        return next_key.split("\\")[-3][3:]
    except:
        return None


def get_proffessors_url(
    results, country, university, domain, global_score, local_score, prof_count, professors
):
    for prof in professors:
        prof_count += 1
        url = prof.find("a", class_="gs_ai_pho").get("href")
        url = "https://scholar.google.com/" + url

        res = {
            "url": url,
            "university_url": domain,
            "country": country,
            "university": university,
            "global score": global_score,
            "local score": local_score,
            "positin in top 100 pages": prof_count,
        }
        results.append(res)
        print(f"{prof_count}: {url}")
    return results, prof_count


def save_json(results):
    with open("Json/professors_urls.json", "w") as file:
        json.dump(results, file)
    print("\n\n\nDONE")


def read_json():
    with open("Json/universities_full_data.json", "r") as file:
        data = json.load(file)
    return data


def main():

    results = []
    req_counter = 0
    headers = get_headers()

    data = read_json()

    for country in data:
        country_name = country["country"]
        for university in country["universities"]:
            domain = university["url"]
            global_score = university["global_score"]
            local_score = university["local_score"]
            university = university["university"]

            if not domain:
                continue

            print("========================")
            print(domain)
            before_author = ""
            prof_count = 0

            while prof_count < 100:
                main_div = make_request_to_google(headers, domain, before_author)
                if not main_div:
                    break
                req_counter += 1
                print(req_counter)
                professors = main_div.find_all(class_="gsc_1usr")
                results, prof_count = get_proffessors_url(
                    results,
                    country_name,
                    university,
                    domain,
                    global_score,
                    local_score,
                    prof_count,
                    professors,
                )

                before_author = get_next_page(main_div)

    save_json(results)


if __name__ == "__main__":
    """This module gets university urls from 'Json/university_urls.json' then
    extracts proffessors from that and save them in
    'Json/universities_full_data.json' file.
    """
    s_time = time.time()
    main()
    e_time = time.time()
    print("Time:", e_time - s_time)

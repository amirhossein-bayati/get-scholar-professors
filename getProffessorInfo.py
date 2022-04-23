import datetime
import json
import time

import requests
from bs4 import BeautifulSoup


def get_date_of_first_and_last_publications(years):
    years.sort(reverse=True)
    last = years[0]
    first = years[-1]
    differrence = last - first
    i = 1
    while differrence > 200:
        i += 1
        first = years[-i]
        differrence = years[0] - first

    return first, last


def update_articles(url, ly):
    cstart = 0
    finished = 0
    publication_count = 0
    date_of_the_first_publication = int(ly)
    uncited_count = 0
    us_patent = 0
    publication_years = []
    try:
        while finished != 1:
            # time.sleep(20)
            url = f"{url}&cstart={cstart}&pagesize=100"
            req = requests.get(url)
            print(req)

            index = req.text
            soup = BeautifulSoup(index, "html.parser")
            main_div = soup.find("div", id="gs_top").find("div", id="gsc_bdy")
            publications = main_div.find("table", id="gsc_a_t").find("tbody")
            articles = publications.find_all("tr")

            for article in articles:
                if "There are no articles in this profile." == article.text:
                    date_of_the_first_publication = get_date_of_first_and_last_publications(
                        publication_years
                    )[0]
                    print("DOne")
                    return [
                        publication_count,
                        uncited_count,
                        date_of_the_first_publication,
                        us_patent,
                    ]

                publication_count += 1
                patent_text = article.find_all("td")[0].find_all(class_="gs_gray")
                for pat in patent_text:
                    txt = pat.text.lower()
                    if "us patent" in txt:
                        us_patent += 1

                cited = article.find_all("td")[1].text
                year = article.find_all("td")[2].text

                if year:
                    year = int(year)
                    publication_years.append(year)
                if not cited:
                    uncited_count += 1

            cstart += 100
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!")
        print(e)
        return [None, None, None, None]


def get_last_publication(url):
    url = url + "&sortby=pubdate"
    req = requests.get(url)
    print(req)
    index = req.text
    soup = BeautifulSoup(index, "html.parser")
    main_div = soup.find("div", id="gs_top").find("div", id="gsc_bdy")
    publications = main_div.find("table", id="gsc_a_t").find("tbody")
    date_of_the_last_publication = publications.find("tr").find_all("td")[2].text

    return date_of_the_last_publication


try:
    with open("Json/professors_infos.json", "r") as file:
        results = json.load(file)
except:
    results = []

try:
    with open("Json/errors.json", "r") as file:
        error_links = json.load(file)
except:
    error_links = []


def main():
    with open("Json/professors_urls.json", "r") as file:
        data = json.load(file)

    for item in data[1700:2300]:
        index_of_prof = data.index(item)
        print(index_of_prof)
        if index_of_prof % 50 == 0:
            msg = f"index: {index_of_prof}"
            print(msg)
            time.sleep(0)

        url = item["url"]
        country = item["country"]
        qs_uni_world_ranking = item["global score"]
        qs_uni_country_ranking = item["local score"]
        uni = item["university"]
        positin_in_top_100_pages = item["positin in top 100 pages"]
        university_url = item["university_url"]

        try:
            req = requests.get(url)
            print(url)
            print(req)
            if req.status_code != 200:
                print("req error")
                msg = f"index: {index_of_prof}"
                print(msg)
                time.sleep(0)
                continue

            index = req.text
            soup = BeautifulSoup(index, "html.parser")
            main_div = soup.find("div", id="gs_top").find("div", id="gsc_bdy")
            author_info = main_div.find("div", id="gsc_prf_w", class_="gsc_lcl").find(id="gsc_prf")

            date = (
                datetime.datetime.now().date().strftime("%d/%m/%Y")
            )  ###################################
            author_name = (
                author_info.find(id="gsc_prf_i").find(id="gsc_prf_in").text
            )  #######################################

            author_bio = author_info.find(id="gsc_prf_i").find("a", class_="gsc_prf_ila")

            try:
                university = author_bio.text  ########################
            except:
                university = uni

            google_scholar_link_of_the_university = university_url

            google_scholar_link_of_the_author = url  ###############################

            projects_bar = main_div.find("div", class_="gsc_rsb")

            articles = projects_bar.find("table", id="gsc_rsb_st").find("tbody")

            citation = (
                articles.find_all("tr")[0].find("td", class_="gsc_rsb_std").text
            )  ########################
            h_index = (
                articles.find_all("tr")[1].find("td", class_="gsc_rsb_std").text
            )  ###########################
            i10_index = (
                articles.find_all("tr")[2].find("td", class_="gsc_rsb_std").text
            )  #########################

            ##############################################
            publications = main_div.find("table", id="gsc_a_t").find("tbody")

            the_most_citation = publications.find("tr").find_all("td")[
                1
            ]  #################################
            the_most_citation = int([text for text in the_most_citation.stripped_strings][0])

            x = [i.find_all("td")[1] for i in publications.find_all("tr")[:10]]
            sum_of_to_10_citations = 0
            for i in x:
                res = len([text for text in i.stripped_strings])
                if res != 0:
                    t = int([text for text in i.stripped_strings][0])
                    sum_of_to_10_citations += t
            sum_of_to_10_citations_density = sum_of_to_10_citations / 12
            date_of_the_last_publication = get_last_publication(url)
            ###############################################

            (
                num_of_publications,
                num_of_publications_without_citation,
                date_of_the_first_publication,
                us_patent,
            ) = update_articles(url, date_of_the_last_publication)
            uncited_rate = num_of_publications_without_citation / num_of_publications

            observation_time_window = int(date_of_the_last_publication) - int(
                date_of_the_first_publication
            )
            average_citation_per_publication = int(citation) / int(num_of_publications)

            if int(observation_time_window) == 0:
                observation_time_window = int(observation_time_window) + 1

            average_citation_per_year = int(citation) / int(observation_time_window)

            average_publication_per_year = int(num_of_publications) / int(observation_time_window)

            the_most_citation_density = int(the_most_citation) / int(citation)

            us_patent = int(us_patent)
            patents_and_Publications_balance = us_patent / num_of_publications

            res = {}
            res["Index"] = index_of_prof
            res["Date"] = date
            res["Author name"] = author_name
            res["University"] = university
            res["country"] = country
            res["Google Scholar link of the university"] = google_scholar_link_of_the_university
            res["Google Scholar link of the author"] = google_scholar_link_of_the_author
            res["Qs uni world ranking"] = qs_uni_world_ranking
            res["Qs uni country ranking"] = qs_uni_country_ranking
            res["Citation"] = citation
            res["h-index"] = h_index
            res["i10-index"] = i10_index
            res["No. Of Publications"] = num_of_publications
            res["No. Of publications without citation"] = num_of_publications_without_citation
            res["Uncited rate"] = uncited_rate
            res["No.Of US pattent"] = us_patent
            res["Patents and Publications balance"] = patents_and_Publications_balance
            res["The most citation"] = the_most_citation
            res["The most citation density"] = the_most_citation_density
            res["Sum of top 10 citations"] = sum_of_to_10_citations
            res["Sum of top 10 citations density"] = sum_of_to_10_citations_density
            res["Date of the first publication (year)"] = date_of_the_first_publication
            res["Date of the last publication (year)"] = date_of_the_last_publication
            res["Observation time window (years)"] = observation_time_window
            res["average citation per publication"] = average_citation_per_publication
            res["average citation per year"] = average_citation_per_year
            res["average publication per year"] = average_publication_per_year
            res["Author's positin in top 100 pages"] = positin_in_top_100_pages

            print(res)
            results.append(res)
            with open("Json/professors_infos.json", "w") as file:
                json.dump(results, file)
                print("saved...")

        except Exception as e:
            print(e)
            error_links.append(url)
            with open("Json/errors.json", "w") as file:
                json.dump(error_links, file)
                print("saved...")
        print("================================\n")
        time.sleep(0)


if __name__ == "__main__":
    """This module reads 'Json/professors_urls.json'
    file and start scraping all proffessor articles and saving them.
    if there is an error with specific article, will be saved in
    'Json/errors.json' else will be saved in 'Json/professors_infos.json' file.
    """
    s_time = time.time()
    main()
    e_time = time.time()
    print("Time:", e_time - s_time)

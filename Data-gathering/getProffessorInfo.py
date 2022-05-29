import functools
import json
import time

from datetime import datetime

import humanize
import requests

from bs4 import BeautifulSoup


def get_date_of_first_and_last_publications(years):
    years.sort(reverse=True)
    now = datetime.now().year
    last = years[0]
    j = 0
    while last > now:
        j += 1
        last = years[j]
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
            articles = get_list_of_articles(url, cstart)
            for article in articles:
                if "There are no articles in this profile." == article.text:
                    (
                        date_of_the_first_publication,
                        date_of_the_last_publication,
                    ) = get_date_of_first_and_last_publications(publication_years)
                    print("Done")

                    return [
                        publication_count,
                        uncited_count,
                        date_of_the_first_publication,
                        date_of_the_last_publication,
                        us_patent,
                    ]

                publication_count += 1
                us_patent = get_number_of_us_patent(us_patent, article)

                cited = article.find_all("td")[1].text
                if not cited:
                    uncited_count += 1

                year = article.find_all("td")[2].text
                if year:
                    year = int(year)
                    publication_years.append(year)
            cstart += 100
    except Exception as e:
        print("!" * 25)
        print(e)
        return [None, None, None, None]


def get_list_of_articles(url, cstart):
    url = f"{url}&cstart={cstart}&pagesize=100"
    req = requests.get(url)
    print(req)

    index = req.text
    soup = BeautifulSoup(index, "html.parser")
    main_div = soup.find("div", id="gs_top").find("div", id="gsc_bdy")
    publications = main_div.find("table", id="gsc_a_t").find("tbody")
    articles = publications.find_all("tr")
    return articles


def get_number_of_us_patent(us_patent, article):
    patent_text = article.find_all("td")[0].find_all(class_="gs_gray")
    for pat in patent_text:
        txt = pat.text.lower()
        if "us patent" in txt:
            us_patent += 1
    us_patent = int(us_patent)
    return us_patent


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


def open_results_file():
    try:
        with open("Json/professors_infos.json", "r") as file:
            results = json.load(file)
    except:
        results = []
    return results


def open_error_file():
    try:
        with open("Json/errors.json", "r") as file:
            error_links = json.load(file)
    except:
        error_links = []
    return error_links


def validata_english_url(url):
    seperator = "&user="
    first, second = url.split(seperator)
    path, _ = first.split("=")
    return path + "=en" + seperator + second


def extract_features(url, uni, university_url, main_div):
    author_info = get_author_info(main_div)
    # get_author_bio(author_info) # Not used
    date = get_date()
    author_name = get_author_name(author_info)
    university = uni
    google_scholar_link_of_the_university = university_url
    google_scholar_link_of_the_author = url
    articles = get_articles(main_div)
    citation = get_citation(articles)
    h_index = get_h_index(articles)
    i10_index = get_i10_index(articles)
    publications = get_publications(main_div)
    the_most_citation = get_the_most_citation(publications)
    sum_of_to_10_citations = get_sum_of_to_10_citations(publications)
    sum_of_to_10_citations_density = get_sum_of_to_10_citations_density(sum_of_to_10_citations)
    date_of_the_last_publication = get_last_publication(url)
    (
        num_of_publications,
        num_of_publications_without_citation,
        date_of_the_first_publication,
        date_of_the_last_publication,
        us_patent,
    ) = update_articles(url, date_of_the_last_publication)

    uncited_rate = get_uncited_rate(num_of_publications, num_of_publications_without_citation)

    observation_time_window = get_observation_time_window(
        date_of_the_last_publication, date_of_the_first_publication
    )

    average_citation_per_publication = get_average_citation_per_publication(
        citation, num_of_publications
    )

    average_citation_per_year = get_average_citation_per_year(citation, observation_time_window)

    average_publication_per_year = get_average_publication_per_year(
        num_of_publications, observation_time_window
    )

    the_most_citation_density = get_the_most_citation_density(citation, the_most_citation)

    patents_and_Publications_balance = get_patents_and_Publications_balance(
        num_of_publications, us_patent
    )

    return (
        date,
        author_name,
        university,
        google_scholar_link_of_the_university,
        google_scholar_link_of_the_author,
        citation,
        h_index,
        i10_index,
        the_most_citation,
        sum_of_to_10_citations,
        sum_of_to_10_citations_density,
        date_of_the_last_publication,
        num_of_publications,
        num_of_publications_without_citation,
        date_of_the_first_publication,
        us_patent,
        uncited_rate,
        observation_time_window,
        average_citation_per_publication,
        average_citation_per_year,
        average_publication_per_year,
        the_most_citation_density,
        patents_and_Publications_balance,
    )


def get_author_info(main_div):
    author_info = main_div.find("div", id="gsc_prf_w", class_="gsc_lcl").find(id="gsc_prf")
    return author_info


def get_date():
    date = datetime.now().date().strftime("%d/%m/%Y")
    return date


def get_patents_and_Publications_balance(num_of_publications, us_patent):
    patents_and_Publications_balance = us_patent / num_of_publications
    return patents_and_Publications_balance


def get_the_most_citation_density(citation, the_most_citation):
    the_most_citation_density = int(the_most_citation) / int(citation)
    return the_most_citation_density


def get_average_publication_per_year(num_of_publications, observation_time_window):
    average_publication_per_year = int(num_of_publications) / int(observation_time_window)
    return average_publication_per_year


def get_average_citation_per_year(citation, observation_time_window):
    average_citation_per_year = int(citation) / int(observation_time_window)
    return average_citation_per_year


def get_average_citation_per_publication(citation, num_of_publications):
    average_citation_per_publication = int(citation) / int(num_of_publications)
    return average_citation_per_publication


def get_observation_time_window(date_of_the_last_publication, date_of_the_first_publication):
    observation_time_window = int(date_of_the_last_publication) - int(
        date_of_the_first_publication
    )
    if int(observation_time_window) == 0:
        observation_time_window = int(observation_time_window) + 1
    return observation_time_window


def get_uncited_rate(num_of_publications, num_of_publications_without_citation):
    uncited_rate = num_of_publications_without_citation / num_of_publications
    return uncited_rate


def get_sum_of_to_10_citations_density(sum_of_to_10_citations):
    sum_of_to_10_citations_density = sum_of_to_10_citations / 12
    return sum_of_to_10_citations_density


def get_sum_of_to_10_citations(publications):
    x = [i.find_all("td")[1] for i in publications.find_all("tr")[:10]]
    sum_of_to_10_citations = 0
    for i in x:
        res = len([text for text in i.stripped_strings])
        if res != 0:
            t = int([text for text in i.stripped_strings][0])
            sum_of_to_10_citations += t
    return sum_of_to_10_citations


def get_author_bio(author_info):
    author_bio = author_info.find(id="gsc_prf_i").find("a", class_="gsc_prf_ila")


def get_author_name(author_info):
    author_name = author_info.find(id="gsc_prf_i").find(id="gsc_prf_in").text
    return author_name


def get_the_most_citation(publications):
    the_most_citation = publications.find("tr").find_all("td")[1]
    the_most_citation = int([text for text in the_most_citation.stripped_strings][0])
    return the_most_citation


def get_publications(main_div):
    publications = main_div.find("table", id="gsc_a_t").find("tbody")
    return publications


def get_i10_index(articles):
    i10_index = articles.find_all("tr")[2].find("td", class_="gsc_rsb_std").text
    return i10_index


def get_h_index(articles):
    h_index = articles.find_all("tr")[1].find("td", class_="gsc_rsb_std").text
    return h_index


def get_citation(articles):
    citation = articles.find_all("tr")[0].find("td", class_="gsc_rsb_std").text
    return citation


def get_articles(main_div):
    projects_bar = main_div.find("div", class_="gsc_rsb")

    articles = projects_bar.find("table", id="gsc_rsb_st").find("tbody")
    return articles


def get_scholar_main_div(index_of_prof, url):
    req = requests.get(url)
    print(url)
    print(req)
    if req.status_code != 200:
        print("req error")
        msg = f"index: {index_of_prof}"
        print(msg)
        return None

    index = req.text
    soup = BeautifulSoup(index, "html.parser")
    main_div = soup.find("div", id="gs_top").find("div", id="gsc_bdy")
    return main_div


def parse_urls_file(item):
    url = item["url"]
    url = validata_english_url(url)
    country = item["country"]
    qs_uni_world_ranking = item["global score"]
    qs_uni_country_ranking = item["local score"]
    uni = item["university"]
    positin_in_top_100_pages = item["positin in top 100 pages"]
    university_url = item["university_url"]
    return (
        url,
        country,
        qs_uni_world_ranking,
        qs_uni_country_ranking,
        uni,
        positin_in_top_100_pages,
        university_url,
    )


def get_index_of_prof(data, item):
    index_of_prof = data.index(item)
    if index_of_prof % 50 == 0:
        msg = f"index: {index_of_prof}"
        print(msg)
        time.sleep(0)
    return index_of_prof


def create_json_obj(
    index_of_prof,
    country,
    qs_uni_world_ranking,
    qs_uni_country_ranking,
    positin_in_top_100_pages,
    url,
    uni,
    university_url,
    main_div,
):

    (
        date,
        author_name,
        university,
        google_scholar_link_of_the_university,
        google_scholar_link_of_the_author,
        citation,
        h_index,
        i10_index,
        the_most_citation,
        sum_of_to_10_citations,
        sum_of_to_10_citations_density,
        date_of_the_last_publication,
        num_of_publications,
        num_of_publications_without_citation,
        date_of_the_first_publication,
        us_patent,
        uncited_rate,
        observation_time_window,
        average_citation_per_publication,
        average_citation_per_year,
        average_publication_per_year,
        the_most_citation_density,
        patents_and_Publications_balance,
    ) = extract_features(url, uni, university_url, main_div)

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
    return res


def save_failed_data(error_links):
    with open("Json/errors.json", "w") as file:
        json.dump(error_links, file)
        print("saved...")


def save_succeed_data(results):
    with open("Json/professors_infos.json", "w") as file:
        json.dump(results, file)
        print("saved...")


def get_files_url(file_name):
    with open("Json/{}".format(file_name), "r") as file:
        data = json.load(file)
    return data


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {humanize.precisedelta(elapsed_time)}")
        return value

    return wrapper_timer


@timer
def main():
    data = get_files_url("professors_urls.json")
    print(f"Length of data: {len(data)}")
    for item in data:
        index_of_prof = get_index_of_prof(data, item)
        (
            url,
            country,
            qs_uni_world_ranking,
            qs_uni_country_ranking,
            uni,
            positin_in_top_100_pages,
            university_url,
        ) = parse_urls_file(item)
        try:
            main_div = get_scholar_main_div(index_of_prof, url)
            if not main_div:
                continue
            json_obj = create_json_obj(
                index_of_prof,
                country,
                qs_uni_world_ranking,
                qs_uni_country_ranking,
                positin_in_top_100_pages,
                url,
                uni,
                university_url,
                main_div,
            )
            results.append(json_obj)
            save_succeed_data(results)
        except Exception as e:
            print(e)
            error_links.append(url)
            save_failed_data(error_links)
        print("=" * 32, end="\n\n")
        time.sleep(0)


results = open_results_file()
error_links = open_error_file()

if __name__ == "__main__":

    """This module reads 'Json/professors_urls.json'
    file and start scraping all proffessor articles and saving them.
    if there is an error with specific article, will be saved in
    'Json/errors.json' else will be saved in 'Json/professors_infos.json' file.
    """

    main()
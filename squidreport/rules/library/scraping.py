import requests
from bs4 import BeautifulSoup
import pandas as pd


# receive data by wikipedia for scrape list of port and protocol
def parse_wikipedia_port_proto():
    URL = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    port_info = pd.DataFrame()

    for table in soup.find_all("table"):
        table_parsed = []
        if not table.caption:
            continue
        caption = table.caption.text.strip()
        if "Legend" in caption:
            continue
        body = table.tbody
        header = body.find("tr")
        col_names = [
            a.text.strip().replace("[1]", "").replace(" ", "_")
            for a in header.find_all("th")
        ]

        for line in table.find_all("tr"):
            values = [value.text.strip() for value in line.find_all("td")]
            if len(values) == len(col_names):
                table_parsed.append({k: v for k, v in zip(col_names, values)})
        port_info = port_info.append(table_parsed, ignore_index=True)
    return port_info


# receive data by alexa.com and process infromation to remove extra characters
def parse_alexa_site_info():
    URL_a = "https://www.alexa.com/topsites"
    page_a = requests.get(URL_a)
    soup_a = BeautifulSoup(page_a.content, "html.parser")
    info_list = []
    return_list = []
    site_info = "/siteinfo/"
    soup_finder = soup_a.find_all("a", href=True)
    for each_info in soup_finder:
        info_list.append(each_info["href"])
    for each_item in info_list:
        if site_info in each_item:
            each_item = each_item.replace(site_info, "")
            return_list.append(each_item)
    return return_list


# receive data by moz.com and process information to remove extra characters
def parse_moz_top_sites():
    URL_m = "https://moz.com/top500"
    page_m = requests.get(URL_m)
    soup_m = BeautifulSoup(page_m.content, "html.parser")
    https = "https"
    www = "www"
    http = "http"
    moz = "moz"

    urls = []
    return_list = []
    links_finder = soup_m.find_all("a", href=True)
    for link in links_finder:
        urls.append(link["href"])

    for url in urls:

        has_http = http in url
        is_an_external_link = moz not in url
        has_https = https in url
        has_www_prefix = www in url
        looks_like_a_website = (has_http or has_https) and has_www_prefix

        if looks_like_a_website and is_an_external_link:
            url = url.replace(https + "://", "")
            url = url.replace(http + "://", "")
            url = url.replace(www + ".", "")
            return_list.append(url)
    return return_list


# sort and eliminate duplicates on my recovered lists
def uniq_sort_list():
    all_urls = []
    for url in parse_moz_top_sites():
        all_urls.append(url)
    for url in parse_alexa_site_info():
        all_urls.append(url)
    all_urls = sorted(set(all_urls))
    return all_urls

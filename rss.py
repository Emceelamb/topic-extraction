import feedparser
import pprint
from urllib.parse import urlsplit, urlunsplit
import requests
from bs4 import BeautifulSoup
from topic_extraction import sanitize_text, get_topics


pp = pprint.PrettyPrinter(indent=4)

url = "https://fetchrss.com/rss/6508da2a6f4dc52d890085e26508d97829ab1e4f05782d42.xml"


def get_feed(url):
    rss = feedparser.parse(url)
    return {"agency": rss.feed.title, "articles": rss.entries}


def get_url(url):
    split_url = urlsplit(url[0].href)
    query = split_url.query.split("    ")
    joined_url = split_url.scheme + "://" + split_url.netloc + query[1]
    return joined_url


def scrape_page(page):
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find(role="article").text
    content = content.replace("\n", "")
    return content


"""
url = get_url(feed.entries[0].links)
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
content = soup.find(role="article").text
"""

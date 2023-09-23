import pprint
import requests
from rss import get_feed, get_url, scrape_page
from topic_extraction import get_topics, sanitize_text

pp = pprint.PrettyPrinter(indent=4)


def main():
    url = "https://fetchrss.com/rss/6508da2a6f4dc52d890085e26508d97829ab1e4f05782d42.xml"
    feed = get_feed(url)
    articles = []

    for document in feed["articles"]:
        link = get_url(document.links)
        article = {"title": document["title"], "link": link, "agency": feed["agency"]}
        articles.append(article)


    for article in articles:
        page = requests.get(article["link"])
        content = scrape_page(page)
        tokens = sanitize_text(content)
        topics = get_topics(tokens)
        article["topics"] = topics

    for a in articles:
        article = {
                "title": a["title"],
                "agency": a["agency"],

        }
    pp.pprint(articles)

# tokens = sanitize_text(content)
# topics = get_topics(tokens)


# pp.pprint(topics)

main()

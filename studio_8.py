import requests
import time
from bs4 import BeautifulSoup as bs
from collections import Counter


class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags



def main():
    url = "https://quotes.toscrape.com"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")

    # scrape_quotes(soup)
    quotes = []
    while True:
        time.sleep(1)
        relative_url = get_next_url(soup)
        if relative_url is None:
            break
        next_page = url + relative_url

        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))
    
    get_shortest_and_longest(quotes)
    print(top_ten_tags(quotes))
    print("-----------------------")
    print(authors_by_quote(quotes))
    return

def authors_by_quote(quotes):
    author_quotes = []
    for quote in quotes:
        author_quotes.append(quote.author)
    author_quotes_count = Counter(author_quotes)
    multiple_instances = []
    for item, count in author_quotes_count.items():
        if count > 1:
            multiple_instances.append((item, count))

    multiple_instances.sort(key=lambda x: x[1], reverse=True)
    return multiple_instances



def top_ten_tags(quotes):
    all_tags = []
    for quote in quotes:
        all_tags.extend(quote.tags)
    counts = Counter(all_tags)
    top_ten = counts.most_common(10)
    return top_ten




def get_shortest_and_longest(quotes):
    longest = 0
    shortest = 100000

    longest_quote = ""
    shortest_quote = ""

    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longest_quote = quote.text

        if len(quote.text)< shortest:
            shortest = len(quote.text)
            shortest_quote = quote.text

    print(longest_quote, longest)
    print("--------------------------------------")
    print(shortest_quote, shortest)
    print("--------------------------------------")
    return

def get_next_url(soup: bs):
    list_item = soup.find("li", {"class": "next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    url = anchor["href"]

    return url

def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})
    all_quotes = []
    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        tags = quote.find_all("a", {"class": "tag"})
        
        tags_text = []

        for tag in tags:
            tags_text.append(tag.get_text(strip=True))
        
        single_quote = Quote(text, author, tags_text)
        
        all_quotes.append(single_quote)
    return all_quotes










if __name__ == "__main__":
    main()
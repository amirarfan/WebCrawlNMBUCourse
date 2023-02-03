import requests
from bs4 import BeautifulSoup


def web_crawl(base_url, max_depth=1, max_pages=1):
    """
    Crawl the website and return all the text from the page and sub-pages
    """
    text = ""
    for page_number in range(1, max_pages + 1):
        url = f"{base_url}?page={page_number}"
        try:
            page = requests.get(url)
        except Exception as e:
            print(e)
            break
        soup = BeautifulSoup(page.content, "html.parser")
        texts = soup.findAll(text=True)
        text += " ".join(t.strip() for t in texts)

        if max_depth > 0:
            links = [
                link.get("href") for link in soup.find_all("a", href=True)
            ]
            for link in links:
                if "/course/" in link:
                    link = f"https://www.nmbu.no{link}"
                    print(link)
                    try:
                        text += web_crawl(link, max_depth - 1)
                    except Exception as e:
                        print(e)
                        break
    return text


if __name__ == "__main__":
    # Crawl the website
    url = "https://www.nmbu.no/courses"

    crawled_text = web_crawl(url, max_depth=1, max_pages=20)

    # Save crawled text to a text file
    with open("crawled_text.txt", "w", encoding="utf-8") as f:
        f.write(crawled_text)

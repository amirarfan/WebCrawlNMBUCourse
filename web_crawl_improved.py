import requests
from bs4 import BeautifulSoup


def web_crawl(base_url, max_depth=1, max_pages=1):
    """
    Crawl the website and return all the text from the page and sub-pages
    """
    text = ""
    for page_number in range(0, max_pages):

        if page_number == 0:
            url = base_url
        else:
            url = f"{base_url}&page={page_number}"
        try:
            page = requests.get(url)
        except Exception as e:
            print(e)
            break
        soup = BeautifulSoup(page.content, "html.parser")

        if max_depth > 0:
            links = [
                link.get("href") for link in soup.find_all("a", href=True)
            ]
            for link in links:
                if "/course/" in link:
                    link = f"https://www.nmbu.no{link}"
                    print(link)
                    soup_course = BeautifulSoup(
                        requests.get(link).text, "html.parser"
                    )
                    h1_text = (
                        soup_course.find(class_="view-header")
                        .findNext("h1")
                        .text
                    )
                    # Extract text from elements with class "views-field views-field-markup-2"
                    class_2 = soup_course.find(
                        class_="views-field views-field-markup-2"
                    )

                    if class_2:
                        class_2_text = class_2.text
                    else:
                        class_2_text = ""
                    # Extract text from elements with class "views-field views-field-markup-3"
                    class_3 = soup_course.find(
                        class_="views-field views-field-markup-3"
                    )

                    if class_3:
                        class_3_text = class_3.text
                    else:
                        class_3_text = ""

                    detail_panel = soup_course.find(
                        class_="panel-col-last panel-panel"
                    )
                    if detail_panel:
                        details = detail_panel.text.strip().replace("\n", " ")
                    else:
                        details = ""

                    course_txt = (
                        f"Course Title: {h1_text}"
                        + class_2_text
                        + class_3_text
                        + details
                    )

                    text += course_txt + "\n\n"
    return text


if __name__ == "__main__":

    url = "https://www.nmbu.no/courses?text=&emnekode=&text_7=&text_3=4&text_4=All&text_6=All&text_5=All&text_2=All&numeric="

    crawled_text = web_crawl(url, max_depth=1, max_pages=5)

    with open("crawled_text_RealTek_Prompt.txt", "w", encoding="utf-8") as f:
        f.write(crawled_text)

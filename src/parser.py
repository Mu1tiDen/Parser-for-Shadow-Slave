import requests
from docx import Document
from bs4 import BeautifulSoup

def find_next_link(soup):
    links = soup.find_all("a", href=True)
    for link in links:
        if link.text in "Следующая глава":
            with open("data/link.txt", 'w') as file:
                file.write(f'https://telegra.ph{link.get('href')}')
                #https://telegra.ph/Glava-2324-Hod-protivnika-05-13
            print("New link successfully write!")
            break
    return "NONE"
def put_chapter_in_file():
    with open("data/link.txt") as file:
        url = file.read()

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"
    }
    req = requests.get(url, headers=headers)
    src = req.text

    with open("data/index.html", "w") as file:
        file.write(src)
    with open("data/index.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    chap_title = soup.find(class_="tl_article_content").find("h1")
    chap_text = soup.find(class_="tl_article_content").find_all("p")

find_next_link(soup)
"""print(chap_title.text.upper(),'\n')

for text_line in chap_text:
    filtered_line = text_line.text
    if filtered_line != '\n' and filtered_line not in "Предыдущая глава Следующая глава":
        print(filtered_line)"""



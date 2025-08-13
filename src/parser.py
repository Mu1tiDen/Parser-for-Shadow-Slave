import requests
import os
from docx import Document
from bs4 import BeautifulSoup



def find_next_link(soup_):
    links = soup_.find_all("a", href=True)

    for link in links:
        if link.text in "Следующая глава":
            with open("data/link.txt", 'w') as file:
                file.write(f'https://telegra.ph{link.get('href')}')
                #https://telegra.ph/Glava-2324-Hod-protivnika-05-13
            print("New link successfully write!")
            return False

    return True


def put_chapter_in_file():
    if not os.path.exists("data/link.txt"):
        with open("data/link.txt", 'w') as file:
            file.write("https://telegra.ph/Glava-989-Padenie-Falkon-Skotta-7-06-23")

    with open("data/link.txt") as file:
        url = file.read()

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"
    }

    req = requests.get(url, headers=headers)
    src = req.text

    with open("data/index.html", "w") as file:
        file.write(src)

    soup = BeautifulSoup(src, "lxml")

    chapter_title = soup.find(class_="tl_article_content").find("h1")
    chapter_text = soup.find(class_="tl_article_content").find_all("p")

    with open("data/test.txt", "a") as file:
        file.write(f'{chapter_title.text.upper()}\n')
        for text_line in chapter_text:
            filtered_line = text_line.text
            if filtered_line != '\n' and filtered_line not in "Предыдущая глава Следующая глава":
                file.write(f'{filtered_line}\n')
        file.write('\n')

        print(f'"{chapter_title.text}" recorded successfully!\n')

    if os.path.exists("data/test.docx"): document = Document("data/test.docx")
    else: document = Document()

    title = document.add_heading(chapter_title.text, 1)
    title.bold = True

    for text_line in chapter_text:
        filtered_line = text_line.text
        if filtered_line != '\n' and filtered_line not in "Предыдущая глава Следующая глава":
            document.add_paragraph(filtered_line, style="No Spacing")

    document.save("data/test.docx")


    return soup

while True:
    soup = put_chapter_in_file()
    if find_next_link(soup):
        print('popa')
        break


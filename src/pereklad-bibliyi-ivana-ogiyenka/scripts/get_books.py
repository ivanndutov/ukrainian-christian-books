from bs4 import BeautifulSoup
import requests

url = "https://bibleonline.ru/bible/ubio/"

# Accessing main html
html = requests.get(url).content
mainSoup = BeautifulSoup(html, 'html.parser')

# Getting all book name conventions along with number of chapters in each
spans = mainSoup.find_all("span")
with_book_parameter = [span.get("book") for span in spans]

bible_books = {}
for i in range(len(spans)):
    if with_book_parameter[i] is None:
        continue
    # TODO implement retrieving of ukrainian names of conventions
    bible_books[with_book_parameter[i]] = int(spans[i].text)

# Getting link for each book
bible_books_links = [url + book for book in bible_books.keys()]

def load_chapter(chapter_url: str) -> str:
    """
    Loads chapter from book url on https://bibleonline.ru/bible/ubio/
    """
    chapter_html = requests.get(chapter_url).content
    chapter_soup = BeautifulSoup(chapter_html, 'html.parser')
    verses_html = chapter_soup.select('[vers]')
    verses = []
    for verse_html in verses_html:
        verse = verse_html.get("vers") + ". " + verse_html.text
        verses.append(verse)
    return verses

# Getting pure chapter content
bible_books_conventions = {}
def get_bible(bible_file: str, bible_books, bible_books_conventions):
    # TODO implement adding heading as conventions
    with open(bible_file, "a", encoding="utf-8") as file:
        for book in list(bible_books.keys()):
            file.write(book + "\n\n")
            for i in range(bible_books[book]):
                chapter_url = f"{url}{book}-{i + 1}"
                chapter = ' '.join(load_chapter(chapter_url))
                file.write(chapter + "\n")
print(list(bible_books.keys()))

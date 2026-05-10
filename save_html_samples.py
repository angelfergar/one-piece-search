import os
from base.web_factory import WebDriverFactory
from webs.manga_plus import MangaPlus

web_directory = "tests/integration/samples"

def get_latest_chapter():
    driver = WebDriverFactory.get_webdriver("https://mangaplus.shueisha.co.jp/titles/200016")
    try:
        page = MangaPlus(driver)
        past_chapter = page.find_chapter() - 1
        return str(past_chapter)
    finally:
        driver.quit()
def create_webs(chapter):
    return {
        "manga_plus": "https://mangaplus.shueisha.co.jp/titles/200016",
        "read_onepiece": "https://ww01.readonepiece.cc/",
        "opscans_found": f"https://opchapters.com/op-chapter-{chapter}/",
        "opscans_not_found": "https://opchapters.com/op-chapter-2000/",
        "tcbop": "https://tcbonepiecechapters.com/mangas/5/one-piece",
        "animeallstar": "https://animeallstar30.com/category/one-piece/"
    }

def capture_web():
    os.makedirs(web_directory, exist_ok=True)

    chapter = get_latest_chapter()
    for name, url in create_webs(chapter).items():
        driver = WebDriverFactory.get_webdriver(url)

        try:
            html = driver.page_source
            filepath = os.path.join(web_directory, f"{name}.html")
            with open(filepath, "w") as f:
                f.write(html)
        except Exception as e:
            print(f"Error with {name}: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    capture_web()
from web_config import WebConfig
from webs.opscans import OpScans
from webs.tcb_scans import TcbScans
import utilities.custom_logger as cl
import logging

log = cl.custom_logger(logging.INFO)

chapter_file = "chapter.txt"  # archivo donde guardaremos el número actual

def get_last_chapter():
    with open(chapter_file, "r") as file:
        return file.read().strip()

def establish_next_chapter(next_chapter):
    with open(chapter_file, "w") as file:
        file.write(str(next_chapter))

if __name__ == "__main__":

    wc = WebConfig()
    webs = ["https://opchapters.com/op-chapter-{chapter}",
            "https://tcbscansonepiece.com/one-piece-chapter-{chapter}-manga/"]
    chapter = get_last_chapter()
    webs_available = []

    for web in webs:
        url = web.format(chapter=chapter)
        driver = wc.set_up(url)
        try:
            if "opchapters" in url:
                page = OpScans(driver)
            elif "tcbscans" in url:
                page = TcbScans(driver)
            else:
                print(f"{url} is not supported")
                driver.quit()
                continue

            images = page.get_chapter_images()

            if images:
                webs_available.append(f"Chapter {chapter} is already available in: {url}")
            else:
                log.error(f"NOT LUCKY: Chapter {chapter} NOT available in: {url}")

        except Exception as e:
            log.error(f"Error while checking {url}: {e}")

        finally:
            driver.quit()

    if webs_available:
        print(f"CHAPTER {chapter} IS ALREADY OUT!! Here are the webs where you can read it.")
        for web in webs_available:
            print(web)
            log.critical(web)
        next_chapter = str(int(chapter) + 1)
        establish_next_chapter(next_chapter)
        log.info(f"Next chapter will be: {next_chapter}")
    else:
        log.error(f"Chapter {chapter} is not available in any web yet. We will keep searching for the One Piece")


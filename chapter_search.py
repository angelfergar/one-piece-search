from web_config import WebConfig
from webs.opscans import OpScans
from webs.tcb_scans import TcbScans
from webs.tcb_op import TcbOp
from webs.read_onepiece import ReadOnePiece
from webs.anime_allstar import AllStar
from webs.manga_plus import MangaPlus
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from utils.db_management import init_db, check_chapter_found, save_chapter, save_links, get_all_subscribers, add_subscriber
from concurrent.futures import ThreadPoolExecutor, as_completed
from info_api import get_op_fact

init_db()

# For new mails
'''
    add_subscriber(email)
'''

# Websites configuration
web_config = [
    {"url": "https://opchapters.com/op-chapter-{chapter}", "clss": OpScans, "web_name": "OP Scans"},
    {"url": "https://opchapters.com/op-{chapter}", "clss": OpScans, "web_name": "OP Scans"},
    # {"url": "https://ww1.tcbscansonepiece.com/one-piece-manga", "clss": TcbScans, "web_name": "TCB Scans"},
    {"url": "https://tcbonepiecechapters.com/mangas/5/one-piece", "clss": TcbOp, "web_name": "TCB One Piece"},
    {"url": "https://readonepiece.cc/", "clss": ReadOnePiece, "web_name": "Read One Piece"},
    {"url": "https://animeallstar30.com/category/one-piece/", "clss": AllStar, "web_name": "Anime All Star"}
]

mangaplus_url = "https://mangaplus.shueisha.co.jp/titles/100020"

# Email config
sender_email = os.environ.get("smtp_user", "anfernagar@gmail.com")
password = os.environ.get("smtp_pass")
receiver_emails = get_all_subscribers()
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Check current week
def current_week():
    today = date.today()
    year, week, _ = today.isocalendar()
    return f'W{week}'

# Check if we already found the chapter this week
def check_week():
    if check_chapter_found(current_week()):
        print(f"Chapter already found this week")
        sys.exit(0)

# Check MangaPlus for release date and chapter number
def get_mangaplus_info():
    wc = WebConfig()
    driver = wc.set_up(mangaplus_url)
    try:
        page = MangaPlus(driver)
        is_break = page.find_break_week() != current_week()
        chapter = str(page.find_chapter())
        week_number = int(page.find_break_week().split("W")[1])
        current_number = int(current_week().split("W")[1])
        weeks_wait = week_number - current_number
        return {"is_break": is_break, "chapter": chapter, "wait": weeks_wait}
    finally:
        driver.quit()

# Email information
def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(
                sender_email,
                receiver_emails,
                message.as_string()
            )
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_found_email(chapter, webs_available):
    subject = f"New One Piece Chapter {chapter} Available!"
    body = f"Chapter {chapter} is now available!\n\nYou can read it on:\n"
    for web in webs_available:
        body += f"{web['name']}: {web['url']}\n\n"
        body += get_op_fact()
    send_email(subject, body)

def send_break_email(weeks):
    subject = "No chapter this week :("
    body = ""
    if weeks > 1:
        body = f"Oda is resting this week, we'll continue searching the One Piece after a {weeks} weeks break.\n\n"
    elif weeks == 1:
        body = f"Oda is resting this week, we'll continue searching the One Piece after a {weeks} week break.\n\n"
    else:
        print(f"The number of weeks is not possible: {weeks}")

    body += get_op_fact()
    send_email(subject, body)

# Main logic
if __name__ == "__main__":

    check_week()

    mangaplus_info = get_mangaplus_info()

    if mangaplus_info["is_break"]:
        send_break_email(mangaplus_info["wait"])
        save_chapter(None, current_week())
        sys.exit(0)

    chapter = mangaplus_info["chapter"]
    webs_available = []

    def check_webs(web, chapter):
        url = web["url"].format(chapter=chapter)
        wc = WebConfig()
        driver = wc.set_up(url)
        try:
            page = web["clss"](driver)
            found = page.get_chapter_images(chapter)
            if found:
                return {"name": web["web_name"], "url": url}
            else:
                print(f"NOT LUCKY: Chapter {chapter} NOT available in: {url}")
                return None
        except Exception as e:
            print(f"Error while checking {url}: {e}")
            return None
        finally:
            driver.quit()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_webs, web, chapter): web for web in web_config}
        for future in as_completed(futures):
            result = future.result()
            if result:
                webs_available.append(result)

    if webs_available:
        print(f"CHAPTER {chapter} IS ALREADY OUT!! Here are the webs where you can read it.")
        for web in webs_available:
            print(web)

        send_found_email(chapter, webs_available)

        next_chapter = str(int(chapter) + 1)
        print(f"Next chapter will be: {next_chapter}")

        chapter_id = save_chapter(chapter, current_week())
        save_links(chapter_id, webs_available)

    else:
        print(f"Chapter {chapter} is not available in any web yet. We will keep searching for the One Piece")

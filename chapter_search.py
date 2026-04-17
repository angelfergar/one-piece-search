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


for email in os.environ.get("op_receivers", "").split(","):
    add_subscriber(email)

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

# Check if we're on a break week
def is_break_week():
    wc = WebConfig()
    break_url = "https://mangaplus.shueisha.co.jp/titles/100020"
    driver_extra = wc.set_up(break_url)
    release_page = MangaPlus(driver_extra)
    release_week = release_page.find_break_week()
    driver_extra.quit()

    if release_week != current_week():
        return True
    else:
        return False

def get_last_chapter():
    wc = WebConfig()
    break_url = "https://mangaplus.shueisha.co.jp/titles/100020"
    driver_extra = wc.set_up(break_url)
    release_page = MangaPlus(driver_extra)
    release_chapter = release_page.find_chapter()
    driver_extra.quit()

    return str(release_chapter)

# Email config
sender_email = os.environ.get("smtp_user", "anfernagar@gmail.com")
password = os.environ.get("smtp_pass")
receiver_emails = get_all_subscribers()
smtp_server = "smtp.gmail.com"
smtp_port = 587

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
        body += f"{web['name']}: {web['url']}\n"
    body += (f"La actualización de Windows rompió mi Firefox, y de regalo el job de Jenkins. Disculpen.\nHe aprovechado y he metido que el número del capítulo"
             f"se saque de forma dinámica y he refactorizado el vaineo.\nBesis!")

    send_email(subject, body)

def send_break_email():
    subject = "No chapter this week :("
    body = "Oda is resting this week, we'll continue searching the One Piece after the break."

    send_email(subject, body)

if __name__ == "__main__":

    check_week()

    if is_break_week():
        print("We're on a break week")
        send_break_email()
        sys.exit(0)

    wc = WebConfig()
    webs = ["https://opchapters.com/op-chapter-{chapter}",
            "https://opchapters.com/op-{chapter}",
            "https://ww1.tcbscansonepiece.com/one-piece-manga",
            "https://tcbonepiecechapters.com/mangas/5/one-piece",
            "https://readonepiece.cc/",
            "https://animeallstar30.com/category/one-piece/"]
    chapter = get_last_chapter()
    webs_available = []

    for web in webs:
        url = web.format(chapter=chapter)
        driver = wc.set_up(url)
        try:
            if "opchapters" in url:
                page = OpScans(driver)
                web_name = "OP Scans"
            elif "tcbscans" in url:
                page = TcbScans(driver)
                web_name = "TCB Scans"
            elif "tcbonepiece" in url:
                page = TcbOp(driver)
                web_name = "TCB One Piece"
            elif "readonepiece" in url:
                page = ReadOnePiece(driver)
                web_name = "Read One Piece"
            elif "animeallstar" in url:
                page = AllStar(driver)
                web_name = "Anime All Star"
            else:
                print(f"{url} is not supported")
                driver.quit()
                continue

            images = page.get_chapter_images(chapter)

            if images:
                webs_available.append({"name": web_name, "url": url})
            else:
                print(f"NOT LUCKY: Chapter {chapter} NOT available in: {url}")

        except Exception as e:
            print(f"Error while checking {url}: {e}")

        finally:
            driver.quit()

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

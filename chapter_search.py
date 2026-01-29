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

chapter_file = "chapter.txt"
week_file = "found_week.txt"
release_file = "release_week.txt"


# Check current week
def current_week():
    today = date.today()
    year, week, _ = today.isocalendar()
    return f'W{week}'


# Check if we already found the chapter this week
def check_week():
    if not os.path.exists(week_file):
        return None

    with open(week_file, "r") as file:
        saved_week = file.read().strip()

    if saved_week == current_week():
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

    # Write the break week info
    if not os.path.exists(release_file):
        with open(release_file, "w") as file:
            file.write(release_week)

    with open(release_file, "r") as file:
        release_info = file.read().strip()

    if release_info != release_week:
        with open(release_file, "w") as file:
            file.write(release_week)
            release_info = release_week

    if release_info != current_week():
        return True
    else:
        return False

# Email config
sender_email = os.environ.get("smtp_user", "anfernagar@gmail.com")
password = os.environ.get("smtp_pass")
raw_receivers = os.environ.get("op_receivers", "")
receiver_emails = [r.strip() for r in raw_receivers.split(",") if r.strip()]
smtp_server = "smtp.gmail.com"
smtp_port = 587


def get_last_chapter():
    if not os.path.exists(chapter_file):
        with open(chapter_file, "w") as file:
            file.write("1170")
        return "1170"
    with open(chapter_file, "r") as file:
        return file.read().strip()


def establish_next_chapter(next_chapter):
    with open(chapter_file, "w") as file:
        file.write(str(next_chapter))

def send_email(subject, body):

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = "OP Fans"
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
        with open(week_file, "w") as file:
            file.write(current_week())
        sys.exit(0)

    wc = WebConfig()
    webs = ["https://animeallstar30.com/category/one-piece/"]
    '''
    webs = ["https://opchapters.com/op-chapter-{chapter}",
            "https://opchapters.com/op-{chapter}",
            "https://ww1.tcbscansonepiece.com/one-piece-manga",
            "https://tcbonepiecechapters.com/mangas/5/one-piece",
            "https://readonepiece.cc/",
            "https://animeallstar30.com/category/one-piece/"]
            '''
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
        establish_next_chapter(next_chapter)
        print(f"Next chapter will be: {next_chapter}")

        with open(week_file, "w") as file:
            file.write(current_week())
    else:
        print(f"Chapter {chapter} is not available in any web yet. We will keep searching for the One Piece")

from web_config import WebConfig
from webs.opscans import OpScans
from webs.tcb_scans import TcbScans
import utilities.custom_logger as cl
import logging
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log = cl.custom_logger(logging.INFO)

chapter_file = "chapter.txt"

# Email config
sender_email = os.environ.get("smtp_user", "anfernagar@gmail.com")
password = os.environ.get("smtp_pass")
receiver_email = "anfernagar@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def get_last_chapter():
    if not os.path.exists(chapter_file):
        with open(chapter_file, "w") as file:
            file.write("1165")
        return "1165"
    with open(chapter_file, "r") as file:
        return file.read().strip()

def establish_next_chapter(next_chapter):
    with open(chapter_file, "w") as file:
        file.write(str(next_chapter))

def send_email(chapter, webs_available):
    subject = f"New One Piece Chapter {chapter} Available!"
    body = f"Chapter {chapter} is now available!\n\nYou can read it on:\n"
    for web in webs_available:
        body += f"{web}\n"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        log.info(f"Email sent successfully for chapter {chapter}!")
    except Exception as e:
        log.error(f"Failed to send email: {e}")

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
                webs_available.append(url)
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

        send_email(chapter, webs_available)

        next_chapter = str(int(chapter) + 1)
        establish_next_chapter(next_chapter)
        log.info(f"Next chapter will be: {next_chapter}")
    else:
        log.error(f"Chapter {chapter} is not available in any web yet. We will keep searching for the One Piece")


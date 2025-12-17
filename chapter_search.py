from web_config import WebConfig
from webs.opscans import OpScans
from webs.tcb_scans import TcbScans
from webs.tcb_op import TcbOp
from webs.read_onepiece import ReadOnePiece
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

chapter_file = "chapter.txt"

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
            file.write("1169")
        return "1169"
    with open(chapter_file, "r") as file:
        return file.read().strip()


def establish_next_chapter(next_chapter):
    with open(chapter_file, "w") as file:
        file.write(str(next_chapter))


def send_email(chapter, webs_available):
    subject = f"New One Piece Chapter {chapter} Available!"
    body = f"Chapter {chapter} is now available!\n\nYou can read it on:\n"
    for web in webs_available:
        body += f"{web["name"]}: {web["url"]}\n"

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
        print(f"Email sent successfully for chapter {chapter}!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":

    wc = WebConfig()
    webs = ["https://opchapters.com/op-chapter-{chapter}",
            "https://opchapters.com/op-{chapter}",
            "https://ww1.tcbscansonepiece.com/one-piece-manga",
            "https://tcbonepiecechapters.com/mangas/5/one-piece",
            "https://readonepiece.cc/"]

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

        send_email(chapter, webs_available)

        next_chapter = str(int(chapter) + 1)
        establish_next_chapter(next_chapter)
        print(f"Next chapter will be: {next_chapter}")
    else:
        print(f"Chapter {chapter} is not available in any web yet. We will keep searching for the One Piece")

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
base_url = "https://onepiece-unsubscribe.onrender.com"

# Email config
sender_email = os.environ.get("smtp_user", "theeternalpose@gmail.com")
password = os.environ.get("smtp_pass")
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
def generate_unsubscribe_links(base_url):
    links = {}

    for email, token in get_all_subscribers():
        links[email] = f"{base_url}/unsubscribe?token={token}"

    return links

def send_email(subject, body, receiver):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(
                sender_email,
                receiver,
                message.as_string()
            )
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_found_email(chapter, webs_available):
    subject = f"Capítulo {chapter} de One Piece disponible!"
    webs_html = ""
    fact = get_op_fact()

    for web in webs_available:
        webs_html += f"""
                <li style="margin: 10px 0;">
                    <a href="{web['url']}" style="color: #ffffff; background-color: #f5a623; 
                    padding: 8px 15px; border-radius: 5px; text-decoration: none;">
                        {web['name']}
                    </a>
                </li>
                """

    unsubscribe_link = generate_unsubscribe_links(base_url)
    for email, link in unsubscribe_link.items():
        body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #1a1a2e; color: #ffffff; padding: 20px;">

                <div style="max-width: 600px; margin: auto; background-color: #16213e; border-radius: 10px; padding: 30px;">

                    <h1 style="color: #f5a623; text-align: center;">The Eternal Pose</h1>
                        <hr style="border-color: #f5a623;">

                    <h3 style="color: #f5a623;">Puedes leer el capítulo en:</h3>
                        <ul style="list-style: none; padding: 0;">
                            {webs_html}
                        </ul>

                    <div style="background-color: #0f3460; border-left: 4px solid #f5a623; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <h3 style="color: #f5a623; margin-top: 0;">¿Sabías que...?</h3>
                            <p style="font-size: 14px; line-height: 1.6;">{fact}</p>
                    </div>

                    <p style="text-align: center; margin-top: 30px; font-size: 12px; color: #888888;">
                            ¿Ya no quieres buscar el One Piece?
                            <a href="{link}" style="color: #f5a623;">Darte de baja</a>
                    </p>
                </div>
            </body>
            </html>
            """
        send_email(subject, body, receiver=email)

def send_break_email():
    subject = "No hay capítulo esta semana :("
    fact = get_op_fact()

    unsubscribe_link = generate_unsubscribe_links(base_url)
    for email, link in unsubscribe_link.items():
        body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #1a1a2e; color: #ffffff; padding: 20px;">

                <div style="max-width: 600px; margin: auto; background-color: #16213e; border-radius: 10px; padding: 30px;">
                
                    <h1 style="color: #f5a623; text-align: center;">The Eternal Pose</h1>
                        <hr style="border-color: #f5a623;">
                    
                    <h3 style="color: #f5a623;">Oda está descansando esta semana. Volveremos la semana que viene</h3>
                    
                    <div style="background-color: #0f3460; border-left: 4px solid #f5a623; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <h3 style="color: #f5a623; margin-top: 0;">¿Sabías que...?</h3>
                            <p style="font-size: 14px; line-height: 1.6;">{fact}</p>
                    </div>
                    
                    <p style="text-align: center; margin-top: 30px; font-size: 12px; color: #888888;">
                            ¿Ya no quieres buscar el One Piece?
                            <a href="{link}" style="color: #f5a623;">Darte de baja</a>
                    </p>
                    </div>
            </body>
            </html>
        """
        send_email(subject, body, receiver=email)

# Main logic
if __name__ == "__main__":

    check_week()

    mangaplus_info = get_mangaplus_info()

    if mangaplus_info["is_break"]:
        send_break_email()
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

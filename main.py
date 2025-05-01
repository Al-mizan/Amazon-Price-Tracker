import os
import smtplib
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart

load_dotenv()
email = os.getenv("my_email")
app_password = os.getenv("my_email_app_password")

url = "https://www.amazon.com/ASUS-Display-NVIDIA%C2%AE-i7-13650HX-G614JV-AS74/dp/B0CRDCXRK2/ref=sr_1_1?_encoding=UTF8&sr=8-1"
headers = {
    "Host": "www.amazon.com",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "sec-gpc": "1",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "priority": "u=0, i",
    "x-forwarded-proto": "https",
    "x-https": "on",
    "X-Forwarded-For": "103.122.142.231"
}
response = requests.get(url=url, headers = headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
price = soup.find("span", {"class": "aok-offscreen"}).get_text()
title = soup.find("span", {"class": "a-size-large product-title-word-break"}).get_text()

price = price.split()[0][1::]
price_of_the_product:float = float(price.replace(",", ""))
title_of_the_product:str = title.strip()

print(price_of_the_product)
print(title_of_the_product)

if price_of_the_product <= 1150:
    announcement = f"{title_of_the_product} is now ${price_of_the_product}\n"
    announcement += f"{url}"
    sender_email = email
    sender_password = app_password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = email
    message["To"] = email
    message["Subject"] = "🎉 Exclusive Offer – Claim Before It's Gone!"
    message.attach(MIMEText(announcement, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, app_password)
            server.sendmail(email, email, message.as_string())
        print(f"Email successfully sent to {email}!")
    except Exception as e:
        print(f"Error sending email: {e}")
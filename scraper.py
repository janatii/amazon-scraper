import requests
import smtplib
import time
from bs4 import BeautifulSoup

URL = 'https://www.amazon.co.uk/dp/B087PZHJ63/ref=gw_uk_desk_mso_vicc_owlck_bundle_0520?pf_rd_r=DWJV5E2CRD16VG6W52GS&pf_rd_p=7d59ab7d-aaec-4d00-9d09-30be11790382'
target_price = 1700
headers = {"User-Agent": "curl/7.49.0"}


def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("span", {"id": "productTitle"}).get_text()

    def get_price_tag():
        return soup.find("span", {"id": "priceblock_ourprice"}).get_text()

    for i in range(0, 100):
        while True:
            try:
                price = get_price_tag()
            except AttributeError:
                continue
            break

    converted_price = float(price[1:])

    if converted_price < target_price:
        send_mail(title)


def send_mail(title):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('email@gmail.com', 'app_password')
    subject = 'Price fell down!%s' % title
    body = 'check the amazon link %s' % URL
    msg = f"Subject: {subject}\n\n{body}"
    # you can send it to yourself
    server.sendmail(
        'email@gmail.com',
        'email@gmail.com',
        msg
    )
    print('Hey mail has been sent!')
    server.close()


while True:
    # check_price once a day
    check_price()
    time.sleep(60 * 3600)

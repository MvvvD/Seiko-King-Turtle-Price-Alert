import unidecode
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client

TARGET_PRICE = 2000

HEADERS = {
    'User-Agent': 'Get it here'}  # http://myhttpheader.com

account_sid = 'redacted'
auth_token = 'redacted'
phone_number = "+48redacted"

# scrapping with soup

# store1
url = 'https://zegarownia.pl/zegarek-meski-seiko-prospex-king-turtle-diver-automatic-srpe03k1'
r = requests.get(url, headers=HEADERS).text
soup = BeautifulSoup(r, 'lxml')
price_tag = unidecode.unidecode(soup.find(class_="price-container price-final_price tax weee").text.strip())
price_tag = int(price_tag[0:-6].replace(" ", ""))
print(price_tag)

# store2
url = 'https://www.timetrend.pl/si-srpe03k1.html'
r = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(r.content, 'lxml')
price_tag2 = unidecode.unidecode(soup.find(name='span', class_="price").text)
price_tag2 = int(price_tag2[0:-6].replace(" ", ""))
print(price_tag2)

# store3
url = 'https://dolinski.pl/seiko-prospex-diver-king-turtle-srpe03k1/'
r = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(r.content, 'lxml')
price_tag3 = int(unidecode.unidecode(soup.find(name='span', class_="ty-price-num").text))
print(price_tag3)

# Twilio stuff
lowest_price = min([price_tag, price_tag2, price_tag3])
if TARGET_PRICE <= lowest_price:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid='redacted',
        body=f'Seiko king turtle: {lowest_price}',
        to=phone_number
    )

# coding=utf-8

from datetime import datetime
import requests
from lxml import html
import mysql.connector

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

# 특정년도, 월에 대한 날씨 정보 조회
def getOilprice():
    Oilprice = { 'Date' : '', 'Oil':'','Diesel':""}

    url = "http://www.opinet.co.kr/user/main/mainView.do"
    resp = requests.get(url)
    resp.encoding = 'utf8'
    text = resp.text
    elem = html.fromstring(text)
    articles = elem.cssselect('div.m_oilinfo_tab')

    for a in articles:
        dd =  datetime.today().strftime("%Y%m%d")
        oil_p = a.cssselect('div.b_inner p.pdt_6 span')[0].text_content().strip()
        diesel_p = a.cssselect('div.box_inner')[1].cssselect('span.price2')[0].text_content().strip()
    Oilprice = { 'date' : dd  , 'gasoline':oil_p,'diesel':diesel_p}
    return (Oilprice)


##실시간 ----------------------------------------------------------------------------------------------------------------------

Oilprice = getOilprice()

cnx = mysql.connector.connect(user='ID', password='PASSWORD',
                              host='URL',
                              database='DB')
cursor = cnx.cursor()

add_oli_price = ("INSERT INTO TB_CR_OIL_PRICE "
               "(date, gasoline, diesel) "
               "VALUES (%s, %s, %s) "
               "ON DUPLICATE KEY UPDATE date=%s, gasoline=%s, diesel=%s")

data_oli_price = (Oilprice.get("date"), Oilprice.get("gasoline"), Oilprice.get("diesel"),
                  Oilprice.get("date"), Oilprice.get("gasoline"), Oilprice.get("diesel"))

cursor.execute(add_oli_price, data_oli_price)

cnx.commit()

cursor.close()
cnx.close()


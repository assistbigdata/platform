# coding=utf-8

from datetime import datetime
import requests
from lxml import html
import mysql.connector


##함수 ----------------------------------------------------------------------------------------------------------------------

def left(s, amount):
    return s[:amount]

def Kospi_real():
    Kospi_ = { 'Date' : '', 'Kospi':'' }

    url = "http://finance.naver.com/sise/sise_index.nhn?code=KOSPI"
    resp = requests.get(url)
    resp.encoding = 'utf8'
    #text = resp.text
    text = resp.content
    elem = html.fromstring(text)

    articles = elem.cssselect('div.subtop_sise_detail')

    for a in articles:
        da =  datetime.today().strftime("%Y%m%d")
        kospi1 = a.text_content().strip()
        kospi1 = left(kospi1,8)
        Kospi_ = { 'Date' : da, 'Kospi': kospi1.replace(",","")}
    return (Kospi_)

Kospi = Kospi_real()

cnx = mysql.connector.connect(user='your_user', password='your_password',
                              host='your_host',
                              database='your_database')
cursor = cnx.cursor()

add_kospi = ("INSERT INTO TB_CR_KOSPI "
               "(date, kospi) "
               "VALUES (%s, %s) "
               "ON DUPLICATE KEY UPDATE date=%s, kospi=%s")

data_kospi = (Kospi.get("Date"), Kospi.get("Kospi"),
                  Kospi.get("Date"), Kospi.get("Kospi"))

cursor.execute(add_kospi, data_kospi)

cnx.commit()

cursor.close()
cnx.close()

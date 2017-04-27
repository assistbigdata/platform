# coding=utf-8

##함수 ----------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from lxml import html
import pandas as pd
import requests
import re
import cssselect
import urllib
Total = []
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]
# 특정년도, 월에 대한 날씨 정보 조회


dic = { 'Target':'', 'date':'','comment':'','writer':'','chk':''}
def _get_date(link):
    resp = requests.get(link)
    resp.encoding = 'utf-8'
    elem = html.fromstring(resp.text)
    return elem.cssselect('span.countGroup')[0].text_content().strip()

def _get_content(link):
    resp = requests.get(link)
    resp.encoding = 'utf-8'
    elem = html.fromstring(resp.text)
    return elem.cssselect('div.content02')[0].text_content().strip()

def topic_crawl(name,target_year):
    target_year=int(target_year)

    for num in range(0,2):
        num=str(num)
        url = 'http://www.bobaedream.co.kr/list?code=freeb&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=Body&s_key=' + name +'&level_no=&vdate=&type=list&page='+num
        print(url)
        resp = requests.get(url)
        resp.encoding = 'utf8'
        text = resp.text

        elem = html.fromstring(text)

        print(elem)

        articles = elem.cssselect('div.cList tbody tr')



        for a in articles:
            try: link = a.cssselect('td.pl14 a')[0].get('href')
            except Exception:
                pass
            real_date = _get_date(urllib.parse.urljoin(url, link))

            p = re.compile('\w\w\w\w.\w\w.\w\w')


            real_date=p.findall(real_date)
            real_date_str = str(real_date)
            real_date_str = mid(real_date_str,2,10)

            real_day = str(real_date)
            real_day = mid(real_day,10,2)

            dd = str(datetime.today().day-1)
            if real_day == dd:
                try : title = a.cssselect('td.pl14 a.bsubject')[0].text_content().strip()
                except Exception:
                    pass
                print(title)

                try: writer = a.cssselect('td.author02')[0].text_content().strip()
                except Exception:
                    pass
            else:
                break

            #    content = _get_content(urllib.parse.urljoin(url, link))
            #    real_date=p.findall(real_date)
            dic = { 'Target':name, 'date':real_date_str,'comment':title,'writer': writer,'chk':name + str(real_date) + title}
            Total.append(dic)

            #else:
            #    break


##실시간 코드 ----------------------------------------------------------------------------------------------------------------------

name_car = ['소나타','sonata','쏘나타',"모닝","그랜져",'그랜저','그렌저','그렌져','Grandeur']

for i in  range(0,9):
    topic_crawl(name_car[i],'2010')
    print(i)

Total_df = pd.DataFrame(Total)
Total_df = Total_df.drop_duplicates(subset='chk')  #delete duplicated
index = pd.DataFrame({ '모닝' : pd.Series(['모닝',0]),'소나타' : pd.Series(['소나타',1]),'그랜저' : pd.Series(['그랜저',2]),'sonata' : pd.Series(['sonata',1]),'쏘나타' : pd.Series(['쏘나타',1]),"그랜져": pd.Series(['그랜져',2]),'그렌저': pd.Series(['그런저',2]),'그렌져': pd.Series(['그렌져',2]),'Grandeur': pd.Series(['Grandeur',2])})
index=index.T
index

name = ["Target",'car_name']

index.columns = name
buzz = pd.merge(Total_df, index, on='Target') # join data
buzz_final = pd.DataFrame(buzz.groupby(['car_name','date']).count())


print(buzz_final)

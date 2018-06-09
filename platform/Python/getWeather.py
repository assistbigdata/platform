# coding=utf-8

from datetime import datetime
from datetime import date
import time
import urllib
import re
import mysql.connector
import requests
import pandas as pd
import numpy as np
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def getWeather(year, mm, stn):
    Weather = { 'Date':'','Avg_temp':"", 'High_temp':'','Low_temp': '','Cloud':"",'Rain':"",'Location':"",'Month':""}
    obs = 1
    x = 24
    y = 9
    year = str(year)
    mm = str(mm)
    stn = str(stn)

    url = "http://www.kma.go.kr/weather/observation/past_cal.jsp?stn=" + stn + "&yy=" + year + "&mm=" + mm + "&obs=1&x=24&y=9"


    lines = []


    f = urllib.request.urlopen(url)
    r = f.read()
    f.close()


    r2 = r.decode('euc-kr', 'ignore')


    lines = r2.split('\n')

    regex = '.*<td class="align_left">평균기온:(.*?)<br \/>최고기온:(.*?)<br \/>최저기온:(.*?)<br \/>평균운량:(.*?)<br \/>일강수량:(.*?)<br \/><\/td>'

    dict_month = {}   # {1 => {평균기온: xx, 최고기온: yy, 최저기온: zz, 평균운량: kk, 일강수량: ll}, 2 => ...}
    day = 1
    for l in lines:
        if not '평균기온' in l: continue

        # 불필요한 문자는 제거함
        l = l.replace("℃", "")
        

        # 정규식 검사를 한다.
        l_reg = re.match(regex, l)
        if not l_reg: continue
 
        # 일자별 딕셔너리 객체 초기화
        dict_day = {'avg':0, 'high':0, 'low':0, 'cloud':0, 'rain':0}
        #[print(a) for a in l_reg.groups()]

        data_avg = l_reg.groups()[0]     # 평균기온
        data_high = l_reg.groups()[1]    # 최고기온
        data_low = l_reg.groups()[2]     # 최저기온
        data_cloud = l_reg.groups()[3]   # 평균운량
        data_rain = l_reg.groups()[4]    # 일강수량
        if len(data_avg)>2:
            data_avg = float(data_avg)
        else:
            data_avg = 0

        dict_day['avg'] = data_avg    # 평균기온
        dict_day['high'] = data_high    # 최고기온
        dict_day['low'] = data_low     # 최저기온
        dict_day['cloud'] = data_cloud   # 평균운량
        dict_day['rain'] = data_rain.replace("-", "0").replace("mm", "")    # 일강수량

        dict_month[day] = dict_day
        day = day + 1

    return (dict_month)


yesterday = date.fromtimestamp(time.time() - 60*60*24).strftime("%Y%m%d")

Weather = getWeather(datetime.today().year, datetime.today().month, 108)[datetime.today().day-1]

cnx = mysql.connector.connect(user='ID', password='PASSWORD',
                              host='URL',
                              database='DB')
cursor = cnx.cursor()

add_weather = ("INSERT INTO TB_CR_WEATHER "
               "(date, temp_avg, temp_high, temp_low, rain, cloud) "
               "VALUES (%s, %s, %s, %s, %s, %s) "
               "ON DUPLICATE KEY UPDATE date=%s, temp_avg=%s, temp_high=%s, temp_low=%s, rain=%s, cloud=%s")

data_weather = (yesterday, Weather.get("avg"), Weather.get("high"), Weather.get("low"),
                  Weather.get("rain"), Weather.get("cloud"),
                  yesterday, Weather.get("avg"), Weather.get("high"), Weather.get("low"),
                  Weather.get("rain"), Weather.get("cloud"))

cursor.execute(add_weather, data_weather)

cnx.commit()

cursor.close()
cnx.close()


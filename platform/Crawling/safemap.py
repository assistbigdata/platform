
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import json
from bs4 import BeautifulSoup

api_key = "TORB5RPN-TORB-TORB-TORB-TORB5RPN25"
service = "WFS"
version = "1.0.0"
request = "GetFeature"
typename = "A2SM_CRMNLSTATS"
outputformat = "GML2"
base_url = "http://www.safemap.go.kr/sm/commonapis.do"
option = "?apikey=%s&SERVICE=%s&VERSION=%s&REQUEST=%s&TYPENAME=%s&OUTPUTFORMAT=%s"
url = base_url + option % (api_key, service, version, request, typename, outputformat)
response = urllib2.urlopen(url)

soup = BeautifulSoup(response)
stats = soup.findAll('safemap:a2sm_crmnlstats')

header = ['objt_id','polc_nm','plcstn_nm','polc_se','murder','brglr','rape','theft','violn','arson','nrctc','tmpt','gamble','tot','ctprvn_nm','sgg_kor_nm','ctprvn_cd','sgg_cd','x','y']
body = [header]
for stat in stats:
    line = []
    line.append(stat.find('safemap:objt_id').text)
    line.append(stat.find('safemap:polc_nm').text)
    line.append(stat.find('safemap:plcstn_nm').text)
    line.append(stat.find('safemap:polc_se').text)
    line.append(stat.find('safemap:murder').text)
    line.append(stat.find('safemap:brglr').text)
    line.append(stat.find('safemap:rape').text)
    line.append(stat.find('safemap:theft').text)
    line.append(stat.find('safemap:violn').text)
    line.append(stat.find('safemap:arson').text)
    line.append(stat.find('safemap:nrctc').text)
    line.append(stat.find('safemap:tmpt').text)
    line.append(stat.find('safemap:gamble').text)
    line.append(stat.find('safemap:tot').text)
    line.append(stat.find('safemap:ctprvn_nm').text)
    line.append(stat.find('safemap:sgg_kor_nm').text)
    line.append(stat.find('safemap:ctprvn_cd').text)
    line.append(stat.find('safemap:sgg_cd').text)
    line.append(stat.find('safemap:x').text)
    line.append(stat.find('safemap:y').text)
    body.append(line)

import csv
f = open('safemap.csv', 'w')
csv.writer(f).writerows(body)
# coding=utf-8
##함수 선언
import pandas as pd
import mysql.connector
import urllib
from datetime import datetime

##api 가저오기

url = "http://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=NGFjZGY1NmEzYmUwMDhlNzk4NGE3ZThiN2ZkYTI0NTE=&format=json&jsonVD=Y&userStatsId=lsi8505/101/DT_1DA7C26/2/1/20160528171448&prdSe=M&newEstPrdCnt=1"




req = urllib.request.Request(url)
response = urllib.request.urlopen(req).read().decode("utf-8")

json_data=pd.io.json.loads(response)

## Data 이쁘게 만들기
dd =  datetime.today().strftime("%Y%m")
find_job = json_data[0]['DT']
find_job_male = json_data[1]['DT']
find_month = json_data[0]['PRD_DE']

find_job = round(float(find_job))
find_job_male = round(float(find_job_male))
find_job_female = find_job - find_job_male

#find_job_df = pd.Series([find_job,find_job_male,find_month])
#find_job_df = pd.DataFrame(find_job_df)
#find_job_df= find_job_df.T
#name1 = ["Total","Male","Month"]
#find_job_df.columns = name1
#print(find_month)
#print(find_job)
#print(find_job_male)
#print(find_job_female)
#print(find_job_df)

cnx = mysql.connector.connect(user='your_user', password='your_password',
                              host='your_host',
                              database='your_database')
cursor = cnx.cursor()

add_employee = ("INSERT INTO TB_CR_EMPLOYEE "
               "(month, total, male, female) "
               "VALUES (%s, %s, %s, %s) "
               "ON DUPLICATE KEY UPDATE month=%s, total=%s, male=%s, female=%s")

data_employee = (find_month, find_job, find_job_male, find_job_female,
                 find_month, find_job, find_job_male, find_job_female)

cursor.execute(add_employee, data_employee)

cnx.commit()

cursor.close()
cnx.close()
%pyspark
SensorDataRDD = sc.textFile('s3://kr.assist.2018.emr/data/obama.txt')
SensorDataRDD.count()

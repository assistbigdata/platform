#!/bin/bash
GET_DATA=`sudo python3.4 /home/ubuntu/Program/Python/getNewData.py`

if [ $GET_DATA -gt 0 ]
then
	sudo R CMD BATCH /home/ubuntu/Program/R/model/runPredict.R /home/ubuntu/Program/R/model/RLog
	rm -f /home/ubuntu/newData/new.csv
fi

install.packages(c("partykit", "C50"), repos="http://cran.r-project.org")

library(C50)

##data
data <- read.csv("E:/Project_R/work/master_v3.11.csv",stringsAsFactors = F)
data_real<-data[,]

#C50
except <- c(2,3,4,7,8,9,12,13,19,20,21,22,23,24,25,26)
except1 <- c(2,3,4,7,8,9,12,13,19,20,21,22,23,24,25,26,27)
data_real$sold_duration_type<-as.factor(data_real$sold_duration_type)
c50_model <- C5.0(data_real[,-except1], data_real$sold_duration_type)

plot(c50_model)
text(c50_model)

library(partykit)
myTree2 <- C50:::as.party.C5.0(c50_model)
aa<-print(myTree2[2])
plot(myTree2[1])
plot(myTree2[2])
plot(myTree2[13])
plot(myTree2[1540])
print(myTree2)

saveRDS(c50_model, "./model/durationModel.rds")

hist(data$sold_duration, freq=FALSE,xlim = range(28))



####################################################################
library(caret)
set.seed(1000) #reproducability setting
data$sold_duration_type <- factor(data$sold_duration_type)
str(data)
intrain<-createDataPartition(y=data$sold_duration_type, p=0.7, list=FALSE) 
train<-data[intrain, ]
test<-data[-intrain, ]

library(rpart)
rpartmod<-rpart(sold_duration_type~. , data=train, method="class")
plot(rpartmod)
text(rpartmod)

install.packages(c("party"), repos="http://cran.r-project.org")
library(party)
actree <- ctree(sold_duration_type~. , data=train)
print(actree)
plot(actree)


plot(actree, type="simple")

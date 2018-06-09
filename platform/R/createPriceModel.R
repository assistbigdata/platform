cardata_ori <- read.csv("./master_v3.11.csv",stringsAsFactors = F)
data_real<-cardata_ori[,]

except1 <- c(2,3,4,8,9,12,13,14,19,20,21,22,23,24,25,26,27,30,32,33,35,36,37,42,43,45,47,52,53,54,56,59,60,61,62,64,66,67,68,70,72,73,74,76,82,83,84)

data_real1 <- data_real[,-except1]
lm_model <- lm(price ~  ., data=data_real1)

saveRDS(lm_model, "./model/priceModel.rds")


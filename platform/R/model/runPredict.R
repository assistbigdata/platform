library(C50)

cardata <- read.csv("/home/ubuntu/newData/new.csv",stringsAsFactors = F, header = F)
header <- read.csv("/home/ubuntu/Program/R/header.csv",stringsAsFactors = F)
names(cardata) <- names(header)

# Duration Type
c50_model <- readRDS("/home/ubuntu/Program/R/model/durationModel.rds")
except1 <- c(68, 69, 70, 71, 72)
pred_c50 <- predict(c50_model, cardata[,-except1], decision.values = TRUE, probability = TRUE)


# Price
lm_model <- readRDS("/home/ubuntu/Program/R/model/priceModel.rds")
except1 <-c(6, 13, 15, 16, 18, 19, 20, 25, 26, 28, 30, 35, 36, 37, 39, 42, 43, 44, 45, 47, 49, 50, 51, 53, 55, 56, 57, 59, 65, 66, 67, 68, 69, 70, 71, 72)
pred_lm <- predict(lm_model, cardata[,-except1], decision.values = TRUE, probability = TRUE)

result <-cbind(as.data.frame(cardata),as.data.frame(pred_c50))
names(result)[names(result) == "pred_c50"] <- c("sold_duration_type")

result <-cbind(as.data.frame(result),as.data.frame(round(pred_lm)))
names(result)[names(result) == "round(pred_lm)"] <- c("price")

filename <- format(Sys.time(), "%Y%m%d%H%M%S")
filename <- paste0(filename, ".csv")
filename <- paste0("/home/ubuntu/Program/R/model/result/", filename)
write.csv(result, filename, row.names=FALSE)


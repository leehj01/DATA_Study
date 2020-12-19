iris
library(reshape)
data(iris)
iris

iris$value
names(iris)
head(iris)
tail(iris)
names(iris) <- c("a","b","c","d","e","f")

iris[0]

install.packages("reshape")
library(reshape)

X=iris[,-5]
y=iris[,5]
iris2<-cbind(X,y)
rename(iris2,c(y="species"))

head(subset(iris, subset = iris$Sepal.Length >= 5.0, select = c(1,2,3)))
ifelse(a>20,"20ë³´ë‹¤?¼ ","20ë³´ë‹¤ ?ž‘?Œ")


for (i in  8:10){
  print(i)
}

repeat{
  print("hello")
  if (i>=10){
    break
  }
  i =i +1
}

for 


summary(iris)

cat(summary(iris),file = "iris.summary.txt")


tapply(iris$Sepal.Length, iris$Species, mean) #ê·¸ë£¹?•‘

job <- c(2,3,4,5,2,2,3,5,2,4,4,6,3)

class(job)
job <- factor(job, levels = c(0:8))
class(job)
income <-c(4865,2346,0,453,23562,0,342,675,0,231,241,0,3525)

length(job)
length(income)
tapply(income, job, mean)
tapply(income, job, mean, defalt=-1)


install.packages("doBy")
library(doBy)
head(orderBy(~Species + Sepal.Length, data=iris))
sampleBy(~Species, data=iris, frac=0.1,replace=T)


###

data(cars)
plot(cars)
lm(dist ~speed, cars)
abline(lm(dist~speed, cars))
abline(lm(dist~speed-1, cars), lty="dotted")


## order 

## sql

install.packages("RJDBC")
library(RJDBC)
drv <- JDBC("oracle.jdbc.OracleDriver", classPath = "ojdbc6.jar")


data("airquality")
head(airquality)


install.packages("reshape2")
library(reshape2)
air_melt <- melt(airquality,id = c("Month","Day"),na.rm = TRUE)

head(air_melt)
airquality2 = dcast(air_melt, formula = Month + Day ~variable, valur.var=value, fun.aggregate = NULL)
head(airquality2)

install.packages("ggplot2")
library(ggplot2)

install.packages(iris)
library(iris)
g <- ggplot(iris, aes(Petal.width, Petal.Length))
g +geom_point()


g4 <- ggplot(mpg, aes(cty))
g4 + geom_density(aes(fill=facor(cyl)),)
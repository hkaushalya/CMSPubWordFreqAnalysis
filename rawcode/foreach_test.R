# foreach test for parallel processing
library(foreach)
set.seed(1234)
addnoise <- function(num) {
  x = num + rnorm(1)
  x
}

addself <- function(num) {
  x = num + num
  x
}

foreach(i=1:3) %do% sqrt(i)
foreach(i=1:3) %do% addnoise(i)
foreach(i=1:3) %do% addself(i)

#use of .combine
x <- foreach(i=1:3, .combine='+') %do% rnorm(4)
print(x)

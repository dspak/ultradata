# What was the name of that dude wearing the Harper's Ferry HURT shirt and did 
# he beat his brother?
# 
# 6/13/17
# Dan Spakowicz

library(XML)
library(tidyverse)

# Pull results
x <- getURL("http://www.laurelultra.com/results_2017.htm")
# Read into table
x <- XML::readHTMLTable(x)[[1]]

# Split name into two columnds
y <- tidyr::separate(x, NAME, into = c("firstname", "lastname"), sep = " ")

# Get rows where the last names appear more than once
z <- table(y$lastname)
brothers <- names(z[z>1])
brothers <- paste(brothers, collapse = "|")
y[grep(brothers, y$lastname),]

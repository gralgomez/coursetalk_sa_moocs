#20160112
#Scrapping with RCurl
#install.packages("RCurl", dependencies = TRUE)
#install.packages("XML", dependencies = TRUE)

# Check http://blog.rstudio.org/2014/11/24/rvest-easy-web-scraping-with-r/

library('RCurl')
library('XML')
library('rvest')

#1 Get the URL and Parse the URL
reviews <- readLines("https://www.coursetalk.com/search?q=")
#Problem ist the htl document is as c("doc") format


xmlfile <- xmlTreeParse(reviews_parsed)
class(xmlfile)

xmltop = xmlRoot(xmlfile)
print(xmltop)[1:2]


#2 Extract xml data

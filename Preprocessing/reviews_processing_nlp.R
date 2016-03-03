setwd("~/Documents/Uni/MasterThesis/R")
#https://rstudio-pubs-static.s3.amazonaws.com/31867_8236987cf0a8444e962ccd2aec46d9c3.html

#Packages needed
#----------------------------------------------------------------------------------------
needed <- c("tm", "languageR", "RWeka", "qdap", "SnowballCC", "RColorBrewer", "ggplot2", "wordcloud", "biclust", "cluster", "igraph", "fpc")   
installed.packages(needed, dependencies=TRUE) 
#----------------------------------------------------------------------------------------

# [REVIEWS]
library(stringr)

# Read CSV [OUTPUT of Python Code]
reviews <- read.csv("~/PycharmProjects/scrapito_Py/reviews3.csv", header=FALSE, comment.char="#")

# [NORMALIZATION] Normalizing course rating V9
reviews$V9 <- str_extract_all(reviews$V9, "[0-9]+/[0-9]+"); reviews$V9 <- gsub("/[0-9]+","", reviews$V9); reviews$V9 <- as.numeric(reviews$V9) 

# [NORMALIZATION] Normalizing course rating V12

# [CORPUS SELECTION] Corpus creation
library(tm)
library(qdap)
library(languageR)
library(RWeka)

fk_corpus <- Corpus(DataframeSource(reviews[12]), readerControl = list(language="eng"))

# [CORPUS] Tokenization - Normalization
fk_corpus <- tm_map(fk_corpus, stripWhitespace) 
fk_corpus <- tm_map(fk_corpus, PlainTextDocument) 
fk_corpus <- tm_map(fk_corpus, content_transformer(tolower))
fk_corpus <- tm_map(fk_corpus, removePunctuation, preserve_intra_word_dashes = TRUE) #%TODO: How to detect urls nd keep them!
fk_corpus <- tm_map(fk_corpus, removeNumbers)
fk_corpus <- tm_map(fk_corpus, removeWords, stopwords("english"))  

# [CORPUS] Filtering out special Patterns
urlPat<-function(x) gsub("(ftp|http)(s?)://.*\\b", "", x) #URLS
emlPat<-function(x) gsub("\\b[A-Z a-z 0-9._ - ]*[@](.*?)[.]{1,3} \\b", "", x) #Emails
tt<-function(x) gsub("RT |via", "", x) #Twitter Tags
tun<-function(x) gsub("[@][a - zA - Z0 - 9_]{1,15}", "", x) #Twitter ids

fk_corpus <- tm_map(fk_corpus, content_transformer(urlPat))
fk_corpus <- tm_map(fk_corpus, content_transformer(emlPat))
fk_corpus <- tm_map(fk_corpus, content_transformer(tt))
fk_corpus <- tm_map(fk_corpus, content_transformer(tun))

# [CORPUS] Stemming
library(SnowballC) 
fk_corpus <- tm_map(fk_corpus, stemDocument)


# [CORPUS] Stage the Data
#----------------------------------------------
#Document Term Matrix
dtm <- DocumentTermMatrix(fk_corpus) #In this Case Review/Terms !!

#Term Document Matrix (Traspose of dtm)
tdm <- TermDocumentMatrix(fk_corpus)

#m <- as.matrix(dtm); dim(m); write.csv(m, file="dtm.csv") #In case the csv wants to be exported

# [CORPUS] Text Analytics
#----------------------------------------------
freq <- colSums(as.matrix(dtm))    # dtm has sparsity of 100%
dtms <- removeSparseTerms(dtm, 0.9)# Check sparsity and exact meaning
freq <- colSums(as.matrix(dtms))   # Total Freq of each Term along all Reviews (see length(freq))
freq <- sort(colSums(as.matrix(dtms)), decreasing=TRUE)

ord <- order(freq)  # Total Terms ordered acc Freq

#most and least frequent terms
freq[head(ord)] #(least)
freq[tail(ord)] #(most)

#freq of frequencies
head(table(freq), 20)   
tail(table(freq), 20)   

wf <- data.frame(word=names(freq), freq = freq)

#Plotting
library(ggplot2)

p <- ggplot(subset(wf, freq>465), aes(word, freq))    
p <- p + geom_bar(stat="identity")   
p <- p + theme(axis.text.x=element_text(angle=45, hjust=1))  
#----------------------------------------------
 




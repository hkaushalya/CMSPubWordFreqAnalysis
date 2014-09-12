rm(list=ls())
library(tm)
library(wordcloud)
library(SnowballC)
library(RColorBrewer)

#text is already well cleaned during the preprossing
cleanCorpus <- function(corpus) {
  print(paste0("cleanCorpus::input corpus type", class(corpus)))
  corpus <- tm_map(corpus, stripWhitespace)
  #corpus <- tm_map(corpus, content_transformer(tolower))
  #corpus <- tm_map(corpus, removePunctuation)
  #corpus <- tm_map(corpus, removeNumbers)
  corpus <- tm_map(corpus, removeWords, stopwords("english"))
  return (corpus)
}


cms <- Corpus(DirSource("data/"))
inspect(cms)

cms <- cleanCorpus(cms)
cms <- tm_map(cms, stemDocument)

dictCorpus <- cms #keep for stem completion
#dictCorpus <- tm_map(dictCorpus, PlainTextDocument) # need this bcos the new verion of tm does not return PlainTextDoc after tranformations like 'tolower

#cms <- tm_map(cms, exclude)

# stem completion
cms <- tm_map(cms, stemCompletion, dictionary=dictCorpus)
cms <- tm_map(cms, PlainTextDocument) # need this bcos the new verion of tm does not return PlainTextDoc after tranformations like 'tolower

#wordcloud(cms)
wordcloud(cms, scale=c(3,0.6), min.freq=3, max.words=100, random.order=FALSE, rot.per=0.15, use.r.layout=FALSE, colors=brewer.pal(8, "Dark2"))

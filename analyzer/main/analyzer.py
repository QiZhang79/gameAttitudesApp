from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF


import json
import numpy
import socket
import datetime
import time
import urllib.request
import pickle
from collections import namedtuple
import requests

#nc -lk 5555
class tweet_analyzer(object):

    def __init__(self):
        # Define Spark configuration
        conf = SparkConf()
        conf.setMaster("local[4]")
        conf.setAppName("twitter-analysis")
        # Initialize a SparkContext
        sc = SparkContext(conf=conf)
        sc.setLogLevel("ERROR")
        # Initialize spark streaming context
        batch_interval = 60
        self.ssc = StreamingContext(sc, batch_interval)


    def run(self):
        # Receive the tweets via TCP
        self.tweet_receive()
        # And start the streaming process
        self.ssc.start()
        self.ssc.awaitTermination()

    def tweet_receive(self):
        lines = self.ssc.socketTextStream("collector", 5555)
        self.get_sentiment_analysis(lines)
        self.get_related_keywords(lines)


    def get_sentiment_analysis(self, lines):
        hashingTF = HashingTF()
        iDF = IDF()
        model = pickle.load(open('main/model.ml', 'rb'))

        def classify_tweet(tf):
            return iDF.fit(tf).transform(tf)

        analysis = lines.map(lambda line: line.split('@')) \
                        .map(lambda x: hashingTF.transform(x)) \
                        .transform(classify_tweet) \
                        .map(lambda x: LabeledPoint(1, x)) \
                        .map(lambda x: model.predict(x.features)) \

        analysis.foreachRDD(lambda rdd: self.post_sentiment_analysis(rdd))


    def post_sentiment_analysis(self, rdd):
        tweet_cnt = len(rdd.collect())
        pos_cnt = rdd.collect().count(1.0)
        neg_cnt = tweet_cnt - pos_cnt

        url_keyword = "http://api:5000/keyword"

        try:
            response = requests.get(url_keyword)
            keyword = response.json()['keyword']
        except:
            keyword = "OMG"

        url_analysis = "http://api:5000/analysis/" + keyword
        data = {'pos_cnt': pos_cnt, 'neg_cnt': neg_cnt, 'datetime': datetime.datetime.now()}
        response = requests.post(url_analysis, data)


    def save_sentiment_analysis(self, rdd):
        with open('tweet_analysis.log', 'a+') as f:
            f.write(str(len(rdd)) + '\n')


    def get_related_keywords(self, lines):
        # Get stop words
        stop_words_url = 'https://raw.githubusercontent.com/6/stopwords-json/master/dist/en.json'
        stop_words_json = urllib.request.urlopen(stop_words_url).read()
        stop_words_decoded = stop_words_json.decode('utf8')
        # Load the stop words into a list
        stop_words = json.loads(stop_words_decoded)

        words = lines.flatMap(lambda line: line.split(' ')) \
                     .map(lambda word: word.replace('@', '')) \
                     .map(lambda word: word.replace('#', '')) \
                     .map(lambda word: word.replace(',', '')) \
                     .map(lambda word: word.replace("''", '')) \
                     .map(lambda word: word.replace('.', '')) \
                     .map(lambda word: word.replace('?', '')) \
                     .map(lambda word: word.replace('!', '')) \
                     .map(lambda word: word.replace('-', '')) \
                     .map(lambda word: word.replace('+', '')) \
                     .map(lambda word: word.replace(':', '')) \
                     .map(lambda word: word.replace("'s", '')) \
                     .map(lambda word: word.replace("’s", '')) \
                     .map(lambda word: word.lower()) \
                     .map(lambda word: word if word not in stop_words else '')

        word_cnt = words.map(lambda word: (word, 1)) \
                        .reduceByKey(lambda x, y: x + y) \
                        .transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False))

        word_cnt.foreachRDD(lambda rdd: self.post_related_keywords(rdd))


    def post_related_keywords(self, rdd):
        url_keyword = "http://api:5000/keyword"

        try:
            response = requests.get(url_keyword)
            keyword = response.json()['keyword']
        except:
            keyword = "OMG"

        related_keywords_li = list(filter(lambda x: x[0]!=keyword and x[0]!='', rdd.take(22)))
        related_keywords_dict = {}
        for pair in related_keywords_li:
            related_keywords_dict[pair[0]] = pair[1]

        url_wordcloud = "http://api:5000/wordcloud/" + keyword
        data = {'related_keywords': str(related_keywords_dict),  'datetime': datetime.datetime.now()}
        response = requests.post(url_wordcloud, data)

        with open('related_keywords.log', 'a+') as f:
            f.write(str(related_keywords_dict) + '\n')
            f.write(str(response) + '\n')


    def save_related_keywords(self, rdd):
        with open('related_keywords.log', 'a+') as f:
            f.write(str(rdd.take(20)) + '\n')



if __name__=="__main__":
    t_analyzer = tweet_analyzer()
    t_analyzer.run()

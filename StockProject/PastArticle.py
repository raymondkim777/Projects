from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
import sqlite3


class PastArticle:
    def __init__(self):
        self.__article = ""
        self.__relStock = [None, None]  # [Stock, Stock]
        self.sentimentScore = 0.0

        self.con = sqlite3.connect("word_database.db")
        self.cur = self.con.cursor()

    def setArticle(self, article_str: str):
        self.__article = article_str

    def getArticle(self):
        return self.__article

    # def sentimentAnalysis(self):  # discern bw reuters & guardian

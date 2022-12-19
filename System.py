from Stock import Stock
import sqlite3
from math import log


class System:
    def __init__(self):
        self.allStockList = []
        self.articleData = None
        self.__api_key = "QW598x36qJi8dFTfT4dwHPmGkJGsxbHt"
        self.pastArticleNum = 30
        self.pastArticleTime = 5

        self.conn = sqlite3.connect("ArticleDatabase.db")
        self.cur = self.conn.cursor()

    def addStock(self, stockName: str, companyName: str):
        newStock = Stock(stockName, companyName)
        self.allStockList.append(newStock)

    def runAllRelSentimentAnalysis(self) -> None:
        stockLen = len(self.allStockList)
        for i in range(0, stockLen - 1):
            for j in range(i + 1, stockLen):
                stock1 = self.allStockList[i]
                stock2 = self.allStockList[j]
                # print(f"Stock1: {stock1.companyName}, Stock2: {stock2.companyName}")
                if not stock1.calculated:
                    # print(f"Stock: {stock1.companyName}, term calculating")
                    self.__stockTermCalculate(stock1)
                if not stock2.calculated:
                    # print(f"Stock: {stock2.companyName}, term calculating")
                    self.__stockTermCalculate(stock2)

        for stock in self.allStockList:
            print(f"Stock: {stock.companyName}, tf_idf: {stock.tf_idf}")

    def __stockTermCalculate(self, stock: Stock) -> None:
        self.cur.execute(f"select Word_Frequency from Articles where Stocks like \"%{stock.companyName}%\";")
        stock1_tf_list = self.cur.fetchall()
        for word_list in stock1_tf_list:
            # print(word_list)
            for word_freq in word_list[0][1: -1].split("), ("):
                # print(word_freq)
                [word, freq] = word_freq.split(", ")
                if word in stock.tf_idf:
                    stock.tf_idf[word] += int(freq)
                else:
                    stock.tf_idf[word] = int(freq)

        self.cur.execute(f"select count(*) from Articles;")
        doc_num = int(self.cur.fetchone()[0])

        for word in stock.tf_idf:
            # print(f"{word}: {stock.term_freq[word]}")
            self.cur.execute(f"select count(*) from Articles where Stocks like \"%{stock.companyName}%\" and Word_Frequency like \"%{word}%\";")
            word_idf = int(self.cur.fetchone()[0])
            # print(f"{word}: {word_idf}")
            word_idf = log(doc_num / (1 + word_idf), 10)
            # print(f"{word}: {word_idf}")
            stock.tf_idf[word] *= word_idf

        stock.tf_idf = dict(sorted(stock.tf_idf.items(), key=lambda x: x[1], reverse=True))
        stock.calculated = True

    def runAllPredictSentimentAnalysis(self):
        pass

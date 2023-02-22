from System import System
from DataBase import DataBase
from PastArticle import PastArticle

'''
f = open("company_names.txt", 'r')
stockList = []
for line in f.read().split("\n"):
    stockList.append(tuple(line.split(", ")))
    '''


PAST_ARTICLE_TIME = ""
FUTURE_ARTICLE_TIME = ""
FUTURE_ARTICLE_NUM = 20

stockList = [
    ("TSLA", "Tesla"),
    ("MSFT", "Microsoft"),
    ("TWTR", "Twitter"),
    ("WMT", "Walmart"),
    ("MCD", "McDonald"),
    ("TM", "Toyota"),
    ("SONY", "Sony"),
    ("NFLX", "Netflix"),
    ("COST", "Costco"),
    ("SSNLF", "Samsung")
]

if __name__ == "__main__":
    # print(stockList)

    system = System()
    # database = DataBase()

    for stock in stockList:
        system.addStock(stock[0], stock[1])
        # database.addArticles(stock[1])

    system.runAllRelAnalysis()
    system.displayResults()

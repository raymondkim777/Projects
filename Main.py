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

stockList = [("TSLA", "Tesla"), ("MSFT", "Microsoft"), ("INTL", "Intel")]

if __name__ == "__main__":
    # print(stockList)

    system = System()

    for stock in stockList:
        system.addStock(stock[0], stock[1])

    # system.runAllRelSentimentAnalysis()

    database = DataBase()
    for stock in stockList:
        database.addArticles(stock[1])
'''


    for stock1 in system.allStockList:
        for stock2 in system.allStockList:
            if stock1 != stock2:
                system.searchPastArticle(stock1, stock2, PAST_ARTICLE_TIME, f"{stock1.companyName} and {stock2.companyName}")

    for stock in system.allStockList:
        system.searchFutureArticle(stock, FUTURE_ARTICLE_NUM, FUTURE_ARTICLE_TIME, f"{stock.companyName} future")

    article_file = open("article_examples/article_ex7.txt", "r", encoding='utf8')
    article_str = article_file.read()

    past_art = PastArticle()
    past_art.setArticle(article_str)
    print(past_art.sentimentAnalysis())
'''

'''
    print("kill me")
    article = PastArticle()
    article.setArticle("asdf")
    print(article.getArticle())

    stock1 = Stock("asdf", "asdf")
    stock2 = Stock("asdf2", "asdf2")

    stock1.updateRelSentiment(stock2, article)
    '''


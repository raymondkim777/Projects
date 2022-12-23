class Stock:
    def __init__(self, stockName, companyName):
        self.stockName = stockName
        self.companyName = companyName

        self.calculated = False
        self.tf_idf = dict()  # {word: tf_idf}
        self.RelSentimentScore = dict()  # {Stock: float}

        self.finalPublicSentiment = 0.0

    def runRelSentimentAnalysis(self):
        pass

    def runPredictSentimentAnalysis(self):
        pass

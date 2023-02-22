class Stock:
    def __init__(self, stockName, companyName):
        self.stockName = stockName
        self.companyName = companyName

        self.calculated = False
        self.tf_idf = dict()  # {word: tf_idf}
        self.keywords = []  # [word1, word2, ...]
        self.keywordRel = dict()  # {Stock: [[(word2_1) num, (word2_2) num, ...], [], [], ...]}
        self.RelSentimentScore = dict()  # {Stock: float}

        self.finalPublicSentiment = 0.0

    def runRelSentimentAnalysis(self):
        pass

    def runPredictSentimentAnalysis(self):
        pass

from Stock import Stock
import sqlite3
from math import log
import spacy

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from tkinter import *
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class System:
    def __init__(self):
        self.allStockList = []
        self.articleData = None
        self.pastArticleNum = 30
        self.pastArticleTime = 5

        self.conn = sqlite3.connect("ArticleDatabase.db")
        self.cur = self.conn.cursor()

        self.nlp = spacy.load('en_core_web_lg')
        self.keyword_cnt = 10

    def addStock(self, stockName: str, companyName: str):
        newStock = Stock(stockName, companyName)
        self.allStockList.append(newStock)

    def runAllRelAnalysis(self) -> None:
        stockLen = len(self.allStockList)
        for i in range(0, stockLen - 1):
            for j in range(i + 1, stockLen):
                stock1 = self.allStockList[i]
                stock2 = self.allStockList[j]
                # print(f"Stock1: {stock1.companyName}, Stock2: {stock2.companyName}")
                # print(f"Stock: {stock1.companyName}, term calculating")
                self.__stockTermCalculate(stock1)
                # print(f"Stock: {stock2.companyName}, term calculating")
                self.__stockTermCalculate(stock2)

        # for stock in self.allStockList:
            # print(f"Stock: {stock.companyName}, tf_idf: {stock.tf_idf}")

        # plot
        '''
        fig = plt.figure()
        fig.suptitle("Keyword Similarities between Stocks")
        '''
        rel_cnt = stockLen * (stockLen - 1) // 2

        cnt = 1
        for i in range(0, stockLen - 1):
            for j in range(i + 1, stockLen):
                stock1 = self.allStockList[i]
                stock2 = self.allStockList[j]

                # new_ax = fig.add_subplot(rel_cnt // 8 + 1, 8, cnt, projection='3d')
                cnt += 1
                self.__stockRelCalculate(stock1, stock2)
                # print(f"Score: {stock1.RelSentimentScore[stock2]}")
        plt.show()

    def __stockTermCalculate(self, stock: Stock) -> bool:
        if stock.calculated:
            return False
        self.cur.execute(f"select Word_Frequency from Articles where Stocks like \"%{stock.companyName}%\";")
        stock1_tf_list = self.cur.fetchall()
        for word_list in stock1_tf_list:
            # print(f"Word list: {word_list}")
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
        return True

    def __stockRelCalculate(self, stock1: Stock, stock2: Stock, ax=None) -> bool:
        if stock2 in stock1.RelSentimentScore:
            return False

        if not self.__stockChooseKeywords(stock1):
            raise Exception(f"{stock1.companyName} keywords not chosen")
        if not self.__stockChooseKeywords(stock2):
            raise Exception(f"{stock2.companyName} keywords not chosen")

        # print(f"{stock1.companyName} words: {stock1.keywords}")
        # print(f"{stock2.companyName} words: {stock2.keywords}")

        stock1.keywordRel[stock2] = [[0 for b in range(len(stock2.keywords))] for a in range(len(stock1.keywords))]
        stock2.keywordRel[stock1] = [[0 for b in range(len(stock1.keywords))] for a in range(len(stock2.keywords))]

        relScore = 0
        for i in range(len(stock1.keywords)):
            for j in range(len(stock2.keywords)):
                word1 = stock1.keywords[i]
                word2 = stock2.keywords[j]

                tokens = self.nlp(f"{word1} {word2}")
                curScore = tokens[0].similarity(tokens[1])
                # print(f"{word1}, {word2}: {curScore}")

                stock1.keywordRel[stock2][i][j] = curScore
                stock2.keywordRel[stock1][j][i] = curScore

                curScore = (curScore * 10 / 2.5) ** 2
                relScore += curScore

        stock1.RelSentimentScore[stock2] = relScore
        stock2.RelSentimentScore[stock1] = relScore

        # axis plot

        if ax is not None:
            ax.set_title(f"{stock1.companyName} and {stock2.companyName}: {relScore:.1f}")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([0, 0.5 ,1])
            ax.set_zlim(-0.2, 1.0)

            x, y, z = [], [], []
            dx, dy, dz = [], [], []
            for i in range(len(stock1.keywords)):
                for j in range(len(stock2.keywords)):
                    x.append(i)
                    y.append(j)
                    z.append(0)
                    dx.append(1)
                    dy.append(1)
                    dz.append(stock1.keywordRel[stock2][i][j])

            dz_np = np.array(dz)
            dz_np = np.squeeze(dz_np)

            nrm = mpl.colors.Normalize(-1, 1)
            colors = plt.cm.RdBu(nrm(-dz_np))
            alpha = np.linspace(0.2, 0.95, self.keyword_cnt, endpoint=True)

            for i in range(len(x)):
                ax.bar3d(x[i], y[i], z[i], dx[i], dy[i], dz[i], alpha=alpha[i % self.keyword_cnt], color=colors[i], linewidth=0)

        return True

    def __stockChooseKeywords(self, stock: Stock) -> bool:
        if len(stock.tf_idf) == 0:
            return False

        idx = 0
        while len(stock.keywords) < self.keyword_cnt and idx < len(stock.tf_idf):
            keyword = list(stock.tf_idf.keys())[idx]
            if self.nlp(keyword)[0].has_vector:
                stock.keywords.append(keyword)
            idx += 1
        return True

    def runAllPredictSentimentAnalysis(self):
        pass

    def displayResults(self):
        # data
        stockRelData = []
        for i in range(0, len(self.allStockList) - 1):
            for j in range(i + 1, len(self.allStockList)):
                stockRelData.append(self.allStockList[i].RelSentimentScore[self.allStockList[j]])

        # parameters
        canvas_width = 650
        canvas_height = 600

        item_radius = 250
        oval_width = 120
        oval_height = 60

        line_width = 2

        root = Tk()
        root.title("Stock Company Analysis Results")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        allFrame = Frame(root)
        allFrame.grid(row=0, column=0)

        canvasFrame = Frame(allFrame, padx=5, pady=5)
        canvasFrame.grid(row=0, column=0)

        displayCanvas = Canvas(canvasFrame, width=canvas_width, height=canvas_height)
        displayCanvas.grid(row=0, column=0)

        resultFrame = Frame(allFrame, padx=25, pady=5)
        resultFrame.grid(row=0, column=1)

        fig = plt.figure()
        resultCanvas = FigureCanvasTkAgg(fig, master=resultFrame)
        resultCanvas.draw()
        resultCanvas.get_tk_widget().pack(fill=BOTH, expand=True)

        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.set_zlim(-0.2, 1.0)

        # items
        positions = []
        colorLines = []
        stockOvals = []
        stockButtons = []
        stockVars = []

        center_xy = [canvas_width // 2, canvas_height // 2]
        for i in range(len(self.allStockList)):
            new_x = math.sin(2 * math.pi / len(self.allStockList) * i) * item_radius
            new_y = -math.cos(2 * math.pi / len(self.allStockList) * i) * item_radius
            positions.append([center_xy[0] + new_x, center_xy[1] + new_y])

        # draw color lines
        subdiv_num = 255
        rgb_s = [204, 0, 0]
        rgb_e = [102, 204, 0]
        inc = [(v1 - v2) / subdiv_num for v1, v2 in zip(rgb_e, rgb_s)]
        color = [
            f"#{int(rgb_s[0] + (i * inc[0])):02x}{int(rgb_s[1] + (i * inc[1])):02x}{int(rgb_s[2] + (i * inc[2])):02x}"
            for i in range(256)]

        maxScore = max(stockRelData)
        minScore = min(stockRelData)

        idx = 0
        for i in range(0, len(self.allStockList) - 1):
            for j in range(i + 1, len(self.allStockList)):
                color_idx = int((stockRelData[idx] - minScore) / (maxScore - minScore) * subdiv_num)
                colorLines.append(displayCanvas.create_line(
                    positions[i][0], positions[i][1],
                    positions[j][0], positions[j][1],
                    fill=color[color_idx], width=line_width
                ))
                idx += 1

        # place ovals
        for pos in positions:
            stockOvals.append(displayCanvas.create_oval(pos[0] - oval_width // 2,
                                     pos[1] - oval_height // 2,
                                     pos[0] + oval_width // 2,
                                     pos[1] + oval_height // 2,
                                     width=0, fill="#E9C8D0"))

        # place stock buttons
        for i in range(len(self.allStockList)):
            stockVars.append(IntVar())
            stockButtons.append(
                Checkbutton(displayCanvas, text=self.allStockList[i].companyName, variable=stockVars[i],
                            onvalue=1, offvalue=0, command=lambda: self.updateSpecificDisplay(ax, stockVars, resultCanvas), bg="#E9C8D0")
                .place(x=positions[i][0], y=positions[i][1], anchor=CENTER)
            )

        root.mainloop()

    def updateSpecificDisplay(self, ax, stockVars, resultCanvas):
        selectStocks = []
        selectIdx = []

        for i in range(len(stockVars)):
            if stockVars[i].get() == 1:
                selectStocks.append(self.allStockList[i])
                selectIdx.append(i)

        if len(selectStocks) != 2:
            ax.clear()

        if len(selectStocks) == 2:
            # prepare data
            stock1 = selectStocks[0]
            stock2 = selectStocks[1]
            print(f"Displayed: {stock1.companyName}, {stock2.companyName}")
            relScore = selectStocks[0].RelSentimentScore[selectStocks[1]]

            # update figure axes
            ax.set_title(f"{stock1.companyName} and {stock2.companyName}: {relScore:.1f}")

            x, y, z = [], [], []
            dx, dy, dz = [], [], []
            for i in range(len(stock1.keywords)):
                for j in range(len(stock2.keywords)):
                    x.append(i)
                    y.append(j)
                    z.append(0)
                    dx.append(1)
                    dy.append(1)
                    dz.append(stock1.keywordRel[stock2][i][j])

            dz_np = np.array(dz)
            dz_np = np.squeeze(dz_np)

            nrm = mpl.colors.Normalize(-1, 1)
            colors = plt.cm.RdBu(nrm(-dz_np))
            alpha = np.linspace(0.2, 0.95, self.keyword_cnt, endpoint=True)

            for i in range(len(x)):
                ax.bar3d(x[i], y[i], z[i], dx[i], dy[i], dz[i], alpha=alpha[i % self.keyword_cnt], color=colors[i],
                         linewidth=0)
        resultCanvas.draw()

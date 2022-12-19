#Stock Prediction Program Through Relationship Analysis between Companies

This program predicts future stock movements primarily based on news article analysis. As a basis, the program computes a vector space model of news articles regarding certain companies to quantify the associativity between different companies. For prediction, the program uses sentiment analysis on recent news articles to first predict a general trend for individual companies, then uses the computed associativity values to further adjust predictions. 

##Periods of Development
September 3, 2022 - Ongoing 

##Development Environment
-'Python 3.10'  
-'Database: SQLite'

##Core Features

###Crawling & Natural Language Processing ([DataBase.py](DataBase.py))  
Our objective is to retrieve relevant article information from online news sources and process them with NLP.  

Libraries used: selenium, bs4, nltk  
&nbsp;&nbsp;&nbsp;&nbsp; selenium: Library used to control web browser (Google Chrome). Controls browser through webdriver with chromedriver.exe separately downloaded.  
&nbsp;&nbsp;&nbsp;&nbsp; bs4: Library used to access html code & retrieve tags. Used for each Google page to retrieve article links. Used for each article link to retrieve article text.  
&nbsp;&nbsp;&nbsp;&nbsp; nltk: Library used for natural language processing. After manually removing stopwords, each remaining word's parts of speech is found via pos_tag & words are reverted to their roots via WordNetLemmatizer.  

The program uses Chrome to search Google with the query "(*company name*) company (*source*)", where (*source*) refers to the news source used (in this case, The Guardian). 10 Google search results pages and their html codes are used to extract and save all new links from the news source (if the link already exists in the database or is not from the news source, the program continues). Each article link is then individually accessed and its html code is used to extract the article's main text.  

For each article text, all stopwords are removed and all remaining words' parts of speech are identified. 
Both the words and their parts of speech are then inputted into a lemmatizer, which reverts each word back into its root form. 
This is done to avoid various forms of a word being incorrectly identified as different words (ex. eat, eats, ate, eating, eaten, etc), and improves document frequency accuracy. 

The frequency of each root word is then identified for each article and is appended to a string in SQL format, which is then
added to the SQL Database for each article.

###SQL ([DataBase.py](DataBase.py), [ArticleDatabase.db](ArticleDatabase.db]))  
SQL Database "article_database" is used to store parsed article information for later access & analysis.

Table: Articles  
&nbsp;&nbsp;&nbsp;&nbsp; Columns (3): Article_ID, Word_Frequency, Stocks  
&nbsp;&nbsp;&nbsp;&nbsp; Article_ID: Stores article links, used as unique ID for that article's information  
&nbsp;&nbsp;&nbsp;&nbsp; Word_Frequency: Stores document frequency of each word in string format --> (*word1*, *frequency1*), (*word2*, *frequency2*),...  
&nbsp;&nbsp;&nbsp;&nbsp; Stocks: Stores relevant stocks included in article (as multiple companies can be mentioned in one article)

###TF-IDF ([System.py](System.py))  
The objective of calculating the tf-idf of each word for each individual document is to quantify the relevant importance of each word for the document in respect to the overall collection of words across all documents. 
The term "tf" refers to "term frequency", and "idf" refers to "inverse document frequency". 

The equation for tf-idf is

$$\sum_{i=1}^{d} t_i \times \log_{10}(\frac{d}{1+d_t})$$

where the variables are as follows:
\begin{align*}
t &= \text{term} \\
t_i &= \text{term frequency of } t \text{ for document } i\\
d &= \text{total number of documents} \\
d_t &= \text{number of documents containing } t
\end{align*}  
  
\\
Here, each "document" refers to individual stocks; thus, multiple word frequencies across all articles relevant to a certain stock are combined to form the term frequency for each word.  

However, even though the term frequency may be high, its importance may not be. This is determined by how often the term presents itself throughout multiple documents — a term with both a high term frequency and high document frequency is likely unimportant and can be disregarded, whereas a term with a high term frequency within a certain document but low document frequency is likely important, and thus should be considered a keyword for that document.  

The term frequency and inverse of the document frequency is multiplied to form the tf-idf for each word within each stock, such that the higher the td-idf value, the more likely it is to be a keyword for that relevant stock. The inverse document frequency is logarithmized to control excessive inflation of values.

###Word Associativity
To quantify the correlation between two companies/stocks, 20 keywords with the highest tf-idf values in each stock will be used for comparison. Let us consider two stocks: $S_1$ and $S_2$. 

Comparing every word in $S_1$ with every word in $S_2$ yields a correlation value between 0 and 1, for a total of 400 values. Here, two words having low correlation is irrelevant; as long as there exists some words with high correlation, $S_1$ and $S_2$ can be considered as correlated. As a basis, a correlation value over 0.7 indicates significant similarity. Thus, each value will be multiplied by $\frac{10}{7}$ and squared, such that values over 0.7 will be amplified and values below 0.7 will decrease in significance. The sum of the results will yield a final correlation value between $S_1$ and $S_2$. This process will be repeated for all pairs of stocks within the program. 

The correlation value between two words will be computed with the library Spacy, using the vector space model "en_vectors_web_lg". 

##Reference
Christopher D. Manning et al., 2008, Introduction to Information Retrieval (8th Edition)
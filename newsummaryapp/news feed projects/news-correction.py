from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

newsapi = NewsApiClient(api_key="67267a48db3c4a44ab6c63bbaaf62040")

@app.route('/')
def home():
    return "news feed"

@app.route('/news/<string:news_source>')
def news(news_source):
    top_headlines = newsapi.get_top_headlines(sources=news_source)['articles']
    return render_template('news.html', headlines=top_headlines)

def get_container(url : str, parser): 
    if 'ndtv.com' in url:
        return parser.find(id='ins_storybody')
    elif 'cnn.com' in url:
        return parser.find(class_ = 'article__content')
    elif 'independent.co.uk' in url:
        return parser.find(id = 'main')
    else:
        return None

def get_news_data(url: str):
    page = requests.get(url)
    parser = BeautifulSoup(page.content, 'html.parser')
    container = get_container(url, parser)
    if container is None:
        return "Unknown url"
    paragraphs = container.select('p')
    news_data = ''
    for p in paragraphs:
        news_data += p.text + '\n'
    return news_data

@app.route('/article')
def article():
    url = request.args.get('url')
    article_text = get_news_data(url)
    summary = get_summary(article_text)
    return render_template('article.html', article_text=article_text, summary=summary)

def get_summary(article):
    parser = PlaintextParser.from_string(article, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 2)
    result = ""
    for words in summary:
        result += str(words)
    return result

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE news(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                urlToImage TEXT,
                categories TEXT,
                source TEXT,
                publishedAt SMALLDATETIME
            )
        ''')
        print("Table created successfully")
    except Error as e:
        print(e)

def create_connection():
    return sqlite3.connect('db/newsDatabase.db')

def initialize():
    try:
        conn = create_connection()
        create_table(conn)
        conn.close()
    except Error as e:
        print(e)
def insert_article(article):
    inserted_article = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO news(title, content, urlToImage, source, publishedAt) VALUES(?,?,?,?,?,?)", (article['title'], article['content'], article['urlToImage'], article['url'], article['publishedAt']))
        conn.commit()
        inserted_article = get_article_by_ID(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return inserted_article


def load_news():
    print('loading news...')
    headlines = get_top_headlines()
    print(headlines)
    for a in headlines:
        url = str(a['url'])
        print('scarping news from: ' + url)
        content = get_news_data(url)
        if content is None: continue
        print('summarizing the news: ')
        summary = news_summarizer.get_summary(content)
        a['content'] = summary
        news = news_feedDB.insert_article(a)
        print('News created successfully')
        print(news)

def main():
    initialize()
    load_news()

if __name__ == "__main__":
    main()
    app.run(debug=True)
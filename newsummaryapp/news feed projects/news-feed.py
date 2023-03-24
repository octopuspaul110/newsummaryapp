from flask import Flask, render_template, jsonify, make_response
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import sqlite3
from sqlite3 import Error

# import nltk
# nltk.download('punkt')

app = Flask(__name__)

# @app.route('/Index')
# def Index():

#     newsapi = NewsApiClient(api_key="67267a48db3c4a44ab6c63bbaaf62040")
#     sources = get_sources(newsapi)
#     headlines = get_top_headlines(newsapi)
    
#     return render_template('news.html', context = sources )

def create_connection():
    return sqlite3.connect(r'C:\Users\User\Desktop\news feed projects\database\newsDatabase.db')

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS news(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                img_url TEXT,
                source TEXT,
                date_published SMALLDATETIME
            )
        ''')
        print("Table created successfully")
    except Error as e:
        print(e)

def get_top_headlines():
    client = NewsApiClient(api_key="67267a48db3c4a44ab6c63bbaaf62040") 
    top_headlines = client.get_top_headlines(sources='cnn,independent',language='en')
    articles = top_headlines['articles']
    return articles

# def get_sources(client):
#     response = client.get_sources()
#     return response["sources"]

def get_article_by_ID(id):
    try:
        conn= create_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, img_url,source,date_published FROM NEWS WHERE id = ?",(id,))
        # (news_id, title, content, img_url,source,date_published)=cur.fetchone()
        row = cur.fetchone()
        if row is None: 
            return None
        article = {}
        article["id"] = row[0]
        article["title"] = row[1]
        article["content"] = row[2]
        article["img_url"] = row[3]
        article["source"] = row[4]
        article["date_published"] = row[5]
        return article
    except Error as e:
        print(e)
        return None
    finally:
        conn.close()

def insert_article(article):
    inserted_article = {}
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO news(title, content, img_url, source, date_published) VALUES(?,?,?,?,?)",
         (article['title'], article['content'], article['urlToImage'], article['url'], article['publishedAt']))
        conn.commit()
        inserted_article = get_article_by_ID(cur.lastrowid)
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return inserted_article


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
        return None
    paragraphs = container.select('p')
    news_data = ''
    for p in paragraphs:
        news_data += p.text + '\n'
    return news_data

def get_summary(article):
    parser = PlaintextParser.from_string(article, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 2)
    result = ""
    for words in summary:
        result += str(words)
    return result

def initialize():
    try:
        conn = create_connection()
        create_table(conn)
        conn.close()
    except Error as e:
        print(e)


def load_news():
    print('loading news...')
    headlines = get_top_headlines()
    print(headlines)
    for a in headlines:
        url = str(a['url'])
        print('scraping news from: ' + url)
        content = get_news_data(url)
        if content is None: continue
        print('summarizing the news: ')
        summary = get_summary(content)
        a['content'] = summary
        news = insert_article(a)
        print('News created successfully')
        print(news)

def get_all_articles():
    articles = []
    try:
        conn = create_connection()
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        curr.execute("SELECT id,title, img_url, date_published FROM NEWS")
        rows = curr.fetchall()

        for row in rows:
            article = {}
            article["id"] = row["id"]
            article["title"] = row["title"]
            article["img_url"] = row["img_url"]
            article["date_published"] = row["date_published"]
            articles.append(article)
        return articles       
    except Error as e:
        print(e)
        return articles
    finally:
        conn.close()
        
def main():
    initialize()
    
@app.route('/articles')
def get_articles():
    result = get_all_articles()
    return jsonify({'message':'success', 'data':result})

@app.route('/articles/<id>')
def get_article(id):
    result = get_article_by_ID(id)
    if result is None:
        return make_response(jsonify({'message':'Not found', 'data': result}),404)
    return jsonify({'message':'success', 'data': result})

@app.route('/articles', methods=['GET'])
def search():
    try:
        conn = create_connection()
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        query = """
            SELECT * FROM news
            WHERE title LIKE '%' || ? || '%'
            OR content LIKE '%' || ? || '%';
            """
        search_anything = request.args.get('search_anything')
        results = curr.execute(query, (search_anything, search_anything)).fetchall()
        if results is None:
            return make_response(jsonify({'message':'Not found', 'data': reults}),404)
        return jsonify({'message':'success', 'data': results})
    finally:
        conn.close()


# @app.route('/articles')
# def Articles():
#     newsapi = NewsApiClient(api_key="67267a48db3c4a44ab6c63bbaaf62040")
#     articles = get_top_headlines(newsapi)

#     return render_template('articles.html', context = articles)

if __name__ == "__main__":
    main()
    app.run(debug = True)

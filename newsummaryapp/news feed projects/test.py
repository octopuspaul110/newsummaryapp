from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

app = Flask(__name__)

newsapi = NewsApiClient(api_key="67267a48db3c4a44ab6c63bbaaf62040")


print(newsapi.get_top_headlines()['articles'])

@app.route('/Index')
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
    container = get_container(url,parser)
    if container is None:
        return "Unknown url"
    paragraphs = container.select('p')
    news_data=''
    for p in paragraphs:
        news_data += p.text + '\n'
    return news_data

def get_summary(article):
    parser = PlaintextParser.from_string(article,Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 2)
    result =""
    for words in summary:
        result +=  str(words)
    return result

if __name__ == "__main__":
    app.run(debug = True)

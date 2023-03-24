import requests
from bs4 import BeautifulSoup

def independent(url="https://www.independent.co.uk/news/world/americas/chinese-spy-balloon-location-latest-news-b2277966.html"):
    news = requests.get(url)
    soup = BeautifulSoup(news.content, 'html.parser')
    div_main = soup.find('div', id = "main")
    #print(div_main.find_all('p').get_text())
    div_p = div_main.find_all('p')
    for line in div_p[1:]:
        print(line.get_text())

news=requests.get("https://www.cnbctv18.com/market/stock-market-live-updates-share-market-today-airtel-hero-motocorp-adani-green-vodafone-idea-15881631.html")
soup = BeautifulSoup(news.content, 'html.parser')
# div_sdc = soup.find('div', class_="sdc-article-body sdc-article-body--story sdc-article-body--lead")
# div_s = div_sdc.find_all('p')
# for line in div_s:
#     print(lie.get_text())
div_sdc = 
print(soup.find_all('p'))

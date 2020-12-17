
from bs4 import BeautifulSoup
import html5lib
import requests
from datetime import datetime



now_date = datetime.now().strftime("%Y-%m-%d-%H:%M")
# print(now_date)

target_site = f'https://finance.naver.com/news/mainnews.nhn?date={now_date}'
# 웹 스크래핑
res = requests.get(target_site)
soup = BeautifulSoup(res.text, 'html5lib')
main_news = soup.select('div.mainNewsList > ul > li')


results = list()
for news in main_news:
    time = news.select_one('span.wdate')
    if not news.a.string:
        tmp = news.select_one('dl > dd.articleSubject > a')
        dic = {
            'title' : tmp.string
            ,'href': 'https://finance.naver.com' + tmp.get('href')
            ,'time': time.string
        }
    else:
        dic = {
            'title' : news.a.string
            ,'href': 'https://finance.naver.com' + news.a.get('href')
            ,'time': time.string
        }
    results.append(dic)



import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import pandas.io.sql as pSql

protocal = 'mysql+pymysql'
user     = 'admin'
password = 'pnudb960726!'
domain   = 'personaldb.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com'
port = 3306
database = 'yaneodoo'
db_url = f'{protocal}://{user}:{password}@{domain}:{port}/{database}'
df = pd.DataFrame(results)


try:
    engine = create_engine(db_url, encoding = 'utf8')
    conn = engine.connect()
    df.to_sql(name = 'main_news3', con = conn, if_exists='replace', index=False)
except Exception as e:
    print(e)
finally:
    conn.close()




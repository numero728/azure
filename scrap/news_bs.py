from bs4 import BeautifulSoup
import html5lib
import requests


target_site = 'https://finance.naver.com/news/'
res = requests.get(target_site)
soup = BeautifulSoup(res.text, 'html5lib')
main_news = soup.select('div.main_news > ul > li')
results = list()
for news in main_news:
    dic = {
        'title' : news.a.string
        ,'href': news.a.get('href')
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
engine = create_engine(db_url, encoding = 'utf8')
try:
    conn = engine.connect()
    df.to_sql(name = 'main_news2', con = conn, if_exists='append', index=False)
except Exception as e:
    print(e)
finally:
    conn.close()

from bs4 import BeautifulSoup
from urllib.request import urlopen


target_site = 'https://finance.naver.com/marketindex/exchangeList.nhn'
res = urlopen(target_site)



if res.getcode() != 200:
  print('사이트에 뭔가 문제가 있다 점검 필요')



soup = BeautifulSoup(res, 'html5lib')




results = list()
for tr in soup.select('tbody > tr'):
    dic = {
        'name' : tr.select_one('.tit').a.string.strip()
        ,'code': tr.select_one('.tit').a.get('href')[-6:-3]
        ,'info_link' : tr.select_one('.tit').a.get('href')
        ,'buy_std': tr.select_one('.sale').string.strip().replace(',','')
        ,'buy_cash': tr.select_one('td:nth-of-type(3)').string.strip().replace(',','')
        ,'sell_cash': tr.select_one('td:nth-of-type(4)').string.strip().replace(',','')
        ,'send_cash': tr.select_one('td:nth-of-type(5)').string.strip().replace(',','')
        ,'get_cash': tr.select_one('td:nth-of-type(6)').string.strip().replace(',','')
        ,'USD_rate': tr.select_one('td:nth-of-type(7)').string.strip()
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

from datetime import datetime
df = pd.DataFrame(results)
stamp=datetime.now().strftime('%Y-%m-%d-%H:%M')
df['meta']=stamp
engine = create_engine(db_url, encoding = 'utf8')
conn = engine.connect()
df.to_sql(name = 'exchange_rate', con = conn, if_exists='replace', index=False)
conn.close()





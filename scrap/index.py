from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import requests
import time
import pandas as pd
import os
path='/home/azureuser/azure/scrap/file'
options=Options()
prefs={"profile.default_content_settings.popups": 0,
        "download.default_directory":path,
        "directory_upgrade": True}
options.add_experimental_option('prefs',prefs)
options.add_argument('--headlss')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver=wd.Chrome(executable_path='/usr/local/bin/chromedriver',chrome_options=options)
driver.get('http://marketdata.krx.co.kr/contents/MKD/03/0301/03010000/MKD03010000.jsp')
time.sleep(10)
btns=driver.find_elements_by_css_selector('.design-center button')
for btn in btns:
    if btn.text=='CSV':
        btn.click()
        time.sleep(5)
        driver.close()
        driver.quit()
    else:
        continue

df=pd.read_csv(path+'data.csv')
if os.path.isfile(path+'data.csv'):
    os.remove(path+'data.csv')
df=df.iloc[:,2:]
del df['null.2']
from sqlalchemy import create_engine
import pymysql
from datetime import datetime
protocal = 'mysql+pymysql'
user     = 'admin'
password = 'pnudb960726!'
domain   = 'personaldb.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com'
port = 3306
database = 'scrap_data'
db_url = f'{protocal}://{user}:{password}@{domain}:{port}/{database}'
eng=create_engine(db_url)
conn=eng.connect()
meta=datetime.now().strftime('%Y-%m-%d-%H:%M')
df['meta']=meta
df.to_sql('market_index',con=conn,if_exists='replace',index=False)
conn.close()

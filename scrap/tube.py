from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import platform
import time
import urllib
import os

try:
    options=Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--deisable-dev-shm-usage')
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    keyword = urllib.parse.quote('주식') 
    target_site = f'https://www.youtube.com/results?search_query={keyword}&sp=CAMSBAgCEAE%253D'
    driver.get( target_site )

    for n in range(5):
        driver.execute_script('''
            window.scrollBy(0, 1000)
        ''')
        time.sleep(2)
    videos = driver.find_elements_by_tag_name('ytd-video-renderer')
    len( videos )
    for video in videos[:20]:
        target = video.find_element_by_id('video-title')
        title  = target.get_attribute('title')
        thumbnail = video.find_element_by_id('img').get_attribute('src')
        video_url = target.get_attribute('href')
        print( title, thumbnail, video_url )
    youtube_list = list()
    for video in videos[:20]:  
        target    = video.find_element_by_id('video-title')
        title     = target.get_attribute('title')
        thumbnail = video.find_element_by_id('img').get_attribute('src')    
        video_url = target.get_attribute('href')
        youtube_list.append( {
            't':title,
            'n':thumbnail,
            'v':video_url
        } )
    youtube_list

    import pandas as pd
    import pymysql
    df = pd.DataFrame(youtube_list)

    from sqlalchemy import create_engine
    import pandas.io.sql as pSql
    protocal = 'mysql+pymysql'
    user     = 'admin'
    password = 'pnudb960726!'
    domain   = 'personaldb.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com'
    port = 3306
    database = 'yaneodoo'
    db_url = f'{protocal}://{user}:{password}@{domain}:{port}/{database}'
    engine = create_engine(db_url, encoding = 'utf8')
    conn = engine.connect()
    df.to_sql(name = 'youtube', con = conn, if_exists ='append',index = False)
except Exception as e:
    print(e)
finally:
    try:
        conn.close()
    finally:
        try:
            driver.close()
        finally:
            driver.quit()







# In[ ]:





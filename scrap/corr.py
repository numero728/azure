# 모듈 import
import requests
import pandas as pd
from zipfile import ZipFile
from bs4 import BeautifulSoup as BS
import lxml
import json
import datetime
import pymysql
from sqlalchemy import create_engine

if True:
    # DB 연결 및 상장기업 목록 조회
    conn=pymysql.connect(
        user='admin',
        host='personaldb.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        password='pnudb960726!',
        charset='utf8mb4',
        database='information_schema',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        sql="SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA='hist_data';"
        cursor.execute(sql)
        data=cursor.fetchall()
        conn.close()

    table_list=[x['TABLE_NAME'] for x in data]


if True:
    for table_name in table_list[0]:
        conn=pymysql.connect(
            user='admin',
            host='personaldb.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com',
            port=3306,
            password='pnudb960726!',
            charset='utf8mb4',
            database='information_schema',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            sql=f"SELECT 'Close' FROM '{table_name}';"
            cursor.execute(sql)
            data=cursor.fetchall()
            conn.close()

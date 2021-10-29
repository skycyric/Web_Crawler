from abc import ABC
from typing import Text
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
result = []
for article_id in range(2110613, 2110614):
    url = f'https://health.ettoday.net/news/{article_id}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    pagetitle = soup.find('h1', {'class': 'title'}).getText().strip()
    dateclear = str(soup.find('time', {'class': 'date'}))
    pagedate = str(re.sub('<.*?>|[|]', '', dateclear))
    print('讀取頁面：' + url)
    result.append({'文章標題': pagetitle, '文章日期': pagedate})
    test = pd.DataFrame(result)
print(test)
test.to_excel('ettoday.xlsx', sheet_name="ettoday", index=False)

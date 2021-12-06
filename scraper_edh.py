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
for article_id in range(29500, 30000):
    url = f'https://www.edh.tw/article/{article_id}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    pagetitle = soup.find('h1', {'class': 'title'}).getText().strip()
    categoryclear = str(soup.find_all(
        'span', {'itemprop': 'itemListElement'}))
    category = str(re.sub('<.*?>', '', categoryclear))
    dateclear = str(soup.find('span', {'itemprop': 'datePublished'}))
    pagedate = str(re.sub('<.*?>|[|]', '', dateclear))
    viewsclear = str(soup.find('span', {'class': 'article_view'}))
    pageviews = str(re.sub('<.*?>|[瀏覽數]', '', viewsclear))
    print('讀取頁面：' + url)
    result.append({'文章標題': pagetitle, '文章類別': category,
                  '文章日期': pagedate, '瀏覽數': pageviews})
    test = pd.DataFrame(result)
print(test)
test.to_excel('edh.xlsx', sheet_name="edh", index=False)

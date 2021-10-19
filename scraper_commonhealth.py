from abc import ABC
from typing import Text
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}
result = []
for article_id in range(85202, 85203):
    url = f'https://www.commonhealth.com.tw/article/{article_id}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    pagetitle = soup.find('h1', {'name': 'title'})
    categoryclear = str(soup.find_all(
        'ul', {'class': 'page__breadcrumb'}))
    category = str(re.sub('<.*?>', '', categoryclear))
    dateclear = str(soup.find('span', {'id': 'publish_time'}))
    pagedate = str(re.sub('<.*?>', '', dateclear))
    viewsclear = str(
        soup.find('div', {'class': 'info__line info__line--view'}))
    pageviews = str(re.sub('<.*?>|[瀏覽數]', '', viewsclear))
    print('讀取頁面：' + url)
    result.append({'文章標題': pagetitle, '文章類別': category,
                  '文章日期': pagedate, '瀏覽數': pageviews})
    test = pd.DataFrame(result)
print(test)
test.to_excel('commonhealth.xlsx', sheet_name="commonhealth", index=False)

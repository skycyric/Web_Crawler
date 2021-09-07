from bs4 import BeautifulSoup
import requests


class Article:
    # 建構式
    def __init__(self, *article_numbers):
        self.article_numbers = article_numbers
        print(self.article_numbers)

    # 爬取

    def scrape(self):

        result = list()

        for article_number in self.article_numbers:

            response = requests.get(
                "https://www.edh.tw/article/" + article_number
            )
            soup = BeautifulSoup(response.text, "lxml")

            artilcle_title = soup.find(
                "meta", {"itemprop": "headline"}
            ).get_attribute_list("content")  # 取得標題

            article_date = soup.find(
                "meta", {"itemprop": "datePublished"}
            ).get_attribute_list("content")  # 取得資料日期

            article_views = soup.find(
                "span", {"class": "number"}
            ).getText().strip()  # 取得瀏覽數

            result.append(
                str(artilcle_title,) + str(article_date,) + str(article_views)
            )
        return result


article = Article("28575")  # 建立article物件
print(article.scrape())  # 印出爬取結果

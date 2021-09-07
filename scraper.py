from bs4 import BeautifulSoup
import requests
import openpyxl


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
                str(artilcle_title) + str(article_date) + str(article_views)
            )
        return result

    # 建立工作簿
    def export(self, articles):
        wb = openpyxl.Workbook()
        sheet = wb.create_sheet("早安健康", 0)

        response = requests.get(
            "https://www.edh.tw/article/28575"
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

        titles = ("文章日期",) + tuple(article_date.getText(),
                                   artilcle_title.getText(), article_views.getText())
        sheet.append(titles)
        for article in articles:
            sheet.append(article)

        wb.save("競網數據.xlsx")


article = Article("28575")  # 建立article物件
article.export(article.scrape())  # 印出爬取結果到excel

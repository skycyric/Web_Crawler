import requests
from bs4 import BeautifulSoup
import csv


def get_meta_robots_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        if meta_robots:
            return meta_robots.get('content')
    return None


def main():
    base_url = "https://health.tvbs.com.tw/"

    categories = ["medical", "nutrition", "tcm", "regimen", "review",
                  "exercise", "cancer", "life", "strong", "encyclopedia", "recipe", "topic"]

    N = 10  # 您可以將 N 更改為您想要的最大數字
    numbers = range(1, 300000 + 1)

    results = []

    for category in categories:
        for number in numbers:
            url = f"{base_url}{category}/{number}"
            content = get_meta_robots_content(url)
            if content:
                results.append([url, content])
                print(f"URL: {url} - Meta robots content: {content}")
            else:
                results.append([url, "Not found or request failed"])
                print(
                    f"URL: {url} - Meta robots tag not found or request failed")

    # 將結果寫入 CSV 文件
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Meta Robots Content"])
        writer.writerows(results)


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}

result = []
url = f"https://www.youtube.com/playlist?list=PLKLVl0LnnSQx8hNmq8zJ2T-9G6BAz0wVc"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
a = soup.find_all("a")
print(a)

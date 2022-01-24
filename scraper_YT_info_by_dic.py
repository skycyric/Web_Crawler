from os import sep
from pprint import pprint
import openpyxl
import youtube_dl
import io
import sys
import re
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")


def get_video_info(youtube_url):
    video_info = {}

    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        video_info["ID"] = info.get("id")
        video_info["標題"] = info.get("title")
        video_info["上傳者"] = info.get("uploader")
        video_info["影片長度(秒)"] = info.get("duration")
        video_info["觀看次數"] = info.get("view_count")
        video_info["標籤"] = info.get("tags")
        video_info["網頁網址"] = info.get("webpage_url")
        video_info["上傳日期"] = info.get("upload_date")
    return video_info


if __name__ == "__main__":
    video_info = get_video_info("https://www.youtube.com/watch?v=z2rIp8LU4c4&t=992s")
    pprint(video_info)

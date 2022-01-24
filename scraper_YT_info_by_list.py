from pprint import pprint
import csv
import pandas as pd
import youtube_dl
import io
import sys
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")

test = subprocess.call(
    ["youtube-dl -j --flat-playlist 'https://www.youtube.com/playlist?list=PLKLVl0LnnSQx8hNmq8zJ2T-9G6BAz0wVc' | jq -r '.id' | sed 's_^_https://youtu.be/_' > result.csv"], Shell=True)

result = []
with open("C:\Project\Web_Crawler\YT_CSV\點擊最高！.csv", newline="") as csvfile:  # open csv file
    rows = csv.reader(csvfile)
    for row in rows:
        vids = "".join(row)
        url = f"https://www.youtube.com/watch?v={vids}"
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            Video_ID = info.get("id")
            Video_Title = info.get("title")
            Video_Uploader = info.get("uploader")
            Video_Duration = info.get("duration")
            Video_Views = info.get("view_count")
            Video_Tags = info.get("tags")
            Video_Url = info.get("webpage_url")
            Video_UploadDate = info.get("upload_date")
            result.append(
                {"影片ID": Video_ID, "影片標題": Video_Title, "影片標籤": Video_Tags})
            test = pd.DataFrame(result)
pprint(test)
test.to_excel("ytTest.xlsx", sheet_name="yt", index=False)

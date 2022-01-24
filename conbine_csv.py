import csv

with open("C:\Project\Web_Crawler\YT_CSV\點擊最高！.csv", newline="") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        vids = "".join(row)
        print(vids)

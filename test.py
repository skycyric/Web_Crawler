import imp
import requests
from bs4 import BeautifulSoup

playlist = []
url = input("Enter the Youtube Playlist URL : ")  # Takes the Playlist Link
data = requests.get(url)
soup = bs4.BeautifulSoup(data.text, 'html.parser')

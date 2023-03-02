import urllib.request
from bs4 import BeautifulSoup
import requests

# textToSearch = 'hello world'
# query = urllib.parse.quote(textToSearch)
# url = "https://www.youtube.com/results?search_query=" + query

# html = requests.get(url)
# html = html.text

# soup = BeautifulSoup(html, 'html.parser')

# print (soup.prettify())

# links = soup.find_all("a", id_="video-title")

# print (links)

# # for vid in links:
# #     print('https://www.youtube.com' + vid['href'])

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; + http://www.google.com/bot.html)'}

textToSearch = 'hello world'

url = 'https://www.youtube.com/results'

response = requests.get(url, params={'search_query': textToSearch}, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

print("video-title" in soup.prettify())

x = soup.find(id="video-title")

print(x)

# for vid in x:
#     print('https://www.youtube.com' + vid['href'])
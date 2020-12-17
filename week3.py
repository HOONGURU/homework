import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


my_client = MongoClient("localhost", 27017)
myDb = my_client['dbsparta']
myMusicCol = myDb['musicList']



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

music_lists = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#
# for music_list in music_lists:
#     number = music_list.select_one('td.number').get_text("", strip=True).strip("상승, 하강, 유지")
#     title = music_list.select_one('td.info > a.title.ellipsis').get_text("", strip=True)
#     print(number, title)

for music_list in music_lists:
    number = music_list.select_one('td.number')
    artist = music_list.select_one('td.info > a.artist.ellipsis').text

    for span in number('span'):
        span.decompose()

    number = number.text.strip()
    title = music_list.select_one('td.info > a.title.ellipsis').get_text("", strip=True)
    myMusicCol.insert_one({"number": number, "title": title, "artist": artist})
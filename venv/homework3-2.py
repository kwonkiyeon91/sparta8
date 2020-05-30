import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
music_chart = soup.select('table.list-wrap > tbody > tr')

# movies (tr들) 의 반복문을 돌리기
rank = 1
print(len(music_chart))
for music in music_chart:
    #print(music)
    #print(music.select_one('tr > .check'))

    #break
    #movie 안에 a 가 있으면,
    title_tag = music.select_one('td.info > a.title')
    if title_tag is not None:

        title = music.select_one('td.info > a.title').text

        #if rank == 1:
        #print(title)
        title = title.replace('\n', '')
        #print(title)
        title = title.lstrip()
        #print(title)
        #break

        artist = music.select_one('td.info > a.artist').text
        temp = {
            'rank':rank,
            'title':title,
            'artist':artist
        }
        db.music_chart.insert_one(temp)
        rank += 1
        print(temp)
    else:
        print(music)

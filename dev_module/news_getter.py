import requests
from bs4 import BeautifulSoup
from CONFIG import settings



def get_news():
    '''
    네이버 뉴스에서 제목과 내용 가져와서, app.py의 news_get라우터 함수에 리턴
    :param: None
    :return: 문자열 리스트
    '''
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(settings.ECONOMY, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    news = soup.select('#main_content > div > div._persist > div:nth-child(1) > div')
    news_box = []
    error_image = 'https://www.pyeongtaek.go.kr/common/images/etc/ready.jpg'
    for target in news:
        title = target.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a')
        sentence = target.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede')
        img_src = target.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div > a > img')
        try:
            news_box.append(title.text+'$%$'+sentence.text+'$%$'+img_src.attrs['src'])
        except:
            news_box.append(title.text + '$%$' + sentence.text + '$%$' + error_image)
            pass
    return news_box

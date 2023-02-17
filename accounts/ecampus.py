import requests
from bs4 import BeautifulSoup as bs



# e-campus 로그인
def ecampus(id, password):
    user_info = {"username": id, "password": password}
    session = requests.Session()
    request = session.post("https://ecampus.smu.ac.kr/login/index.php", data=user_info)

    if request.url == "https://ecampus.smu.ac.kr/":     # 로그인 성공
        return session


# 사용자 정보 크롤링
def information(session):
    if session:
        request = session.get("https://ecampus.smu.ac.kr/user/user_edit.php")
        source = request.text
        soup = bs(source, "html.parser")

        context = {
            "name": soup.find('input', id='id_firstname').get('value'),
            "department": soup.find('input', id='id_department').get('value'),
            "email": soup.find('input', id='id_email').get('value')
        }
        return context

# 학기별 과목 정보 크롤링
def subject(session, year, semester):
    url = f'https://ecampus.smu.ac.kr/local/ubion/user/?year={year}&semester={semester}'
    request = session.get(url)
    source = request.text
    soup = bs(source, "html.parser")
    return soup.find_all('a', class_='coursefullname')


def getSBJ_ID(session, year, semester, SBJ_NO):
    url = f'https://ecampus.smu.ac.kr/local/ubassistant/index.php?a_year={year}&a_semester={semester}&a_type=idnumber&a_keyword={SBJ_NO}'
    request = session.get(url)
    source = request.text
    soup = bs(source, "html.parser")
    return list(map(lambda x: changeFormat(x['href']), soup.find_all('a', class_='audit')))


def changeFormat(url):
    return int(url.split('id=')[1])

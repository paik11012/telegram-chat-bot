from flask import Flask,request
import pprint
from decouple import config
import requests
API_TOKEN = config('API_TOKEN')                     #상수는 대문자


app = Flask(__name__)

API_TOKEN = config('API_TOKEN')
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')


@app.route('/')
def hello():
     return 'Hello world'


@app.route('/greeting/<name>')
def greeting(name):
     return f'Hello, {name}'


@app.route(f'/{API_TOKEN}', methods=['POST'])       #telegram은 post요청으로만 받겠다, 메세지 들어옴
def telegram():                                     #웹 북 셋팅 = 주소가 어디로 들어갈 지 설정하는 것
    from_telegram = request.get_json()
    #pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None:    #from_telegram 딕셔너리 형태, get으로 접근하면 내용 없어도 오류 안뜸
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')
        
        #첫 네글자가 '/번역 '일 때 확인
        if text[0:4] == '/한영 ': 
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,#요청에 대한 정보는 headers에 있다, trailing comma
            }
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:]}#4번째 글자 이후의 문자열만 대상으로 번역하겠다 알겠니?
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')

        if text[0:4] == '/영한 ':
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,#요청에 대한 정보는 headers에 있다, trailing comma
            }
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:]
            }
            #요청보내기
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')
        
        
        #send message api url
        baseurl = 'https://api.telegram.org'
        apiurl = f'{baseurl}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(apiurl)
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
    #ngrok 다운로드 받기 / 3/ 
    #지금까지는 get request(주소창에 뭐 치는거), post request(회원가입, 게시글 작성 등 그냥 버튼 누르는 것)

    #python anywhere
    
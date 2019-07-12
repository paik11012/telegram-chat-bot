import requests                     #bot에게 명령하기 위해서
import pprint                       #이쁘게
from decouple import config         #decouple에서 config 호출

baseurl = 'https://api.telegram.org'
token = config('API_TOKEN')
chatid = config('CHAT_ID')
text = '난 람쥐야, 반갑다옹'

apiurl = f'{baseurl}/bot{token}/sendMessage?chat_id={chatid}&text={text}'
response = requests.get(apiurl)
pprint.pprint(response.json())      #깔끔하게 프린트

#환경변수 .env
#사용자-봇-flask 까지 메세지가 보내진다
#미세먼지라는 단어가 있으면 (누구에게, 어떤 메세지를 받았는가) - 그리고 값을 측정해 메세지를 보내줘
# chapter 06_04
# 코루틴 : 하나의 쓰레드에서 yield , generate 에는 코루틴 개념이 들어가 있다.
# Asyncio
# 비동기 I/O : 동기는 기다리는 것이고, 비동기는 기다리지 않는것, 비동기 I/O Coroutine 작업
# Generator => 반복적인 객체 Return (yield)
# 즉 , 실행 하고 멈추고 -> 다른 작업으로 위임해주고 -> Stop 지점 부터 재실행 원리
# Non-Blocking 비동기 처리에 적합
# 코루틴에는 Asyncio 가 존재

# BlockIO : 내가 무엇가 요청할때, 쓰레드가 멈쳐있는 것. 한명때문에 모두가 멈쳐있는 것
# 순차 실행

import timeit
from urllib.request import urlopen # 웹사이트에 요청
import ssl

# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)>
# 위와 같은 에러가 발생하여, 아래의 context 를 만들어주고, 그것을 uropen 에 넣어준다. 그럼 해결된다.
# 원인 : 개정된 pep 467 에 따라 모든 https 통신은 필요한 인증서와 호스트 명을 기본으로 체크하도록 되어있어서 그렇다고 한다.
# 해결방법은 아래와 같이, urlopen의 context 파라미터를 넘겨주면 에러를 발생시키지 않는다.
# 만약, import requests 로 접근할 경우, requests.get(url, verify=False) 을 적어주면 된다.
context = ssl._create_unverified_context()
urls = ['http://daum.net', 'https://google.com', 'https://apple.com', 'https://tistory.com', 'https://github.com', 'https://gmarket.co.kr']

start = timeit.default_timer()

# 순차 실행부
for url in urls:
    print('Strart', url)
    #실제 요청
    text = urlopen(url, context =context) # 요청이 오면, 아래에 print - 요청이 와야 다음 단계에 가기 때문에, 이것때문에 동시에 하지는 못함 요청하면 모든 코루틴이 멈춘다
    # print('Contents', dir(text), text.read()) # text.read() : 실제 메인페이지의 내용을 볼수 있다.
    # 이것을 block IO 라고 함
    print('Done', url)

# 완료시간 - 시작시간
duration = timeit.default_timer() - start

# 총 실행 시간
print('Total Time', duration)
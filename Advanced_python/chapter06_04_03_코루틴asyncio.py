# chapter 06_04
# 코루틴 : 하나의 쓰레드에서 yield , generate 에는 코루틴 개념이 들어가 있다.
# Asyncio
# 비동기 I/O : 동기는 기다리는 것이고, 비동기는 기다리지 않는것, 비동기 I/O Coroutine 작업
# Generator => 반복적인 객체 Return (yield)
# 즉 , 실행 하고 멈추고 -> 다른 작업으로 위임해주고 -> Stop 지점 부터 재실행 원리
# Non-Blocking 비동기 처리에 적합
# 코루틴에는 Asyncio 가 존재

# BlockIO -> Thread 사용
# 쓰레드 개수 및 GIL 문제 염두, 공유 메모리 문제 해결

import timeit
from urllib.request import urlopen # 웹사이트에 요청
import ssl
from concurrent.futures import ThreadPoolExecutor
import threading # 어떤 쓰레드가 어떻게 일하는지 보는 것 - 몇번쓰레드까지 만들어졌는지 모니터링
import asyncio

# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)>
# 위와 같은 에러가 발생하여, 아래의 context 를 만들어주고, 그것을 uropen 에 넣어준다. 그럼 해결된다.
# 원인 : 개정된 pep 467 에 따라 모든 https 통신은 필요한 인증서와 호스트 명을 기본으로 체크하도록 되어있어서 그렇다고 한다.
# 해결방법은 아래와 같이, urlopen의 context 파라미터를 넘겨주면 에러를 발생시키지 않는다.
# 만약, import requests 로 접근할 경우, requests.get(url, verify=False) 을 적어주면 된다.
context = ssl._create_unverified_context()
urls = ['http://daum.net', 'https://google.com', 'https://apple.com', 'https://tistory.com', 'https://github.com', 'https://gmarket.co.kr']

start = timeit.default_timer()


async def fetch(url):
    print('Thread Name :', threading.current_thread().getName(), 'Start', url) # 현재 쓰레드가 어디인지를 나타내는 애
    urlopen(url, context=context)
    print('Thread Name :', threading.current_thread().getName(), 'Done', url)  # 현재 쓰레드가 어디인지를 나타내는 애


# 동시성이기 때문에, 실행하는 순서도 매번 바뀐다. 그냥 일이 끝나는데로 반환되는 것을 볼 수 있다.
# 3.6 이후, 여러개의 generate 를 가지는 함수앞에는 async 가 붙는다.
# main 이 여러가지로 진행하니깐,async
async def main():
    #  3.7이상부터 ? yield from 이 await 으로 바뀜.


    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            executor.submit(fetch, url) # 패치 함수와 url 을 넣어주면 됨.

# 쓰레드를 할때는 main을 늘 만들어줘야한다. 진입점이 없으면 에러가 발생한다.
if __name__ == '__main__':
    # 코루틴에 여러 함수 와 yield 를 쓸때, 중간에서 중재해주는 애가 필요하다. 요즘은 asyncio 로 간단히 할 수 있다.
    # 루프 생성
    loop = asyncio.get_event_loop() # 여러개의 generate 가 있으면, yield로 멈추면, 다음으로 제어건을 가져오도록 흐름을 만들어주는 아이
    # 루프 대기
    loop.run_until_complete(main()) # 모든 generate 가 끝날때까지 기다려주는 함수


    # 함수 실행
    main()

    # 완료시간 - 시작시간
    duration = timeit.default_timer() - start

    # 총 실행 시간
    print('Total Time', duration) # Total Time 1.591328305
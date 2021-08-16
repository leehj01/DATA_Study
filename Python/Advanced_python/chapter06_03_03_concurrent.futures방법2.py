# 동시성 개념
# 비동기 작업
# ThreadPool 실습 / ProcessPool 실습 / block , non-block 개념

# chapter 06-03-03 파이썬 심화
# Future 동시성
# 비동기 작업 실행
# 지연 시간(Block) CPU 및 리소스 낭비 방지 -> Network I/O 관련 작업에 동시성 활용 권장
# 적합한 작업일 경우 순차 진행보다 압도적으로 성능 향상

# 실습 대상 3가지 경우

# 순차 실행
# concurrent.futures 방법1
# concurrent.futures 방법2


# resouces의 nations 데이터 사용 - 내가 원하는 국가에 대해서만, 별도의 파일로 만들어서 작업하고 싶다!

# concurrent.futures 방법1( ThreadPoolExecutor , ProcessPoolExecutor)
# map()
# 서로 다른 스레드 또는 프로세스에서 실행 가능
# 내부 과정을 알 필요 없으며, 파이썬이 고수준의 추상화 인터페이스 제공

# 파이썬의 Global Interpreter Lock (GIL) 이란?
# Gil은 한번에 하나 스레드만 수행 할 수 있게 인터프리터 자체에서 락을 거는 것 ( 병목현상이나, 스레드 충돌로 무한 루프로 빠질 가능성 이 있기 때문에 )
# 그래서, 파일을 읽고 쓰는 거는 하나의 쓰레드에서 작업을 하고 이후에 멀티 쓰레드를 하는것이 빠름

import os
import time
import sys
import csv
from concurrent import futures

# 3.x 이후에는 비동기적으로 고수준의 모델을 가져올수 있다.

# 순차실행 예제

# 국가 정보
NATION_LS = ('Singaproe Germany Korea Israel Norway Italy Canada France Spain').split()# 대문자로 적어줘서 바뀌지 않는 정보라는 의미를 가지게 함
# print(NATION_LS)

# 초기 csv 위치
TARGET_CSV = 'resources/nations.csv'

# 저장 폴더 위치
DEST_DIR = 'result'

# csv 헤더 기초 정보
HEADER = ['Region','Country','Item Type','Sales Channel','Order Priority','Order Date','Order ID','Ship Date',
          'Units Sold','Unit Price','Unit Cost','Total Revenue','Total Cost','Total Profit']

# 국가별 csv 파일 저장
def save_csv(data, filename):
    # 최종 경로 생성
    path = os.path.join(DEST_DIR, filename)

    with open(path, 'w', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=HEADER)
        # HEADER write
        writer.writeheader()
        # Dict to CSV Write
        for row in data:
            writer.writerow(row)

# 국가별 분리 - 읽고
def get_sales_data(nt):
    with open(TARGET_CSV, 'r') as f:
        reader = csv.DictReader(f)
        # Dict 을 리스트로 적재
        data = []
        # Header
        # print(reader.fieldnames)
        for r in reader:
            # OrderedDict
            # print(r)
            # 조건에 맞는 국가만 삽입
            if r['Country'] == nt :
                data.append(r)
    return data

# 중간 상환 출력
def show(text):
    print(text, end=' ')
    # 중간 출력 ( 버퍼 비우기 )
    sys.stdout.flush()

# 국가별 분리 함수 실행
def seperate_many(nt):
    # 분리 데이터
    data = get_sales_data(nt)

    # 상황 출력
    show(nt)

    # 파일 저장
    save_csv(data, nt.lower() + '.csv')

    return nt


# 시간 측정 및 메인 함수
def main(seperate_many):
    # worker 개수 구하기 : 너무 많아도 좋지 않음, 운영체재에서 그렇게 허락도 하지 않음
    worker = min(20, len(NATION_LS)) # NATION_LS 는 9개 이므로, 결과적으로 쓰레드는 9개이다.

    #  성능 측정을 위한 시작시간
    start_tm = time.time()

    #결과 건수
    # ThreadPoolExecutor : GIL 에 종속 # 12 초 정도 - 쓰레드를 쓴것
        # I/O 작업을 분리 해서, 변수에 담아두고 9번을 반복하는 작업에만 쓰레드를 쓰면 빨라
    # ProcessPoolExecutor : GIL 을 우회하고 변경후엔 # 4.28s 만에 실행됨! 빠르게 실행되지만, cpu 활용도가 100%로 치솟음(안좋음...)
    # 언제, 코루틴을 쓸지, 쓰레드를 쓸지, 프로세싱을 할지 고민해야함
    # 멀티 프로세싱을 아래처럼 해버리면, cpu 가 올라가버리기 때문에, 극단적으로 일어나서 안좋음 - 단기간의 연산에는 쓰는 것이 좋고, 잘 써야함
        # os.cpu_count() 에서 내가 가지고 있는 cpu 의 갯수를 찾아서 넣어줌
    # 쓰레드는 cpu가 많이 잡아 먹지 않음

    # futures
    futures_list = []

    with futures.ThreadPoolExecutor(worker) as excutor: # 몇개의 일꾼을 사용할건지! 에 대한 매개 변수를 받음
        # map 을 사용하면, 각각의 값이 에러가 발생했는지, 취소가 됬는지 확인할 수 가 없음 - 이것을 세부적으로 볼수 있는 방법도 존재 -> submit을 이용하기
        # submit -> Callable 객체를 스케줄링(실행 예약 해주는 역할) -> Future ( 하나의 task(job)으로 반환 )
        # Map이나 submit 의 속도차이는 없다. 어차피 스레드를 활용하는 것 이기 때문에,
        # future -> result(), done() ( 각각의 일이 잘 했는지 ) , as_complete() (모든 일이 끝날때까지 기다리기) 를 주로 사용
        for nt in sorted(NATION_LS):
            # future 반환
            future = excutor.submit(seperate_many, nt)
            # 스케쥴링
            futures_list.append(future)
            # 출력 1
            # print('Scheduled for {} : {}'.format(nt, future))
            # print()

            # 스케쥴링한 것을 as_compledted 를 하면서, 결과를 볼수 있다.
        for future in futures.as_completed(futures_list): # future_list에 담아두는 작업이 끝날 때까지
            result = future.result() # 하나의 일이 끝났으면, result 를 반환해줌
            done = future.done() # 하나의 일이 잘 끝났는지
            cancel = future.cancel() # 일이 취소가 되지 않았는지 에 대한 결과값
            cancelled = future.cancelled

            # future 결과 확인
            print('Future Result : {}, Done : {}'. format(result, done))
            # print('Future Cancelled : {}'.format(cancel))
            print('Future Cancelled : {}'.format(cancelled))


    # 종료 시간
    end_tm = time.time() - start_tm

    msg = '\n{} csv separated in {:.2f}s'
    # 최종 결과출력
    print(msg.format(list(futures_list), end_tm))

# 실행
if __name__ == '__main__': # 이것이 있어야, 불필요한 것이 실행되지 않음
    main(seperate_many)

    # Spain Singaproe Norway France Italy Canada Korea Israel Germany
    # <generator object Executor.map.<locals>.result_iterator at 0x10f12edd0> csv separated in 12.81s
    # 결과가 하나씩 나오는 느낌이 아니라, 품고있다가 툭 나오는 느낌으로 나온다.
    # 순차적으로 했을때(단일 스레드로 할 때보다)보다 속도가 빨라지지 않는다. -> 그 이유는 file I/O
    # 하나의 파일에 한번에 접근하다보니깐( context switching 비용 ), GIL 때문에, 하나만 수행할 수 있게 lock이 걸림
    # 이러한 문제때문에 파일을 읽고 쓰는 문제에서는 멀티 프로세싱을 사용하는 것이 좋다.
    # 따라서, 파일을 읽는 것은 따로 작업해서, 불러놓고선 9개의 작업을 동시에 하는 것이 좋다.
    # 하지만, 다른방법으로는 GIL을 우회하는 방법으로 with futures.ThreadPoolExecutor(worker) as excutor: 이것을
    # ProcessPoolExecutor으로 바꾸는 방법이다.
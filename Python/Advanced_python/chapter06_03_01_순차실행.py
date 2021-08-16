# 동시성 개념
# 비동기 작업
# ThreadPool 실습 / ProcessPool 실습 / block , non-block 개념

# chapter 06-03-01 파이썬 심화
# Future 동시성
# 비동기 작업 실행
#
# 적합한 작업일 경우 순차 진행보다 압도적으로 성능 향상

# 실습 대상 3가지 경우

# 순차 실행
# concurrent.futures 방법1
# concurrent.futures 방법2


# resouces의 nations 데이터 사용 - 내가 원하는 국가에 대해서만, 별도의 파일로 만들어서 작업하고 싶다!

# 순차 실행

import os
import time
import sys
import csv

# 순차실행 예제

# 국가 정보
NATION_LS = ('Singaproe Germany Korea Israel Norway Italy Canada France Spain').split()# 대문자로 적어줘서 바뀌지 않는 정보라는 의미를 가지게 함
print(NATION_LS)

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
def seperate_many(nt_list):
    for nt  in sorted(nt_list):
        # 분리 데이터
        data = get_sales_data(nt)

        # 상황 출력
        show(nt)

        # 파일 저장
        save_csv(data, nt.lower() + '.csv')

    return len(nt_list)



# 시간 측정 및 메인 함수
def main(seperate_many):
    #  성능 측정을 위한 시작시간
    start_tm = time.time()
    #결과 건수
    result_cnt = seperate_many(NATION_LS)
    # 종료 시간
    end_tm = time.time() - start_tm

    msg = '\n{} csv separated in {:.2f}s'
    # 최종 결과출력
    print(msg.format(result_cnt, end_tm))

# 실행
if __name__ == '__main__': # 이것이 있어야, 불필요한 것이 실행되지 않음
    main(seperate_many)



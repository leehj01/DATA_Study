# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## 1. TF-IDF(단어 빈도-역 문서 빈도, Term Frequency-Inverse Document Frequency)

# +
doc1 = '''
지능 지수 라는 말 들 어 보 셨 을 겁니다 . 여러분 의 지성 을 일컫 는 말 이 죠 . 그런데 심리 지수 란 건 뭘까요 ? 사람 들 이 특정 한 식 으로 행동 하 는 이유 에 대해 여러분 은 얼마나 알 고 계시 나요 ? 또 타인 이나 심지어 여러분 의 행동 을 예측 하 는 일 은 얼마나 잘 하 시 나요 ? 또 , 심리학 에 대해 갖춘 지식 중 에서 어느 정도 나 잘못 된 것 일까요 ? 심리학 에 관한 열 가지 신화 를 통해 잘못 된 것 들 을 알아보 도록 하 죠 . 여러분 은 한 번 쯤 들 어 보 셨 을 법 한 것 은 자신 들 의 심리학 에 대해 고려 할 때 , 거의 항상 남자 는 화성 에서 왔 고 , 여자 는 금성 에서 온 것 같 다고 합니다 . 하지만 실제로 남자 와 여자 는 얼마나 다른 걸까요 ? 이 를 알아보 기 위해 , 일단 남녀 사이 에 확실 하 게 차이 나 는 것 을 살펴보 고 심리학 적 인 성별 간 의 차이점 을 동일 한 척도 상 에서 대비 해 보 도록 하 겠 습니다 . 남자 와 여자 간 에 실제로 차이 나 는 능력 중 하나 는 그 들 이 공 을 얼마나 멀리 던질 수 있 느냐 하 는 것 입니다 . 여기 남자 들 의 데 이타 를 보 시 면 , 정상 분포 곡선 이 라는 걸 볼 수 있 습니다 . 남자 들 소수 는 정말 멀리 던지 고 , 남자 들 소수 는 멀리 던지 지 못하 지만 , 남자 들 대부분 은 평균 적 인 거리 를 던졌 습니다 . 여자 들 도 역시 비슷 한 분포 상태 를 보입니다 만 사실 남녀 사이 엔 커다란 차이 가 있 습니다 . 사실 , 평균 수준 의 남자 라면 모든 여성 중 대략 98 % 보다 더 멀리 던질 수 있 거든요 . 이 와 동일 하 게 표준 화 된 척도 상 에서 심리학 에서 말 하 는 성별 간 의 차이 를 살펴 봅시다 . 심리학자 라는 여러분 에게 말 하 길 남자 들 의 공간 지각 능력 이 여자 들 보다 뛰어나 다고 할 겁니다 . 예 를 들 어 , 지도 읽 는 능력 같 은 건데 , 맞 는 말 입니다 . 하지만 그 차이 의 정도 를 살펴봅시다 . 아주 작 죠 . 두 선 이 너무 근접 해서 거의 겹칠 정도 입니다 .
'''

doc2 = '''
최상 의 제시 유형 은 학습 자 에 좌우 되 는 것 이 아니 라 학습 해야 할 내용 에 따라 좌우 됩니다 . 예 를 들 어 여러분 이 운전 하 기 를 배울 때 실제로 몸 으로 체감 하 는 경험 없이 누군가 가 어떻게 할 지 이야기 하 는 것 을 듣 는 것 만 으로 배울 수 있 습니까 ? 연립 방정식 을 풀 어야 하 는데 종이 에 쓰 지 않 고 머리 속 에서 말 하 는 것 으로 풀 수 가 있 을까요 ? 또는 만일 여러분 이 체감 형식 의 학습 자 유형 이 라면 , 건축학 시험 을 해석 적 춤 을 이용 하 여 수정 할 수 있 을까요 ? 아니 죠 ! 배워야 할 내용 을 제시 된 유형 에 맞추 어야 합니다 , 당신 에게 맞추 는 게 아니 라요 . 여러분 들 상당수 가 " A " 급 의 우등 생 이 라는 걸 아 는데 , 조만간 중등 학력 인증 시험 ( GCSE ) 결과 를 받 게 되 시 겠 네요 . 그런데 , 만일 , 여러분 들 이 희망 했 던 성적 을 받 지 못하 게 된다 해도 여러분 들 의 학습 방식 을 탓 해서 는 안 되 는 겁니다 . 여러분 이 비난 할 수 있 는 한 가지 는 바로 유전자 입니다 . 이건 최근 에 런던 대학교 ( UCL ) 에서 수행 했 던 연구 결과 는 여러 학생 들 과 그 들 의 중등 학력 인증 시험 결과 사이 의 차이 중 58 % 는 유전 적 인 요인 으로 좁혀졌 습니다 . 매우 정밀 한 수치 처럼 들립니다 . 그러면 어떻게 알 수 있 을까요 ? 유전 적 요인 과 환경 적 요인 의 상대 적 기여 도 를 알 고 싶 을 때 우리 가 사용 할 수 있 는 방식 은 바로 쌍둥이 연구 입니다 . 일 란 성 쌍생아 의 경우 환경 적 요인 과 유전 적 요인 모두 를 100 % 똑같이 공유 하 게 되 지만 이란 성 쌍생아 의 경우 는 100 % 동일 한 환경 을 공유 하 지만 유전자 의 경우 여타 의 형제자매 들 처럼 50 % 만 공유 하 게 됩니다 . 따라서 일 란 성 쌍둥이 와 이란 성 쌍둥이 사이 의 인증 시험 결과 가 얼마나 비슷 한지 비교 해 보 고 여기 에 약간 의 수학 적 계산 을 더하 게 되 면 그 수행 능력 의 차이 중 어느 정도 가 환경 적 요인 의 탓 이 고 어느 정도 가 유전자 탓 인지 를 알 수 있 게 됩니다 .
'''

doc3 = '''
그러나 이 이야기 는 세 가지 이유 로 인해 신화 입니다 . 첫째 , 가장 중요 한 건 실험실 가운 은 흰색 이 아니 라 회색 이 었 다 라는 점 이 죠 . 둘째 , 참 여자 들 은 실험 하 기 전 에 와 참여 자 들 이 걱정 을 표현 할 때 마다 상기 시키 는 말 을 들 었 는데 , 전기 충격 이 고통 스럽 기 는 하 지만 , 치명 적 이 지 는 않 으며 실제로 영구 적 인 손상 을 남기 는 일 은 없 을 거 라는 것 이 었 습니다 . 셋째 , 참 여자 들 은 단지 가운 을 입 은 사람 이 시켜 전기 충격 을 주지 는 않 았 죠 . 실험 이 끝나 고 그 들 의 인터뷰 를 했 을 때 모든 참여 자 들 은 강한 신념 을 밝혔 는데 , ' 학습 과 처벌 ' 연구 가 과학 적 으로 가치 있 는 목적 을 수행 했 기 때문 에 비록 동료 참여 자 들 에게 가해진 순간 적 인 불편 함 에 반해서 과학 을 위해서 오래 남 을 성과 를 얻 을 것 이 라고 말 이 죠 . 그러 다 보 니 제 가 이야기 를 한 지 벌써 12 분 이 되 었 습니다 . 여러분 들 중 에 는 아마 거기 앉 아서 제 이야기 를 들으시는 동안 저 의 말투 와 몸짓 을 분석 하 면서 제 가 말 하 는 어떤 것 을 인지 해야 할까 해결 하 려고 하 셨 을 겁니다 , 제 가 진실 을 이야기 하 는 지 , 또는 거짓말 을 하 고 있 는 것 인지 말 이 죠 . 만일 그러 셨 다면 , 아마 지금 쯤 완전히 실패 하 셨 을 겁니다 . 왜냐하면 우리 모두 가 사람 이 말 하 는 패턴 과 몸짓 으로 도 거짓말 여부 를 알아내 는 것 이 가능 하 다고 생각 하 지만 , 오랜 세월 수백 회 에 걸쳐 행해진 실제 심리 검사 의 결과 를 보 면 우리 들 모두 는 , 심지어 경찰관 이나 탐정 들 을 포함 해서 도 기본 적 으로 몸짓 과 언어 적 패턴 으로 거짓말 을 탐지 하 는 것 은 운 에 맞 길 수 밖 에 는 없 는 것 입니다 . 흥미 롭 게 도 한 가지 예외 가 있 는데요 : 실종 된 친척 을 찾 아 달 라고 호소 하 는 TV 홍보 입니다 .
'''

# +
list_ = ['a', 'ab', 'a', 'c']

dict_ = {}
for i in list_:

    if dict_.get(i) is None:
        dict_[i] = + 1

    else:
        dict_[i] = 1 + dict_[i]
# -

dict_['d'] = dict_.get('d', 3)

dict_

# +
import pandas as pd


# TF 구하는 함수
def get_term_frequency(document, word_dict=None):
    if word_dict is None:
        word_dict = {}

    words = document.split()

    for w in words:
        word_dict[w] = 1 + (0 if word_dict.get(w) is None else word_dict[w])

    return pd.Series(word_dict).sort_values(ascending=False)


get_term_frequency(doc1)


# +
# DF 구하기
def get_document_frequency(documents):
    dicts = []
    vocab = set([])
    df = {}

    for d in documents:  # 문서에 있는 단어들의 모음집을 만들어줌.
        tf = get_term_frequency(d)
        dicts += [tf]
        vocab = vocab | set(tf.keys())

    for v in list(vocab):  # vocab 안에 몇개가 들어있는지, 즉 문서에 있는지를 확인해서 갯수 카운드
        df[v] = 0
        for dict_d in dicts:
            if dict_d.get(v) is not None:
                df[v] += 1

    return pd.Series(df).sort_values(ascending=False)


get_document_frequency([doc1, doc2])


# -

# TF-IDF 구하기
def get_tfidf(docs):
    vocab = {}
    tfs = []

    for d in docs:
        vocab = get_term_frequency(d, vocab)  # tf 를 구하는 함수 사용
        tfs += [get_term_frequency(d)]  # 문서들의 tf을 리스트로 모두 모아놓음

    df = get_document_frequency(docs)  # df를 구하는 함수 사용

    from operator import itemgetter  # 정렬하는 함수
    import numpy as np

    stats = []
    for word, freq in vocab.items():
        tfidfs = []
        for idx in range(len(docs)):
            if tfs[idx].get(word) is not None:
                tfidfs += [tfs[idx][word] * np.log(len(docs) / df[word])]
                #  구할 때, log를 취해줘야 idf값이 기하급수적으로 커지는 것을 방지 할 수있음

            else:
                tfidfs += [0]

        stats.append((word, freq, *tfidfs, max(tfidfs)))

    return pd.DataFrame(stats, columns=('word',
                                        'frequency',
                                        'doc1',
                                        'doc2',
                                        'doc3',
                                        'max')).sort_values('max', ascending=False)


get_tfidf([doc1, doc2, doc3])

# ## 다른 방법으로 TF-IDF 구하기

docs = [
    '먹고 싶은 사과',
    '먹고 싶은 바나나',
    '길고 노란 바나나 바나나',
    '저는 과일이 좋아요'
]
vocab = list(set(w for doc in docs for w in doc.split()))
vocab.sort()

# +
# 다른 방법으로 TF, IDF, TF-IDF 값을 구하기

import pandas as pd
from math import log

N = len(docs)  # 총 문서의 수


def tf(t, d):
    return d.count(t)


result = []
for i in range(N):  # 각 문서에 대해서 아래 명령을 수행
    result.append([])
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]
        result[-1].append(tf(t, d))

tf_ = pd.DataFrame(result, columns=vocab)
tf_


# +
def idf(t):
    df = 0
    for doc in docs:
        df += t in doc
    return log(N / (df + 1))


result = []
for j in range(len(vocab)):
    t = vocab[j]
    result.append(idf(t))

idf_ = pd.DataFrame(result, index=vocab, columns=["IDF"])
idf_


# +
def tfidf(t, d):
    return tf(t, d) * idf(t)


result = []
for i in range(N):
    result.append([])
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]

        result[-1].append(tfidf(t, d))

tfidf_ = pd.DataFrame(result, columns=vocab)
tfidf_
# -

# ## sklearn으로 TF와 TF-IDF 을 구하기
# - 단, 사이킷런의 TF-IDF는 보편적인 TF-IDF 식에서 조정된 식음
#     - IDF의 로그항의 분자에 1을 더해주며, 로그항의 1을 더해줌
#     - TF-IDF에 L2정규화 방법으로 값을 조정

from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    'you know I want your love',
    'I like you',
    'what should I do ',
]
vector = CountVectorizer()
print(vector.fit_transform(corpus).toarray())  # 코퍼스로부터 각 단어의 빈도 수를 기록한다.
print(vector.vocabulary_)  # 각 단어의 인덱스가 어떻게 부여되었는지를 보여준다.

from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    'you know I want your love',
    'I like you',
    'what should I do ',
]
tfidfv = TfidfVectorizer().fit(corpus)
print(tfidfv.transform(corpus).toarray())
print(tfidfv.vocabulary_)

from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    doc1, doc2, doc3
]
tfidfv = TfidfVectorizer().fit(corpus)
print(tfidfv.transform(corpus).toarray())
print(tfidfv.vocabulary_)


# ## TF 행렬 만들기

# +
def get_tf(docs):
    vocab = {}
    tfs = []

    for d in docs:
        vocab = get_term_frequency(d, vocab)
        tfs += [get_term_frequency(d)]

    from operator import itemgetter
    import numpy as np

    stats = []
    for word, freq in vocab.items():
        tf_v = []
        for idx in range(len(docs)):
            if tfs[idx].get(word) is not None:
                tf_v += [tfs[idx][word]]
            else:
                tf_v += [0]

        stats.append((word, freq, *tf_v))

    return pd.DataFrame(stats, columns=('word',
                                        'frequency',
                                        'doc1',
                                        'doc2',
                                        'doc3',
                                        )).sort_values('frequency', ascending=False)


get_tf([doc1, doc2, doc3])
# -

# ## Based on Context Window ( Co- occurrence )
# - 윈도우 기반 동시 등장 행렬
# - 단어별로 윈도우 내에 속해 있는 이웃 단어들의 출현 빈도를 세어 행렬로 나타내는 것
# - window size 는 하이퍼파라미터 임. 너무 큰 크기를 가지면 현재 단어와 관계가 없는 단어들의 출현 빈도를 셈 따라서 적절한 크기를 설정해야함.

# +
with open('ted.txt', encoding='utf-8-sig') as f:
    lines = [l.strip() for l in f.read().splitlines() if l.strip()]

text = []
for i in lines:
    line = i.split('. ')
    for j in line:
        text.append(j)

# +
from collections import defaultdict
import pandas as pd


# 함께 출현한 빈도수를 나타내는 함수
def get_context_counts(lines, w_size=2):
    co_dict = defaultdict(int)

    for line in lines:
        words = line.split()

        for i, w in enumerate(words):
            l_ind = max(i - w_size + 1, 0)
            r_ind = i + w_size
            for c in words[l_ind: r_ind]:
                if w != c:
                    co_dict[(w, c)] += 1

    return pd.Series(co_dict)


co_dict = get_context_counts(text)
co_dict
# -

tfs = get_term_frequency(' '.join(text))
tfs


# +
def co_occurrence(co_dict, vocab):
    data = []

    for word1 in vocab:
        row = []

        for word2 in vocab:
            try:
                count = co_dict[(word1, word2)]
            except KeyError:
                count = 0
            row.append(count)

        data.append(row)

    return pd.DataFrame(data, index=vocab, columns=vocab)


co = co_occurrence(co_dict, tfs.index[:1000])
print(co)

# +
import torch

torch.save(co, 'co.pth')
co = torch.load('co.pth')
co
# -

# ## 4문장으로만 다시 코드만 돌려봄

tem = ['I like to watch movies', 'I like icecream', 'I enjoy flying', 'I like to eat desert']

# +
co_dict = get_context_counts(tem, w_size=3)
print(co_dict)
tfs = get_term_frequency(' '.join(tem))
coc = co_occurrence(co_dict, tfs.index)
print(coc)

import torch

torch.save(coc, 'coc.pth')
coc = torch.load('coc.pth')
coc
# -







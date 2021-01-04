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

# ### 동시 발생 단어들을 활용하는 방법

# +

lines = """
I enjoy flying .
I like NLP .
I like deep learning .
"""

lines = lines.strip().split('\n')


def get_context_counts(lines, w_size=2):
    co_dict = defaultdict(int)
    
    for line in lines:
        words = line.split()
        
        for i, w in enumerate(words):
            l_ind = max(i-w_size+1, 0)
            r_ind = i+w_size
            for c in words[l_ind:r_ind]:
                if w != c:
                    co_dict[(w, c)] += 1
            
    return pd.Series(co_dict)


co_dict = get_context_counts(lines)

def get_term_frequency(document, word_dict=None):
    if word_dict is None:
        word_dict = {}
    words = document.split()

    for w in words:
        word_dict[w] = 1 + (0 if word_dict.get(w) is None else word_dict[w])

    return pd.Series(word_dict).sort_values(ascending=False)

tfs = get_term_frequency(' '.join(lines))
stanford_index = ['I', 'like', 'enjoy', 'deep', 'learning', 'NLP', 'flying', '.']
tfs = tfs[stanford_index]


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
        

# -

# ## 유사도 기반의 선택 선호도 예제
# ### 예제를 위한 데이터셋 만들기

# +
# # !git clone https://github.com/e9t/nsmc  
#  네이버 영화 평점 데이터 셋 

# +
# %%time
# 데이터 불러오기
import pandas as pd
import torch
corpus = pd.read_csv('./nsmc/ratings_train.txt', sep='\t').document.values[:10000]

# 데이터를 토크나이즈 하기 - POS와 단어로 나눔
from konlpy.tag import Kkma

tagger = Kkma()

results = []
for line in corpus:
    pos_result = tagger.pos(line)
    results.append(pos_result)
    
# 토크나이즈 한 것들을 다시, 문장 형태로 해줌 
corpus = [' '.join([c[0] for c in line]) for line in results]
# -

# ### 코퍼스를 받아 문장 내에서 술어, 표제어(nng)를 찾아 Seen_r(w)함수를 구성함

# +
from konlpy.tag import Mecab

def count_seen_geadwords(lines, predicate= "VV", headword= 'NNG'):
    """
    코퍼스를 받고 문장 내에서 술어(동사, W)와 표제어(명사, NNG)를 찾
    Seen_R(w) 함수를 구성
    """
    
    tagger= Kkma()
    seen_dict = {}
    
    for line in lines:
        pos_result = tagger.pos(line)
        
        word_h, word_p = None, None
        for word, pos in pos_result :
            if pos == predicate or pos[:3] == predicate + '+':
                word_p = word
                break
                
            if pos == headword:
                word_h = word
                
            if word_h is not None and word_p is not None:
                seen_dict[word_p] = [word_h] + ([] if seen_dict.get(word_p) is None else seen_dict[word_p])
                
            
        return seen_dict


# -

# 스터디원 코드 
def count_seen_headwords(lines, tagger=None, predicate='VV', headword='NNG'):
    """
    코퍼스를 받고 문장 내에서 술어(동사, W)와 표제어(명사, NNG)를 찾
    Seen_R(w) 함수를 구성
    """
    seen_dict = {}
    for line in lines:
        if tagger:
            assert hasattr(tagger, 'pos'), 'tagger must have a "pos" method!'
            pos_result = tagger.pos(line)
        else:
            pos_result = line
        word_h, word_p = None, None
        for word, pos in pos_result:
            if pos == predicate or pos[:3] == predicate + '+':
                word_p = word
                break
            if pos == headword:
                word_h = word
        if word_h is not None and word_p is not None:
            seen_dict[word_p] = [word_h] + \
                ([] if seen_dict.get(word_p) is None else seen_dict[word_p])
    return seen_dict


# ### 주어진 술어와 표제어에 대해서 선택 관련도 점수를 구하는 함수 
# - 단어사이의 유사도를 구하기 위해서 이전에 구성한 특징 벡터들을 담은 판다스 데이터 프레임을 받음 
# - 그럼 metric으로 주어진 함수를 통해 유사도를 계산함 

def get_selectional_association(
        predicate, headword, lines, dataframe, metric):
    """
    주어진 술어와 표제어에 대해서 선택 관련도 점수를 계산
    """
    v1 = torch.FloatTensor(dataframe.loc[headword].values)
    seens = seen_headwords[predicate]
    total = 0
    for seen in seens:
        try:
            v2 = torch.FloatTensor(dataframe.loc[seen].values)
            total += metric(v1, v2)
        except:
            pass
        
    return total


# + active=""
# # 스터디원 코드 
# def get_selectional_association(
#         predicate, headword, lines, co, metric, seen_headwords):
#     """
#     주어진 술어와 표제어에 대해서 선택 관련도 점수를 계산
#     """
#     v1 = torch.FloatTensor(co.loc[headword].values)
#     seens = seen_headwords[predicate]
#     total = 0
#     for seen in seens:
#         try:
#             v2 = torch.FloatTensor(co.loc[seen].values)
#             total += metric(v1, v2)
#         except:
#             pass
#     return total
# -

# ### 앞의 함수들을 활용하여 주어진 술어에 대해 올바른 headword를 고르는 wsd함수

# +
from functools import partial

def wsd(predicate, headwords):
    selectional_associations = []
    for h in headwords:
        selectional_associations += [get_selectional_association(predicate, h, lines, co, get_cosine_similarity)]
    print(selectional_associations)


# + active=""
# from functools import partial
#
# def wsd_base(predicate, headwords, lines, co, similarity_func, seen_headwords):
#     selectional_associations = []
#     for h in headwords:
#         selectional_associations = selectional_associations + \
#             [get_selectional_association(
#                 predicate, h, lines, co, similarity_func, seen_headwords)]
#     print(selectional_associations)
#     
#     
# param_dict = dict(
#     lines=lines,
#     co=co,
#     similarity_func=get_cosine_similarity,
#     seen_headwords=seen_headwords
# )
# wsd = partial(wsd_base, **param_dict)
# -

# ### 실행함수들  

def get_cosine_similarity(x1, x2):
    return (x1 * x2).sum() / ((x1**2).sum()**.5 * (x2**2).sum()**.5)


# +
# %%time
seen_headwords = count_seen_headwords(results)
co_dict = get_context_counts(corpus)
tfs = get_term_frequency(' '.join(corpus))
co = co_occurrence(co_dict, tfs.index[:1000])
torch.save(co, 'co.pth')

wsd('보', ['동화', '영화','배우' ])

# 보다라는 동사에 대한 유사도 

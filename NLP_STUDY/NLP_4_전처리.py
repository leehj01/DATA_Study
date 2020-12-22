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

# ## 1. 분절
# ### 1.1 문장 단위 분절

import sys, fileinput, re
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

# +

import sys, fileinput, re
from nltk.tokenize import sent_tokenize

if __name__ == "__main__":
    for line in fileinput.input("input.txt", openhook=fileinput.hook_encoded("utf-8")):
        #         print(line)
        if line.strip() != "":  # 이건 굳이 없어도 되지만. .. 넣은 것 같음
            line = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', line.strip())

            sentences = sent_tokenize(line.strip())  # 이 함수를 사용하면, 문장단위로 나누어주고 리스트 형식으로 만들어 줌
            print(sentences, '\n')

            for s in sentences:
                if s != "":
                    #                     sys.stdout.write(s + "\n")
                    print(s)

fileinput.close()
# -

for line in fileinput.input("input.txt", openhook=fileinput.hook_encoded("utf-8")):
    sentences = sent_tokenize(line.strip())
    for i in sentences:
        print(i)

# ###  1.2. 문장 합치기 및 분절 예제

import sys, fileinput, re
from nltk.tokenize import sent_tokenize

# +
import sys, fileinput
from nltk.tokenize import sent_tokenize

if __name__ == "__main__":
    buf = []

    for line in fileinput.input("input2.txt", openhook=fileinput.hook_encoded("utf-8")):
        if line.strip() != "":
            buf += [line.strip()]
            #             print(buf)
            sentences = sent_tokenize(" ".join(buf))  # 문장을 기준으로 더해준다.?
            #             print(sentences)  # buf와 sentence의 결과가 같다.. ?

            if len(sentences) > 1:
                buf = sentences[1:]
                #                 print(buf)
                #                 print(sentences)

                sys.stdout.write(sentences[0] + '\n')

    sys.stdout.write(" ".join(buf) + "\n")

# -

# ### 1.3. 한국어 분절  ( Tokenization )
# - 기본적으로 어근과 접사를 분리하는 역할을 하며, 나아가 잘못된 띄어쓰기에 대해 올바르게 교정하는 역할을 함.

# +
from konlpy.tag import Kkma

kkma = Kkma()

line = '둥둥섬의 왕위 계승자로 태어난 수사자 라이언. 무뚝뚝한 표정과는 다르게 배려심이 많고 따뜻한 리더십을 가지고 있습니다.'
tokenized = kkma.pos(line)
print(tokenized)
# -
# ## 2. BPE ( 바이트 페어 인코딩 : Byte Pair Encoding )
# ### 2.1. BPE ( 바이트 페어 인코딩 : Byte Pair Encoding ) 의 작동 방법
# - 연속적으로 가장 많이 등장하는 글자의 쌍을 찾아서 하나의 글자로 병합하는 방식을 수행

# +
'가나나다다다다가나나다다'

# 가장 많이 등장하는 글자는 '다다'  -> A로 치환

'가나나AA가나나A'

# 그 다음으로 많이 등장하는 글자 '가나나'  -> B 치환
'BAABA'

# 이제 더이상 병합할 쌍이 없으므로 종료됨
# -

# ### 2.2. 자연어 처리에서 BPE
# - 자연어 처리에서의 BPE는 단어를 분리한다는 의미임. 즉, 글자 단위에서 점차적으로 단어 집합을 만들어 내는 Bottom up 방식의 접근을 사용함
# -  https://arxiv.org/pdf/1508.07909.pdf
# - BPE의 특징은 알고리즘의 동작을 몇 회 반복(iteration)할 것인지를 사용자가 정한다는 점입니다. 여기서는 총 10회를 수행한다고 가정합니다. 다시 말해 가장 빈도수가 높은 유니그램의 쌍을 하나의 유니그램으로 통합하는 과정을 총 10회 반복합니다. 위의 딕셔너리에 따르면 빈도수가 현재 가장 높은 유니그램의 쌍은 (e, s)입니다.

# +
import re, collections
from IPython.display import display, Markdown, Latex

num_merges = 4

dictionary = {'w a l k </w>': 5,
              'w a l k e d </w>': 2,
              'd r k i n g </w>': 6,
              'e a t i n g </w>': 3
              }


def get_stats(dictionary):
    # 유니그램의 pair들의 빈도수를 카운트
    pairs = collections.defaultdict(int)
    for word, freq in dictionary.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    print('현재 pair들의 빈도수 :', dict(pairs))
    return pairs


def merge_dictionary(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out


bpe_codes = {}
bpe_codes_reverse = {}

for i in range(num_merges):
    display(Markdown("### Iteration {}".format(i + 1)))
    pairs = get_stats(dictionary)
    best = max(pairs, key=pairs.get)
    dictionary = merge_dictionary(best, dictionary)

    bpe_codes[best] = i
    bpe_codes_reverse[best[0] + best[1]] = best

    print("new merge: {}".format(best))
    print("dictionary: {}".format(dictionary))
# -

print(bpe_codes)

# ## SentencePiece

# Conda 환경이여서 conda install
# !conda install -c powerai sentencepiece -y
# python 환경이면 pip install
# !pip install sentencepiece -y

# ## 학습시키기
# **-------------------------------------------학습 파라미터 이름과 의미----------------------------------------**
# * input : 학습시킬 파일 (텍스트파일만)
# * model_prefix : 만들어질 모델 이름 마음대로 커스텀 가능
# * vocab_size : 단어 집합의 크기
#     * 커질수록 성능이 좋아지고 모델 파라미터수가 증가함--->시간이오래걸릴듯함
# * model_type : 사용할 모델 (unigram(default), bpe, char, word)
# * max_sentence_length: 문장의 최대 길이
# * pad_id, pad_piece: pad token id, 값
# * unk_id, unk_piece: unknown token id, 값
# * character_coverage = 1.0 # to reduce character set
#   - 중국어, 일본어 같이 자소단위로 이루어진 언어(rich character set)에서는 0.9995 다른언어(small character set)에 대해서 1로 설정
# * bos_id, bos_piece: begin of sentence token id, 값
# * eos_id, eos_piece: end of sequence token id, 값
# * user_defined_symbols: 사용자 정의 토큰 내가 원하는 형태소만 가져오기
#
# **-----------------------------------------------------------------------------------------------------------**

# +
# %%time
import sentencepiece as spm

input_file = 'kakao_title.txt'
model_name = 'subword_tokenizer_kor'  # 모델이름 (맘대로 커스텀가능)
vocab_size = 32000
model_type = 'bpe'
user_defined_symbols = '[PAD],[UNK],[CLS],[SEP],[MASK],[UNK1],[UNK2],[UNK3],[UNK4]'

templates = '--input={} --model_prefix={} --vocab_size={} --user_defined_symbols={} --model_type={}'

template = templates.format(input_file, model_name, vocab_size, user_defined_symbols, model_type)

# template을 Train시켜준다.
spm.SentencePieceTrainer.Train(template)
# -

# ## 만들어진모델을 테스트해보자
# **-----------------------------------------테스트 함수-------------------------------------**
# * GetPieceSize() : 단어 집합의 크기를 확인합니다. = vocab_size
# * encode_as_pieces : 문장을 입력하면 서브 워드 시퀀스로 변환합니다. **★이걸로 형태소분절**
# * encode_as_ids : 문장을 입력하면 정수 시퀀스로 변환합니다.
# * idToPiece : 정수로부터 맵핑되는 서브 워드로 변환합니다.
# * PieceToId : 서브워드로부터 맵핑되는 정수로 변환합니다.
# * DecodeIds : 정수 시퀀스로부터 문장으로 변환합니다.
# * DecodePieces : 서브워드 시퀀스로부터 문장으로 변환합니다.
# * encode : 문장으로부터 인자값에 따라서 정수 시퀀스 또는 서브워드 시퀀스로 변환 가능합니다.
#
# **-----------------------------------------------------------------------------------------------------------**

# +
# 학습이 완료되면, subword_tokenizer_kor.model 과 subword_tokenizer_kor.vocab 이 생성됨
# vocab 파일에서 학습된 서브워드들을 확인 할 수 있다.

with open('subword_tokenizer_kor.vocab', encoding='utf-8') as f:
    vo = [doc.strip().split('\t') for doc in f]
# v[0] : token name
# v[1] : token score

word2idx = {w[0]: i for i, w in enumerate(vo)}

# -

# 생성된 model파일을 로드해서 단어 시퀀스를 정수 시퀀스로 바꾸는 인코딩 작업이나
# 반대로 변환하는 디코딩 작업을 할 수 있음.
model_file = 'subword_tokenizer_kor.model'
model = spm.SentencePieceProcessor()
model.load(model_file)

# +
# 기능이 tensorflow 에도 있다.  위의 코드와 같은 기능을 하는 코드이다.
import tensorflow as tf

# 생성된 모델넣어주자 이게 더 잘 분석해주는 것 같음
serialized_model_proto = tf.io.gfile.GFile(vocab_file, 'rb').read()

sp = spm.SentencePieceProcessor()
sp.load_from_serialized_proto(serialized_model_proto)

# +
tmp = '여행같은 음악 지친 하루 끝 힐링이 필요한 당신에게 추천하는 인디곡'

print('단어집합의 크기                              : ',
      model.GetPieceSize())  # 학습시킬때 단어 량을 vocab_size = 32000 로 설정 해줘서 3200 이나옴
print("정수(1785)로부터 맵핑되는 서브워드 변환      : ", model.IdToPiece(1785))
print("서브워드(▁힐링이)로부터 맵핑되는 정수로 변환 : ", model.PieceToId("▁힐링이"), '\n')

# 서브워드 시퀀스로부터 문장을 반환
print(model.DecodeIds([360, 175, 18, 539, 252, 446, 1785, 814, 1122, 990, 3787]), '\n')

# 문장으로부터 인자값에 다라 정수 시퀀스 또는 서브워드 시퀀스로 변환
print(model.encode("힐링이 필요한 당신에게 추천하는 인디곡", out_type=str))
print(model.encode("힐링이 필요한 당신에게 추천하는 인디곡", out_type=int), '\n')

print(model.encode_as_pieces(tmp))  # 문장을 입력하면 서브 워드 시퀀스로 변환
print(model.encode_as_ids(tmp))  # 문장을 입력하면 정수 시퀀스로 변환

# -



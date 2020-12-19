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

# ### 문장 단위 분절

import sys, fileinput ,re
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

# +
  
import sys, fileinput, re
from nltk.tokenize import sent_tokenize

if __name__ == "__main__":
    for line in fileinput.input("input.txt",openhook=fileinput.hook_encoded("utf-8")):
#         print(line)
        if line.strip() != "": # 이건 굳이 없어도 되지만. .. 넣은 것 같음
            line = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', line.strip())

            sentences = sent_tokenize(line.strip())  # 이 함수를 사용하면, 문장단위로 나누어주고 리스트 형식으로 만들어 줌 
            print(sentences, '\n')
            
            for s in sentences:
                if s != "":
#                     sys.stdout.write(s + "\n")
                    print(s)
                    
fileinput.close()
# -

for line in fileinput.input("input.txt",openhook=fileinput.hook_encoded("utf-8")):
    sentences = sent_tokenize(line.strip())  
    for i in sentences:
        print(i)

# ### 문장 합치기 및 분절 예제

import sys, fileinput ,re
from nltk.tokenize import sent_tokenize

# +
import sys, fileinput
from nltk.tokenize import sent_tokenize

if __name__ == "__main__":
    buf = []

    for line in fileinput.input("input2.txt",openhook=fileinput.hook_encoded("utf-8")):
        if line.strip() != "":
            buf += [line.strip()]
#             print(buf)
            sentences = sent_tokenize(" ".join(buf)) # 문장을 기준으로 더해준다.?
#             print(sentences)  # buf와 sentence의 결과가 같다.. ?
            
            if len(sentences) > 1:
                buf = sentences[1:]
#                 print(buf)
                print(sentences)

                sys.stdout.write(sentences[0] + '\n')

    sys.stdout.write(" ".join(buf) + "\n")

# -

# ### 한국어 분절  ( Tokenization )
# - 기본적으로 어근과 접사를 분리하는 역할을 하며, 나아가 잘못된 띄어쓰기에 대해 올바르게 교정하는 역할을 함.

# +
from konlpy.tag import Kkma
kkma = Kkma()

line = '둥둥섬의 왕위 계승자로 태어난 수사자 라이언. 무뚝뚝한 표정과는 다르게 배려심이 많고 따뜻한 리더십을 가지고 있습니다.'
tokenized = kkma.pos(line)
print(tokenized)
# -



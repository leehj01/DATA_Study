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
#     display_name: PythonWithData 3
#     language: python
#     name: python3
# ---

# # 토치 텍스트
# --------------------
# - 파이토치(PyTorch)에서는 텍스트에 대한 여러 추상화 기능을 제공하는 자연어 처리 라이브러리 토치텍스트(Torchtext)를 제공함
# - 토치텍스트가 제공하는 기능들은 다음과 같습니다.
#
#     - 파일 로드하기(File Loading) : 다양한 포맷의 코퍼스를 로드
#     - 토큰화(Tokenization) : 문장을 단어 단위로 분리
#     - 단어 집합(Vocab) : 단어 집합을 만드는 것 
#     - 정수 인코딩(Integer encoding) : 전체 코퍼스의 단어들을 각각의 고유한 정수로 맵핑
#     - 단어 벡터(Word Vector) : 단어 집합의 단어들에 고유한 임베딩 벡터를 만들어줌. 랜덤값으로 초기화한 값일 수도 있고, 사전 훈련된 임베딩 벡터들을 로드할 수도 있다
#     - 배치화(Batching) : 훈련 샘플들의 배치를 만들어줍니다. 이 과정에서 패딩 작업(Padding)도 이루어집니다.
#     
# - 위 모든 과정 이전에 훈련 데이터, 검증 데이터, 테스트 데이터를 분리하는 작업은 별도로 해주어야 하며 위 모든 과정 이후에 각 샘플에 대해서 단어들을 임베딩 벡터로 맵핑해주는 작업. 룩업 테이블(Lookup Table)이라 불리는 작업은 파이토치의 nn.Embedding()을 통해서 해결해야 합니다. 

# !pip install torchtext

# ## 1. 예제를 위한 데이터셋 불러와서 Train과 Test로 분리

# +
import urllib.request
import pandas as pd

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="ratings_test.txt")

train_df = pd.read_table('ratings_train.txt')
test_df = pd.read_table('ratings_test.txt')

print('훈련 데이터 샘플의 개수 : {}'.format(len(train_df)))
print('테스트 데이터 샘플의 개수 : {}'.format(len(test_df)))

# -

test_df.head()

# ## 2. 코퍼스와 레이블 읽기
# - 한줄에서 클래스와 텍스트가 탭 ('\t')으로 구분된 데이터의 입력을 받는 내용
#
# ###  2.1.필드 정의하기 ( torchtext.data)
#
# - torchtext.data에는 필드(Field)라는 도구를 제공합니다. 필드를 통해 앞으로 어떤 전처리를 할 것인지를 정의합니다.
#     - sequential : 시퀀스 데이터 여부. (True가 기본값)
#     - use_vocab : 단어 집합을 만들 것인지 여부. (True가 기본값)
#     - tokenize : 어떤 토큰화 함수를 사용할 것인지 지정. (string.split이 기본값)
#     - lower : 영어 데이터를 전부 소문자화한다. (False가 기본값)
#     - batch_first : 미니 배치 차원을 맨 앞으로 하여 데이터를 불러올 것인지 여부. (False가 기본값)
#     - is_target : 레이블 데이터 여부. (False가 기본값)
#     - fix_length : 최대 허용 길이. 이 길이에 맞춰서 패딩 작업(Padding)이 진행된다.
#     
# ### 2.2. 데이터 셋 만들기 ( TabularDataset )
# - train_data, test_data = TabularDataset.splits(
#         path='.', train='train_data.csv', test='test_data.csv', format='csv',
#         fields=[('text', TEXT), ('label', LABEL)], skip_header=True)
#         
# - 파라미터 
#     - path : 파일이 위치한 경로.
#     - format : 데이터의 포맷.
#     - fields : 위에서 정의한 필드를 지정. 첫번째 원소는 데이터 셋 내에서 해당 필드를 호칭할 이름, 두번째 원소는 지정할 필드.
#     - skip_header : 데이터의 첫번째 줄은 무시.
#     
# ### 2.3. 데이터로더 만들기
#  - 데이터로더는 데이터셋에서 미니 배치만큼 데이터를 로드하게 만들어 주는 역할을 함. 토치텍스트에서는 iterator을 이용하여 데이터 로더를 만들어줌 
#  
#     ' from torchtext.data import Iterator
#          batch_size = 5
#          train_loader = Iterator(dataset=train_data, batch_size = batch_size) 
#          test_loader = Iterator(dataset=test_data, batch_size = batch_size) '
#  
#     
# ### 2.4. 단어 집합 만들기 ( Vocabulary )
# - 토큰화 전처리를 끝냈다면, 이제 각 단어에 고유한 정수를 맵핑해주는 정수 인코딩(Integer enoding) 작업이 필요합니다. 그리고 이 전처리를 위해서는 우선 단어 집합을 만들어주어야 합니다.
# ![image.png](attachment:image.png)

# ## 3. 데이터를 전처리하는 함수를 구현해보기 

# ![image.png](attachment:image.png)

# ## 3.1. 코퍼스와 레이블 읽기 ex, 텍스트 분류 

# +
from torchtext import data
from torchtext.data import TabularDataset
from torchtext.data import Iterator

class DataLoader(object):
    def __init__(self, train_fn, valid_fn,
                batch_size = 64,
                device = -1,
                max_vocab = 999999,
                min_freq = 1,
                use_eos = False,
                shuffle = True):
        super(DataLoader , self).__init__()
        
        
        # 인풋 파일의 필드를 정의해주기
        # 잇풋 파일은 두개의 필드를 고려한다.
        #  하나는 실제 텍스트를 위한 text 객체, 하나는 레이블 데이터를 위한 label 객체 
        # 주의할 점은 필드는 어떻게 전처리할지 정의하는 것이고, 실제 훈련 데이터에 대해서 전처리는 진행 x 
        
        self.label = data.Field(sequential=False,
                               use_vocab= True,
                               unk_token= None)
        self.text = data.Field( use_vocab= True,
                              batch_first= True,
                              include_leng = 'EOS' if use_eos else None)
        
        # TAB 으로 두개의컬럼을 제한한다
        # 인풋 파일의 두개의 컬럼을 load 하기위해 TabularDataset 을 사용한다
        # train_fn 과 vaild_fn로 분리할 것이다. 
        
        train, vaild = TabularDataset.splits(path = "",
                                            train = train_fn,
                                            validation = valid_fn,
                                            format = 'csv',
                                            fields = [('label', self.label),
                                                     ('text', self.text)]
                                            )
        
        # load된 데이터 셋을 각 iterator를 사용하여 데이터 로더를 만들어줌 
        # 문장의 길이에 대해서 정렬해주고 비슷한 길이끼리 그룹화해준다. 
        
        self.train_iter, self.valid_iter = data.BucketIterator.splits((train, valid),
                                                                     batch_size = batch_size,
                                                                     device = "cuda :%d" % device if device >=0 else "cpu",
                                                                     shuffle = shuffle,
                                                                     sort_key = lambda x : len(x.text),
                                                                     sort_within_batch = True)
        
        # 마지막으로, 단어 집합을 만들기 
        # 단어와 단어와 indice사이의 테이블을 매핑시켜주는 것이다.
        
        self.label.build_vocab(train) # TEXT.build_vocab(train_data, min_freq=10, max_size=10000)
        self.text.build_vovab(train, max_size = max_vocab , min_freq = min_freq)
# -

# ## 3.2. 코퍼스 읽기
# - 한 라인이 텍스트로만 채워져 있을 때를 위한 코드 ex, 언어모델 
# - LanguageModelDataset을 통해 미리 정의된 필드를 텍스트 파일에서 읽어드림 
# - 각 문장의 길이에 따라 정렬을 통해 비슷한 길이의 문장끼리 미니배치를 만들어줌 
# - 이 작업을 통해 매우 상이한 길이의 문장들이 하나의 미니배치에 묵여 훈련시간에서 손해보는 것을 방지함

# +
from torchtext import data, datasets

PAD, BOS, EOS = 1,2,3

class DataLoader():
    
    def __init__(self,
                 train_fn, 
                 valid_fn,
                 batch_size = 64,
                 device = 'cpu',
                 max_vocab = 999999,
                 max_length = 255,
                 fix_length = None,
                 use_both = True,
                 use_eos = True,
                 shuffle = True):
        
        
        super(DataLoader , self).__init__()
        
        
        # 인풋 파일의 필드를 정의해주기 - 여기서 코퍼스는가 한라인만 채워져서 field가 하나 . 
        self.text = data.Field( sequential = True, 
                               use_vocab= True,
                               batch_first= True,
                               include_lengths = True,
                               fix_length = fix_length,
                               init_token = '<BOS>' if use_bos else None,
                               eos_token = 'EOS' if use_eos else None)
        
        train = LanguageModelDataset(path = trian_fn,
                                    fields = [('text', self.text)],
                                    max_length = max_length )
        valid = LanguageModelDataset(path = valid_fn,
                                    fields = [('text', self.text)],
                                    max_length = max_length )
        
        self.train_iter = data.BucketIterator(train, 
                                             batch_size = batch_size,
                                              device = "cuda :%d" % device if device >=0 else "cpu",
                                              shuffle = shuffle,
                                              sort_key = lambda x : -len(x.text),
                                              sort_within_batch = True)
        
        self.valid_iter = data.BucketIterator(valid, 
                                             batch_size = batch_size,
                                              device = "cuda :%d" % device if device >=0 else "cpu",
                                              shuffle = False,
                                              sort_key = lambda x : -len(x.text),
                                              sort_within_batch = True
                                             )
        self.text.build_vocab(train, max_size = max_vovab)
        
        
class LanguageModelDataset(data.Dataset):
    
    def __init__(self, path, fields, max_length = None, **kwargs):
        if not isinstance(fields[0], (tuple, list)):
            fields = [('text',fields[0])]
            
        examples = []
        
        with open(path) as f :
            for line in f :
                line = line.strip()
                if max_lengh and max_lengh < len(line.split()):
                    continue
                if line != '':
                    examples.append(data.Example.fromlist(
                    [line], fields))
                    
        suoer(LanguageModelDataset, self).__init__(examples, fields, **kwargs)


# -

# ## 3.3. 병렬 코퍼스 읽기 
# - 텍스트로만 채워진 두개의 파일을 동시에 입력 데이터로 읽어들이는 코드 
# - 두 파일의 코퍼스는 병렬 데이터로 취급되어 같은 라인끼리 맵핑되어야 하므로, 같은 라인수로 채워져 있어야함
# - ex, 기계번역 , 요약 
# - 탭을 사용하여 하낭의 파일에서 두개의 열에 각 언어의 문장을 표현하는 것도 하나의 방법이 됨 

# +
from torchtext import data, datasets

PAD, BOS, EOS = 1,2,3

class DataLoader():
    
    def __init__(self,
                 train_fn = None, 
                 valid_fn = None,
                 exts = None,
                 batch_size = 64,
                 device = 'cpu',
                 max_vocab = 999999,
                 max_length = 255,
                 fix_length = None,
                 use_both = True,
                 use_eos = True,
                 shuffle = True,
                dsl = False):
        
        
        super(DataLoader , self).__init__()
        
        
        
        # 필드 
        self.src = data.Field( sequential = True, 
                               use_vocab= True,
                               batch_first= True,
                               include_lengths = True,
                               fix_length = fix_length,
                               init_token = '<BOS>' if use_bos else None,
                               eos_token = 'EOS' if use_eos else None)
        

        self.tgt = data.Field( sequential = True, 
                               use_vocab= True,
                               batch_first= True,
                               include_lengths = True,
                               fix_length = fix_length,
                               init_token = '<BOS>' if use_bos else None,
                               eos_token = 'EOS' if use_eos else None)
        
        
        if train_fn is not None and valid_fn is not None and exts is not None:
            train = TranslationDataset(path = train_fn,
                                      exts = exts,
                                      fields = [('src', self.src),
                                               ('tgt', self.tgt)],
                                      max_length = max_length)
            
            valid = TranslationDataset(path = valid_fn,
                          exts = exts,
                          fields = [('src', self.src),
                                   ('tgt', self.tgt)],
                          max_length = max_length)
        
        
        self.train_iter = data.BucketIterator(train,
                                             batch_size = batch_size, 
                                             device = "cuda :%d" % device if device >=0 else "cpu",
                                              shuffle = shuffle,
                                              sort_key = lambda x : len(x.tgt) + (max_length * len(x.src)),
                                              sort_within_batch = True)
        self.valid_iter = data.BucketIterator(valid, 
                                             batch_size = batch_size,
                                              device = "cuda :%d" % device if device >=0 else "cpu",
                                              shuffle = False,
                                              sort_key = lambda x : len(x.tgt) + (max_length * len(x.src)),
                                              sort_within_batch = True)
                                              
        self.text.build_vocab(train, max_size = max_vocab)
        self.tgt.build_vocab(train, max_size = max_vocab)
                
                                              
                                              
    def load_vocab( self, src_vocab, tgt_vocab):
        self.src.vocab = scr_vocab
        self.tgt.vocab = tgt_vocab
                                              
                                              
            
        
        
        
class TranslationDataset(data.Dataset):
    
    @staticmethod
    def sort_key(ex):
        return data.interleave_key(len(ex.src), len(ex.trg))
    
    
    def __init__(self, path, exts, fields, max_length = None, **kwargs):
        if not isinstance(fields[0], (tuple, list)):
            fields = [('src', fields[0]), ('trg',fields[1])]

                                              
        if not path.endswith('.'):
            path += '.'
                                              
        src_path, trg_path = tuple(os.path.expanduser(path + x ) for x in exts )                                      
                                
        examples = []
        
        with open(src_path, encoding = 'utf-8') as src_file, open(trg_path, encoding = 'uft-8') as trg_file :
            for src_line, trg_line in zip(src_file,trg_file) :
                src_line, trg_line = src_line.strip(), trg_line.strip()
                if max_lengh and max_lengh < max(len(src_line.split()), len(trg_line.split())):
                    continue
                                              
                if src_line != '' and trg_line != '':
                                              
                    examples.append(data.Example.fromlist(
                    [src_line, trg_line], fields))
                    
        super().__init__(examples, fields, **kwargs)
                                            
# -



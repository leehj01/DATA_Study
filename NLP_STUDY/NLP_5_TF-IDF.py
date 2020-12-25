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

# +
import pandas as pd

def get_term_frequency(document, word_dict = None ):
    if word_dict is None :
        word_dict = {}
    words = document.split()
    
    for w in words:
        word_dict[w] = 1 + ( 0 if word_dict.get(w) is None else word_dict[w])
        
    return pd.Series(word_dict).sort_values(ascening = False)


# -

def get_document_frequency(documents):
    dicts = [] 
    vocab = set([])
    df = {}
    
    for d  in documents :
        tf = get_term_frequency(d)
        dicts += [tf]
        vocab = vocab | set(tf.keys())
        
    for v in list(vocab):
        df[v] = 0
        for dict_d in dicts :
            if dict_d.get(v) is not None:
                df[v] += 1
                
    return pd.Series(df).sort_values(ascending = False)


def get_tfidf(docs):
    vocab = {}
    tfs = []

    for d in docs :
        vocab = get_term_frequency( d, vocab)
        tfs += [get_term_frequency(d)]
    df = get_document_frequency(docs)
    
    from operator import itermgetter
    import numpy as np
    
    stats = []
    for word, freq in vocab.items():
        tfidfs = []
        for idx in range(len(docs)):
            if tfs[idx].get(word) is not None :
                tfidfs += [tfs[idx][word] * np.log(len(docs) / df[word])]
                
            else :
                tfidfs += [0]
                
        stats.append((word, freq, *tfidfs, max(tfidfs)))

    return pd.DataFrame(stats, colums = ('word',
                                        'frequency',
                                        'doc1',
                                        'doc2',
                                        'doc3',
                                        'max')).sort_values('max',ascending = False)


get_tfidf([doc1, doc2, doc3])


# ## TF 행렬 만들기

def get_tf(docs):
    vocab = {}
    tfs = []

    for d in docs :
        vocab = get_term_frequency( d, vocab)
        tfs += [get_term_frequency(d)]

    from operator import itermgetter
    import numpy as np
    
    stats = []
    for word, freq in vocab.items():
        tf_v = []
        for idx in range(len(docs)):
            if tfs[idx].get(word) is not None :
                tf_v += [tfs[idx][word]]
            else :
                tf_v += [0]
                
            stats.append((word, freq, *tf_v))
        
        return pd.DataFrame(stats, colums = ('word',
                                        'frequency',
                                        'doc1',
                                        'doc2',
                                        'doc3',
                                        'max')).sort_values('frequency',ascending = False)


# +
from collections import defaultdict

import pandas as pd

def get_context_counts(lines, w_size = 2):
    co_dict = defaltdict(int)
    
    for line in lines :
        words = line.split()
        
        for i , w in enumerate(words):
            for c in words[ i - w_size : i + w_size]:
                if w != c :
                    co_dict[(w,c)] += 1
    
    return pd.Series(co_dict)


# -

def co_occurrence(cp_dict, vocab):
    data = []
    
    for word1 in vocab :
        row = []
        
        for word2 in vocab:
            try :
                count = co_dict[(word1, word2)]
                
            except KeyError:
                count = 0
            row.append(count)
            
        data.append(row)
        
    return pd.DataFrame(data, index = vocab, columns = vocab)



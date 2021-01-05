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

# ## 벡터간의 유사도 또는 거리를 구하는 방법

# +
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Arc
import math
# %matplotlib inline

import torch
import torch.nn as nn

# +
# 벡터에 대한 값 넣기

x = torch.LongTensor([[6], [4]]).float()  # 63 비트 integer data type 을 넣는 것
y = torch.LongTensor([[4], [8]]).float()

print(' x : ', x.numpy().flatten())
print(' y : ', y.numpy().flatten())


# -

# 시각화를 위한 좌표 설정
def plot_distance(x, y, distance_viz_func=None, title=None):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.annotate(s=' ', xy=(6, 4), xytext=(0, 0), arrowprops=dict(arrowstyle='->'))
    ax.annotate(s='', xy=y, xytext=(0, 0), arrowprops=dict(arrowstyle='->'))
    ax.axhline(0, color='k', alpha=0.3)
    ax.axvline(0, color='k', alpha=0.3)
    ax.grid()
    if distance_viz_func:
        distance_viz_func(x, y, ax=ax)
    if title:
        plt.title(title)
    ax.set_xticks(range(-1, 11))
    ax.set_yticks(range(-1, 11))
    plt.show()


plot_distance(x, y, title='x, y')

# ### 1. L1 거리

# +
import torch


def get_l1_distance(x1, x2):
    return ((x1 - x2).abs()).sum()


# -

get_l1_distance(x, y)


def viz_func(x, y, ax=None):
    x0, x1 = x
    y0, y1 = y
    ax.hlines(min(x1, y1), min(x0, y0), max(x0, y0), color='b')
    ax.vlines(min(x0, y0), min(x1, y1), max(x1, y1), color='b')


plot_distance(x, y, viz_func, title="L1 Norm")


# ### 2. L2 거리

def get_l2_distance(x1, x2):
    return ((x1 - x2) ** 2).sum() ** .5


get_l2_distance(x, y)


def viz_func(x, y, ax=None):
    plt.annotate('', xy=y, xytext=x, arrowprops=dict(arrowstyle='-', color='b'))


plot_distance(x, y, viz_func, title="L2 Norm")


# ### 3. infinity Norm

def get_infinity_distance(x1, x2):
    return ((x1 - x2).abs()).max()


get_infinity_distance(x, y)


def viz_func(x, y, ax=None):
    x0, x1 = x
    y0, y1 = y
    if (x0 - y0).abs() > (x1 - y1).abs():
        ax.hlines(min(x1, y1), min(x0, y0), max(x0, y0), color="b")
    else:
        ax.vlines(min(x0, y0), min(x1, y1), max(x1, y1), color="b")


plot_distance(x, y, viz_func, title="L$infty$ Norm")


# ### 4. 코사인 유사도

def get_cosine_similarity(x1, x2):
    return (x1 * x2).sum() / ((x1 ** 2).sum() ** .5 * (x2 ** 2).sum() ** .5)


get_cosine_similarity(x, y)

line1 = Line2D([0, 1], [0, 4], linewidth=1, linestyle="-", color="green")
l1xy = line1.get_xydata()


# https://stackoverflow.com/questions/25227100/best-way-to-plot-an-angle-between-two-lines-in-matplotlib
def get_angle_plot(
        x, y, offset=1, color=None,
        origin=[0, 0], len_x_axis=3, len_y_axis=3
):
    # Angle between line1 and x-axis
    slope1 = x[1] / x[0]
    angle1 = abs(math.degrees(math.atan(slope1)))  # Taking only the positive angle

    # Angle between line2 and x-axis
    slope2 = y[1] / y[0]
    angle2 = abs(math.degrees(math.atan(slope2)))

    theta1 = min(angle1, angle2)
    theta2 = max(angle1, angle2)

    angle = theta2 - theta1

    if color is None:
        color = line1.get_color()  # Uses the color of line 1 if color parameter is not passed.

    return Arc(origin, len_x_axis * offset, len_y_axis * offset, 0, theta1, theta2, color=color,
               label=str(angle) + u"\u00b0")


def viz_func(x, y, ax):
    angle_plot = get_angle_plot(x, y, color='b')
    ax.add_patch(angle_plot)


plot_distance(x, y, viz_func, title='Cosine Similarity')


# ### 5. 자카드 유사도

# +
def get_faccard_similarity(x1, x2):
    return torch.stack([x1, x2]).min(dim=0)[0].sum() / torch.stack([x1, x2])


# torch.stack 는 두개의 텐서를 결합하는 함수이다.


# -

# ## 단어 중의소 해소 : 레스크 알고리즘

# +
# 먼저, NLTK의 워드넷에서 단어 검색

from nltk.corpus import wordnet as wn

for ss in wn.synsets('bass'):
    print(ss, ss.definition())  # 단어의 설명을 구하는 코드


# +
# 레스크 알고리즘 수행을 위해 간단하게 감싸서 구현

def lesk(sentence, word):
    from nltk.wsd import lesk

    best_synset = lesk(sentence.split(), word)
    print(best_synset, best_synset.definition())


# -

sentence = "I went fishing last weekend and i got a bass and cooked it "  # 물고리를 의미함
word = "bass"
lesk(sentence, word)  # 잘 예측함

sentence = 'I love the music from the speaker which has strong beat and bass'  # 음악
word = 'bass'
lesk(sentence, word)  # 잘 예측함

sentence = 'I think the bass is more important than guitar'
word = 'bass'
lesk(sentence, word)

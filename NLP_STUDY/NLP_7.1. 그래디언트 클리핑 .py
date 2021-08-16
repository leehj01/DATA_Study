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

# ## 그래디언트 클리핑
# - torch.nn.utils.clip_grad_norm 이라는 함수를 통해 그래디언트 클리핑 기능을 사용할 수 있다.

import torch.optim as optim
import torch.nn.utils as torch_utils

# +
learning_rate = 1.
max_grad_norm = 5.

optimizer = optim.SGD(model.parameters(), lr = learning_rate)

# 기울기 폭발 ( gradient exploding 을 막기 위해서 그래디언트 클리핑 실시)
torch_utils.clip_grad_norm_(model.parameters(), max_grad_norm)
optimizer.step()
# -



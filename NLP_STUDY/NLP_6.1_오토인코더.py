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

# ## 모델 불러오기

# +
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

batch_size = 256
learning_rate = 0.0002
num_epoch = 5

mnist_train = dset.MNIST(
    "./", train=True, transform=transforms.ToTensor(), 
    target_transform=None, download=True)
mnist_test = dset.MNIST(
    "./", train=False, transform=transforms.ToTensor(),
    target_transform=None, download=True)

train_loader = torch.utils.data.DataLoader(
    mnist_train,batch_size=batch_size, shuffle=True,num_workers=2,drop_last=True)
test_loader = torch.utils.data.DataLoader(
    mnist_test,batch_size=batch_size, shuffle=False,num_workers=2,drop_last=True)


# -

# ## 오토 인코더 모델 

class Autoencoder(nn.Module) : 
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Linear(28*28 , 20)
        self.decoder = nn.Linear(20, 28*28)
        
    def forward(self, x):
        x = x.view(batch_size, -1)
        encoded = self.encoder(x)
        out = self.decoder(encoded).view(batch_size, 1, 28,28)
        return out


# +
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

model = Autoencoder().to(device)
loss_func = nn.MSELoss()
optimizer  = torch.optim.Adam(model.parameters(), lr = learning_rate)
# -

model

loss_arr = []
for i in range(num_epoch):
    for j , [image, label] in enumerate (train_loader):
        x = image.to(device)
        
        optimizer.zero_grad()
        output = model.forward(x)
        loss = loss_func(output, x)
        loss.backward()
        optimizer.step()
        
    if j % 1000 ==0 :
        print(loss)
        loss_arr.append(loss.cpu().data.numpy()[0])

# +
out_img = torch.squeeze(output.cpu().data)
# print(out_img)

for i in range(3):
    plt.subplot(1,2,1)
    plt.imshow(torch.squeeze(image[i]).numpy(), cmap = 'gray')
    plt.subplot(1,2,2)
    plt.imshow(out_img[i].numpy(), cmap='gray')
    plt.show()

import torch
import torch.nn as nn
import numpy as np
import os, os.path
import cv2

def imread(path):
    im = cv2.imread(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = np.asarray(im).flatten()
    return im


path = './Datas/'
datas = [ [] for _ in range(10)]

for i in range(len(datas)):
    filenames = os.listdir(path + str(i))
    filenames.sort()
    for n, fi in enumerate(filenames):
        path_to_img = path+str(i)+'/'+fi
        #print(path_to_img)
        tab_im = imread(path_to_img)
        datas[i].append(tab_im)
print(datas[0][8])
#!/usr/bin/env python3
import cv2
from tqdm import tqdm
import glob
import numpy as np
import os

def pad(img, target_size=256):
    H, W, _ = img.shape
    axis = 0 if H < W else 1
    diff = img.shape[1 - axis] - img.shape[axis]
    pad1 = diff // 2
    pad2 = diff - pad1
    width = [(0, 0)] * 3
    width[axis] = (pad1, pad2)
    img = np.pad(img, width)
    img = cv2.resize(img, (target_size, target_size))
    return img

paths = glob.glob('data_raw/*/*')

for path_raw in tqdm(paths):
    path = path_raw.replace('_raw', '')
    os.makedirs(path, exist_ok=True)

    for img_path in glob.glob(f'{path_raw}/img_*.jpg'):
        img = cv2.imread(img_path)
        img = pad(img)
        cv2.imwrite(img_path.replace('_raw', ''), img)
# vim: ts=4 sw=4 sts=4 expandtab

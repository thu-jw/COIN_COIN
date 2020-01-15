#!/usr/bin/env python3
from glob import glob
import os
import numpy as np
root = './data_washed'

num_clips = []
num_steps = []
vids = os.listdir(root)

for vid in vids:
    clips = os.listdir(f'{root}/{vid}')
    num_clips.append(len(clips))
    for i in range(len(clips)):
        num_step = len(os.listdir(f'{root}/{vid}/{i}'))
        num_steps.append(num_step)
        if num_step == 22:
            print(vid)

print('num clips', np.sum(num_clips))
print('max steps', np.max(num_steps))

from IPython import embed
embed()
# vim: ts=4 sw=4 sts=4 expandtab

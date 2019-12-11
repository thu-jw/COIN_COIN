#!/usr/bin/env python3
import glob
import json
import os
from tqdm import tqdm
import shutil
from pathlib import Path
from IPython import embed

paths = glob.glob('/opt/data*/tsn_of*/*')

# make dict
paths_dict = {
    path.rsplit('/')[-1]: path for path in paths
}

annotations = json.load(open('../annotations/COIN.json', 'r'))
# check exsit
for key, info in tqdm(annotations['database'].items()):
    path = paths_dict[key]
    duration = info['duration']
    anno = info['annotation']
    images = glob.glob(path + '/img_*.jpg')
    num_frames = len(images)
    fps = num_frames / duration

    for action_id, action in enumerate(anno):
        start, end = action['segment']
        label = action['label']
        start_frame = int(fps * start) + 1
        stride = int((end - start) * fps // 16)
        dst_path = os.path.join('data_with_name', key, f'{action_id}_{label}')
        os.makedirs(dst_path, exist_ok=True)
        for i in range(16):
            frame_id = i * stride + start_frame
            filename = f'img_{frame_id:05d}.jpg'
            src_path = os.path.join(path, filename)
            shutil.copyfile(src_path, os.path.join(dst_path, filename))


# vim: ts=4 sw=4 sts=4 expandtab

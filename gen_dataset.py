#!/usr/bin/env python3
import glob
import json
import os
from tqdm import tqdm
import shutil
from pathlib import Path
from IPython import embed
from collections import OrderedDict

def parse_cuts(cut_points, steps):
    # get clips from annotated video
    clips = []
    clip_start = None
    cut_points = list(map(int, filter(None, cut_points.split(','))))
    for clip_end in cut_points:
        if clip_start is None:
            clip_start = 0
        clips.append([clip_start, clip_end])
        clip_start = clip_end + 1
    if clip_start is None:
        clip_start = 0

    if clip_start <= steps - 1:
        clips.append([clip_start, steps - 1])
    return cut_points, clips

annotations = json.load(open('COIN_COIN.json', 'r'), object_pairs_hook=OrderedDict)

paths = glob.glob('/opt/data*/tsn_of*/*')

# make dict
paths_dict = {
    path.rsplit('/')[-1]: path for path in paths
}

"""
the washed data will be structured as:
data/video_name/task_index/step_index/img_*.jpg
"""
for anno in annotations:
    anno = anno['fields']
    if anno['state'] != 2: # skip unfinished videos
        continue
    video_name = anno['video_name']
    cut_points, clips = parse_cuts(anno['cut_points'], anno['steps'])

    for i, clip in enumerate(clips):
        for j in range(clip[0], clip[1] + 1):
            src_path = os.path.join('/opt/data5/COIN_COIN', video_name, str(j))
            dst_path = os.path.join('data_washed', video_name, str(i))
            os.makedirs(dst_path, exist_ok=True)
            os.symlink(src_path, os.path.join(dst_path, str(j)))
            # shutil.copytree(src_path, dst_path, symlinks=True)

# vim: ts=4 sw=4 sts=4 expandtab

#!/usr/bin/env python3
from glob import glob
import os
import imageio
from tqdm import tqdm

# data/video_name/step_id/img_*.jpg
root = 'data'
for video_name in tqdm(os.listdir(root)):
    for step_id in os.listdir(os.path.join(root, video_name)):
        save_path = f'{root}/{video_name}/{step_id}/action.gif'
        # if os.path.exists(save_path):
        #     continue
        try:
            images_path = sorted(glob(f'{root}/{video_name}/{step_id}/img_*.jpg'))[::2]
            images = [imageio.imread(path) for path in images_path]
            imageio.mimsave(save_path, images, duration=0.4)
        except RuntimeError as e:
            print(video_name, step_id, e)

# vim: ts=4 sw=4 sts=4 expandtab

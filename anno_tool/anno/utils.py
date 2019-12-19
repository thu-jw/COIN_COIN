# coding: utf-8
import pandas as pd
from IPython import embed

def load_action_dict():
    df = pd.read_excel('anno/static/taxonomy.xlsx', sheet_name='target_action_mapping')
    df = df.iloc[:, 2:]
    action_dict = df.set_index('Action Id').T.to_dict('list')
    for k, v in action_dict.items():
        action_dict[k] = v[0]
    return action_dict

def parse_cuts(video):
    # get clips from annotated video
    clips = []
    clip_start = None
    cut_points = list(map(int, filter(None, video.cut_points.split(','))))
    for clip_end in cut_points:
        if clip_start is None:
            clip_start = 0
        clips.append([clip_start, clip_end])
        clip_start = clip_end + 1
    if clip_start is None:
        clip_start = 0

    if clip_start <= video.steps - 1:
        clips.append([clip_start, video.steps - 1])
    return cut_points, clips

if __name__ == "__main__":
    d = load_action_dict()
    for i in range(1, 779):
        if i not in d:
            print(i)

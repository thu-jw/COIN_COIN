#!/usr/bin/env python3
import glob
import json
import os
from collections import OrderedDict
import argparse
import pandas as pd
from tqdm import tqdm
from IPython import embed
import numpy as np
import itertools
import pdb
import random
import cv2
import pickle as pkl

def nchoice(array, size=2):
    if size is None:
        size = len(array)
    return random.sample(array, min(len(array), size))

def smart_load(obj):
    return json.loads(obj) if isinstance(obj, str) else obj

def parse_cuts(cut_points, steps):
    # get clips from annotated video
    clips = []
    clip_start = None
    cut_points = list(map(int, filter(None, cut_points.split(','))))
    for clip_end in cut_points:
        if clip_start is None:
            clip_start = 0
        clips.append([clip_start, clip_end + 1])
        clip_start = clip_end + 1
    if clip_start is None:
        clip_start = 0

    if clip_start <= steps - 1:
        clips.append([clip_start, steps])
    return cut_points, clips

def filter_clips(args, save=False):
    """
    cut the clips longer than args.max_length
    drop the clips shorter than args.min_length
    save results to csv
    """
    print('filtering clips')
    annotations = json.load(open('data_gen/anno.json', 'r'), object_pairs_hook=OrderedDict)
    df = pd.DataFrame(columns=['video_name', 'video_class', 'action_ids', 'num_clips', 'clips', 'train'])
    for anno in tqdm(annotations):
        row = OrderedDict()
        anno = anno['fields']
        assert anno['state'] == 2
        row['video_name'] = anno['video_name']
        row['video_class'] = anno['video_class']
        row['action_ids'] = list(map(int, filter(None, anno['action_ids'].split(','))))
        row['num_actions'] = len(row['action_ids'])
        # get clips
        _, clips = parse_cuts(anno['cut_points'], anno['steps'])
        new_clips = []
        for clip in clips:
            span = clip[1] - clip[0]
            if span < args.min_length:
                continue
            if span <= args.max_length:
                new_clips.append(clip)
            else:
                start = clip[0]
                while start < clip[1]:
                    end = min(start + args.max_length, clip[1])
                    if end - start >= args.min_length:
                        new_clips.append([start, end])
                    start = end

        row['num_clips'] = len(new_clips)
        row['clips'] = new_clips
        row['train'] = True
        df = df.append(pd.Series(row), ignore_index=True)

    if save:
        df.to_csv(args.csv, index=False)
    return df

def split_train_test(args, df=None):
    print('spliting train and test set')
    if df is None:
        df = pd.read_csv(args.csv)

    df['train'] = False
    video_classes = np.unique(df['video_class'].values)
    for vclass in video_classes:
        df_vclass = df.loc[df['video_class'] == vclass]
        total_clips = df_vclass['num_clips'].sum()
        train_clips = int(total_clips * (1 - args.test_ratio))

        num_clips = df_vclass['num_clips'].tolist()
        s, selected_indices = find_subset(num_clips, train_clips)
        selected_names = df_vclass.iloc[selected_indices]['video_name']
        df.loc[df.video_name.isin(selected_names), 'train'] =  True
        # print(vclass, total_clips, train_clips, s)
    df.to_csv(args.csv, index=False)
    return df

def find_subset(num_clips, train_clips):
    indices = np.argsort(num_clips)

    s = 0
    selected_indices = []
    try:
        for ind in indices[::-1]:
            if s + num_clips[ind] > train_clips:
                continue
            s += num_clips[ind]
            selected_indices.append(ind)
    except:
        embed()
    return s, selected_indices

def gen_QA(args, df=None):
    print('generating question/answers')
    if df is None:
       df = pd.read_csv(args.csv)
    train_set = []
    test_set = []

    for _, row in df.iterrows():
        video_name = row['video_name']
        clips = smart_load(row['clips'])
        action_ids = smart_load(row['action_ids'])
        is_train = smart_load(row['train'])
        for clip in clips:
            # generate Q-A for each clip
            # Q[0], Q[1] are start and end frame
            question = [sorted(glob.glob('data_raw/{}/{}/img_*.jpg'.format(video_name, clip[i] - i)))[-i].split('/', 1)[-1] for i in range(2)]
            choices = []
            correct_steps = ['{}/{}'.format(video_name, i) for i in np.arange(*clip)]
            correct_choice = {
                'steps': correct_steps,
                'correct': True,
                'wrong_type': 'correct',
            }


            # try to generate wrong anwers
            if args.setting == 'long':
                # the first three types of wrong choices are only valid in long term setting
                # 1. missing
                pool = [i for i in range(len(correct_steps))]
                for idx in nchoice(pool):
                    steps = correct_steps.copy()
                    steps.pop(idx)
                    choices.append({
                        'steps': steps,
                        'correct': False,
                        'wrong_type': 'missing',
                    })

                # 2. swap
                pool = [k for k in itertools.product(np.arange(*clip), np.arange(*clip)) if action_ids[k[0]] != action_ids[k[1]]]
                if len(pool) > 0:
                    for k1, k2 in nchoice(pool):
                        steps = correct_steps.copy()
                        i1, i2 = k1 - clip[0], k2 - clip[0]
                        steps[i1], steps[i2] = steps[i2], steps[i1]
                        choices.append({
                            'steps': steps,
                            'correct': False,
                            'wrong_type': 'swap',
                        })

                # 3. extra
                pool = [i for i in range(len(action_ids))]# if i < clip[0] or i >= clip[1]]
                for i1 in nchoice(pool):
                    steps = correct_steps.copy()
                    new = '{}/{}'.format(video_name, i1)
                    steps.insert(np.random.randint(len(steps)), new)
                    choices.append({
                        'steps': steps,
                        'correct': False,
                        'wrong_type': 'extra',
                    })

            # 4. replacing: same
            pool = [i for i in range(len(action_ids))]# if i < clip[0] or i >= clip[1]]
            count = 0
            for i2 in nchoice(pool, size=None):
                pool_k1 = [k for k in range(clip[0], clip[1]) if action_ids[i2] != action_ids[k]]
                if len(pool_k1) == 0:
                    continue
                i1 = np.random.choice(pool_k1) - clip[0]
                steps = correct_steps.copy()
                steps[i1] = '{}/{}'.format(video_name, i2)

                choices.append({
                    'steps': steps,
                    'correct': False,
                    'wrong_type': 'replace_same',
                })
                count += 1
                if count >= 2 and len(choices) > 3:
                    break

            # 5. replacing: other
            if len(choices) < 3:
                items = df.loc[(df.video_class == row['video_class']) & (df.video_name != row['video_name'])].sample(n=3-len(choices), random_state=1)
                for _, item in items.iterrows():
                    steps = correct_steps.copy()
                    i1 = np.random.randint(len(steps))
                    i2 = np.random.randint(item['num_actions'])
                    steps[i1] = '{}/{}'.format(item['video_name'], i2)
                    choices.append({
                        'steps': steps,
                        'correct': False,
                        'wrong_type': 'replace_other',
                    })

            np.random.shuffle(choices)
            choices = choices[:3]
            choices.append(correct_choice)
            np.random.shuffle(choices)

            if is_train:
                train_set.append({
                    'question': question,
                    'choices': choices
                })
            else:
                test_set.append({
                    'question': question,
                    'choices': choices
                })

    np.random.shuffle(train_set)
    np.random.shuffle(test_set)
    json.dump(train_set, open('metadata/{}/train.json'.format(args.setting), 'w'))
    json.dump(test_set, open('metadata/{}/test.json'.format(args.setting), 'w'))
    print(args.setting, len(train_set), len(test_set))

    # get stat
    dataset = {
        'train': train_set,
        'test': test_set,
    }
    for k, v in dataset.items():
        print(k)
        stat = {}
        for QA in v:
            for choice in QA['choices']:
                wrong_type = choice['wrong_type']
                if wrong_type not in stat:
                    stat[wrong_type] = 1
                else:
                    stat[wrong_type] += 1
        print(stat)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-length', '-M', help="max length of clip", default=5)
    parser.add_argument('--min-length', '-m', help="min length of clip", default=2)
    parser.add_argument('--test-ratio', '-r', help="ratio for test samples", default=0.1)
    parser.add_argument('--setting', '-s', help="setting", default='long', choices=('long', 'short'))
    parser.add_argument('--use-checkpoints', '-c', default=False, action='store_true')
    args = parser.parse_args()

    np.random.seed(1)
    random.seed(1)

    if args.setting == 'short':
        args.max_length = args.min_length = 1
    else:
        assert args.max_length >= args.min_length
        assert args.min_length >= 2

    args.csv = 'data_gen/anno_{}.csv'.format(args.setting)

    if not args.use_checkpoints:
        df = filter_clips(args, save=True)
        df = split_train_test(args, df)
    gen_QA(args, df=None)

# vim: ts=4 sw=4 sts=4 expandtab

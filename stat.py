#!/usr/bin/env python3
import json
import glob
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--setting', '-s', type=str)
    parser.add_argument('--phase', '-p', type=str)
    args = parser.parse_args()

    if args.phase == 'all':
        phases = ['train', 'test']
    else:
        phases = [args.phase]

    meta_coin = json.load(open('./COIN.json'))['database']
    count = {}
    duration = 0
    action_id = []
    length = 0
    wrong_type = {}
    for phase in phases:
        path = f'./metadata/{args.setting}/{phase}.json'
        metadata = json.load(open(path))
        for item in metadata:
            for c in item['choices']:
                w = c['wrong_type']
                if w in wrong_type:
                    wrong_type[w] += 1
                else:
                    wrong_type[w] = 1

                length += len(c['steps'])
                for step in c['steps']:
                    vid, index = step.split('/')
                    anno = meta_coin[vid]['annotation']
                    seg = anno[int(index)]['segment']
                    duration += seg[1] - seg[0]
                    action_id.append(anno[int(index)]['id'])
        count[phase] = len(metadata)


    num_problems = sum(count.values())
    action_id = set(action_id)
    mean_duration = duration / (num_problems * 4)
    mean_length = length / (num_problems * 4)
    print('type of actions:', len(action_id))
    print('number of problems: ', num_problems)
    print(count)
    print('mean duration: ', mean_duration)
    print('mean length: ', mean_length)
    print('wrong type', wrong_type)
    total_steps = len(glob.glob('./data/*/*'))
    print('total steps:', total_steps)
# vim: ts=4 sw=4 sts=4 expandtab

#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

COIN = json.load(open('COIN.json'))
metadata = {}
for setting in ['long6', 'short1']:
    if setting not in metadata:
        metadata[setting] = {}
    for phase in ['train', 'test']:
        metadata[setting][phase] = json.load(open(f'./metadata/{setting}/{phase}.json'))

# prepare hist
duration = {}
bins = np.arange(0, 310, 10)

for setting in metadata.keys():
    if setting not in duration:
        duration[setting] = {}
    for phase, problems in metadata[setting].items():
        duration_list = []
        for item in problems:
            for c in item['choices']:
                for step in c['steps']:
                    vid, index = step.split('/')
                    anno = COIN['database'][vid]['annotation']
                    seg = anno[int(index)]['segment']
                    duration_list.append(seg[1] - seg[0])
        duration[setting][phase] = np.histogram(duration_list, bins=bins)
        print(max(duration_list))
print('duration loaded')


fig = plt.figure(figsize=(20, 10))
bins = np.arange(0, 300, 1)


for setting in duration.keys():
    print(setting)
    bar_list = []
    width = 0.2 if 'long' in setting else -0.2
    for phase, value in duration[setting].items():
        hist, edges = value
        x = (edges[1:] + edges[:-1]) / 2
        print(len(x), len(hist))
        assert len(x) == len(hist)
        bar_list.append(plt.bar(x, hist, align='edge', width=width))

plt.savefig('duration.pdf')
# vim: ts=4 sw=4 sts=4 expandtab

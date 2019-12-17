#!/usr/bin/env python3
import json
from tqdm import tqdm
from IPython import embed

annotations = json.load(open('../annotations/COIN.json', 'r'))


length = []

for key, info in tqdm(annotations['database'].items()):
    duration = info['duration']
    anno = info['annotation']
    if len(anno) == 51:
        embed()
    length.append(len(anno))

# vim: ts=4 sw=4 sts=4 expandtab

#!/usr/bin/env python3
import json
from tqdm import tqdm
from IPython import embed

annotations = json.load(open('../annotations/COIN.json', 'r'))


length = []

for key, info in tqdm(annotations['database'].items()):
    duration = info['duration']
    anno = info['annotation']
    for a in anno:
        if int(a['id']) in [103, 228, 319, 381]:
            print(a['id'], a['label'])

# vim: ts=4 sw=4 sts=4 expandtab

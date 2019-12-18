#!/usr/bin/env python3
import json
from collections import OrderedDict
from tqdm import tqdm

annotations = json.load(open('../COIN.json', 'r'), object_pairs_hook=OrderedDict)

processed = []
for i, (key, info) in tqdm(enumerate(annotations['database'].items())):
    anno = info['annotation']
    fields = {}
    fields['video_name'] = key
    fields['video_class'] = info['class']
    fields['cut_points'] = ""
    fields['checkpoint'] = 0
    fields['steps'] = len(anno)
    fields['action_ids'] = ','.join([a['id'] for a in anno])

    fields['state'] = 2 if fields['steps'] <= 3 else 0
    fields['train'] = info['subset'] == 'training'

    processed.append(
        OrderedDict([
            ("model", "anno.video"),
            ("pk", i + 1),
            ("fields", fields)
        ])
    )


json.dump(processed, open('./anno/fixtures/COIN.json', 'w'))

# vim: ts=4 sw=4 sts=4 expandtab

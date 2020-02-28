#!/usr/bin/env python3
import json
from collections import OrderedDict
from tqdm import tqdm
import numpy as np
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--setting', '-s', default='long_uniform', type=str)
    parser.add_argument('--phase', '-p', default='test', type=str)
    args = parser.parse_args()

    qas = json.load(open(f'../metadata/{args.setting}/{args.phase}.json', 'r'), object_pairs_hook=OrderedDict)
    processed = []

    for i, qa in enumerate(qas):
        fields = {}
        fields['question'] = json.dumps(qa['question'])
        fields['choices'] = json.dumps(qa['choices'])
        fields['answers'] = ''
        fields['answerers'] = ''
        fields['correct_answer'] = [i for i in range(4) if qa['choices'][i]['correct']][0]
        fields['setting'] = args.setting
        fields['phase'] = args.phase

        processed.append(
            OrderedDict([
                ("model", "humantest.qa"),
                ("pk", i + 1),
                ("fields", fields)
            ])
        )


    json.dump(processed, open('./humantest/fixtures/qa.json', 'w'))

# vim: ts=4 sw=4 sts=4 expandtab

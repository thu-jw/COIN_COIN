#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def draw_duration():
    COIN = json.load(open('COIN.json'))
    metadata = {}
    for setting in ['long6', 'short1']:
        if setting not in metadata:
            metadata[setting] = {}
        for phase in ['train', 'test']:
            metadata[setting][phase] = json.load(open(f'./metadata/{setting}/{phase}.json'))
    # prepare hist
    duration = {}
    sep = 30
    bins = np.arange(0, 310, sep)

    for setting in metadata.keys():
        if setting not in duration:
            duration[setting] = {}
        for phase, problems in metadata[setting].items():
            duration_list = []
            for item in problems:
                for c in item['choices']:
                    s = 0
                    for step in c['steps']:
                        vid, index = step.split('/')
                        anno = COIN['database'][vid]['annotation']
                        seg = anno[int(index)]['segment']
                        s += seg[1] - seg[0]
                    duration_list.append(s)
            duration[setting][phase] = np.histogram(duration_list, bins=bins)


    fig = plt.figure(figsize=(10, 10))

    colors = {
        'long6': {'train': (1, 0, 0), 'test': (1, 0, 0, 0.5)},
        'short1': {'train': (0, 0, 1), 'test': (0, 0, 1, 0.5)},
    }


    bars = []
    for setting in ['long6', 'short1']:
        bar_list = []
        width = (sep / 2) * 0.9
        if 'long' in setting:
            width *= -1

        train_hist, edges = duration[setting]['train']
        x = (edges[1:] + edges[:-1]) / 2
        test_hist, _ = duration[setting]['test']
        test_bar = plt.bar(x, train_hist + test_hist, align='edge', width=width, color=colors[setting]['test'])
        train_bar = plt.bar(x, train_hist, align='edge', width=width, color=colors[setting]['train'])
        bars += [train_bar, test_bar]

    plt.rcParams.update({'font.size': 15})
    plt.legend(bars, ('long/train', 'long/test', 'short/train', 'short/test'))
    plt.xticks(bins)
    plt.xlabel('Time Duration (s)', fontsize=15)
    plt.ylabel('Number of Choices', fontsize=15)
    plt.savefig('duration.pdf')

def draw_steps():
    metadata = {}
    for phase in ['train', 'test']:
        metadata[phase] = json.load(open(f'./metadata/long6/{phase}.json'))
    # prepare hist
    num_steps = {}
    sep = 1
    bins = np.arange(0.5, 8.5, sep)

    for phase, problems in metadata.items():
        num_steps_list = []
        for item in problems:
            for c in item['choices']:
                num_steps_list.append(len(c['steps']))
        num_steps[phase] = np.histogram(num_steps_list, bins=bins)


    fig = plt.figure(figsize=(10, 10))

    colors = {
        'train': (1, 0, 0),
        'test': (1, 0, 0, 0.5),
    }


    bars = []
    width = (sep / 2) * 0.9
    train_hist, edges = num_steps['train']
    x = (edges[1:] + edges[:-1]) / 2
    test_hist, _ = num_steps['test']
    test_bar = plt.bar(x, train_hist + test_hist, align='center', width=width, color=colors['test'])
    train_bar = plt.bar(x, train_hist, align='center', width=width, color=colors['train'])
    bars += [train_bar, test_bar]

    plt.rcParams.update({'font.size': 15})
    plt.legend(bars, ('train', 'test'))
    plt.xticks(x)
    plt.xlabel('Number of Steps', fontsize=15)
    plt.ylabel('Number of Choices', fontsize=15)
    plt.savefig('steps.pdf')


def draw_count():
    counts = {
        'train': [],
        'test': []
    }
    settings = ['short1'] + [f'long{i}' for i in range(2, 7)]
    for setting in settings:
        for phase in ['train', 'test']:
            metadata = json.load(open(f'./metadata/{setting}/{phase}.json'))
            counts[phase].append(len(metadata))
    # prepare hist
    sep = 1
    bins = np.arange(0.5, 8.5)

    fig = plt.figure(figsize=(10, 10))

    colors = {
        'train': (1, 0, 0),
        'test': (1, 0, 0, 0.5),
    }

    bars = []
    width = (sep / 2) * 0.9
    train_hist = np.array(counts['train'])
    x = np.arange(1, 7)
    test_hist = np.array(counts['test'])
    test_bar = plt.bar(x, train_hist + test_hist, align='center', width=width, color=colors['test'])
    train_bar = plt.bar(x, train_hist, align='center', width=width, color=colors['train'])
    bars += [train_bar, test_bar]

    plt.rcParams.update({'font.size': 15})
    plt.legend(bars, ('train', 'test'))
    plt.xticks(x, ['short'] + [f'long{i}' for i in range(2, 7)])
    plt.xlabel('Setting', fontsize=15)
    plt.ylabel('Number of Problems', fontsize=15)
    plt.savefig('counts.pdf')

def draw_types():
    counts = {
        'train': {},
        'test': {}
    }

    settings = ['short1'] + [f'long{i}' for i in range(2, 7)]

    hist = {}
    for phase in ['train', 'test']:
        metadata = json.load(open(f'./metadata/long6/{phase}.json'))
        for item in metadata:
            for c in item['choices']:
                w = c['wrong_type']
                if w in counts[phase]:
                    counts[phase][w] += 1
                else:
                    counts[phase][w] = 0

        hist[phase] = [counts[phase][t] for t in ['missing', 'extra', 'swap', 'replace_same']]

    # prepare hist
    sep = 1
    fig = plt.figure(figsize=(10, 10))

    colors = {
        'train': (1, 0, 0),
        'test': (1, 0, 0, 0.5),
    }

    bars = []
    width = (sep / 2) * 0.9
    train_hist = np.array(hist['train'])
    x = np.arange(1, 5)
    test_hist = np.array(hist['test'])
    test_bar = plt.bar(x, train_hist + test_hist, align='center', width=width, color=colors['test'])
    train_bar = plt.bar(x, train_hist, align='center', width=width, color=colors['train'])
    bars += [train_bar, test_bar]

    plt.rcParams.update({'font.size': 15})
    plt.legend(bars, ('train', 'test'))
    plt.xticks(x, ['missing', 'extra', 'swapping', 'replacing'])
    plt.xlabel('Types of Wrong Choices', fontsize=15)
    plt.ylabel('Number of Choices', fontsize=15)
    plt.savefig('types.pdf')


def draw_tasks():
    tasks = {}
    COIN = json.load(open('COIN.json'))
    metadata = {}
    all_tasks = set()
    for phase in ['train', 'test']:
        metadata[phase] = json.load(open(f'metadata/long6/{phase}.json'))
        tasks[phase] = {}
        for item in metadata[phase]:
            vid = item['question'][0].split('/')[0]
            task = COIN['database'][vid]['class']
            all_tasks.add(task)
            if task not in tasks[phase]:
                tasks[phase][task] = 1
            else:
                tasks[phase][task] += 1

    all_tasks = list(all_tasks)
    hist = {
        phase: [counts.get(k, 0) for k in all_tasks] for phase, counts in tasks.items()
    }
    x = np.arange(len(all_tasks))

    sep = 1
    width = sep * 0.9

    colors = {
        'train': (1, 0, 0),
        'test': (1, 0, 0, 0.5),
    }

    fig = plt.figure(figsize=(40, 10))
    train_bar = plt.bar(x, hist['train'], align='center', width=width, color=colors['train'])
    test_bar = plt.bar(x, hist['train'], bottom=hist['test'], align='center', width=width, color=colors['test'])
    bars = [train_bar, test_bar]
    # fig.tight_layout()
    fig.subplots_adjust(bottom=0.3)
    plt.autoscale(enable=True, axis='x', tight=True)

    plt.rcParams.update({'font.size': 15})
    plt.legend(bars, ('train', 'test'))
    plt.xticks(x, all_tasks, rotation='vertical', fontsize=12)
    plt.ylabel('Number of Problems', fontsize=15)
    plt.savefig('tasks.pdf')

if __name__ == '__main__':
    # draw_duration()
    # draw_steps()
    # draw_count()
    # draw_types()
    # draw_tasks()
# vim: ts=4 sw=4 sts=4 expandtab

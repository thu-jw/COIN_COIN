#!/usr/bin/env python3
import torch
from torchvision import transforms
import json
from torch.utils.data import Dataset, DataLoader
import cv2
from glob import glob
from PIL import Image
import argparse

class COIN_COIN_Dataset(Dataset):
    def __init__(self, args):
        self.setting = args.setting
        self.phase = args.phase
        self.max_length = args.max_length
        self.metadata = json.load(open(f'metadata/{self.setting}/{self.phase}.json', 'r'))

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
        ])

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, index):
        """
        question: (2, 3, H, W)
        choices: (4, M, 8, 3, H, W)
        label: (4)
        """
        qa = self.metadata[index]
        question = torch.cat([self.transform(Image.open(f'data/{q}')).unsqueeze(0) for q in qa['question']], dim=0)

        choices = torch.cat([
            self.pad(torch.cat([self.load_step(s) for s in c['steps']], dim=0), max_length=self.max_length).unsqueeze(0) # (L, 8, 3, H, W)
            for c in qa['choices']
        ], dim=0)

        label = torch.Tensor([c['correct'] for c in qa['choices']])
        return question, choices, label

    def load_step(self, step):
        """
        load 8 frames from the step
        return size: (8, 3, H, W)
        """
        paths = sorted(glob(f'data/{step}/*.jpg'))[::2]
        images = torch.cat([self.transform(Image.open(path)).unsqueeze(0) for path in paths], dim=0)
        return images.unsqueeze(0)

    def pad(self, choice, max_length=6):
        """
        choice: (L, 8, 3, H, W)
        return: (M, 8, 3, H, W)
        """
        L = choice.shape[0]
        assert L <= max_length
        if L == max_length:
            return choice
        zero = torch.zeros((max_length - L, *choice.shape[1:]))
        return torch.cat([choice, zero], dim=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-M', '--max_length', type=int, default=6)
    parser.add_argument('--setting', default='long')
    parser.add_argument('--phase', default='train')
    args = parser.parse_args()

    dataloader = DataLoader(
        dataset=COIN_COIN_Dataset(args),
        batch_size=2, shuffle=True,
        num_workers=16
    )

    batch = next(iter(dataloader))
    for i in batch:
        print(i.shape)

# vim: ts=4 sw=4 sts=4 expandtab

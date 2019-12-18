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

if __name__ == "__main__":
    d = load_action_dict()
    for i in range(1, 779):
        if i not in d:
            print(i)

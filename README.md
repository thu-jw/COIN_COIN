# COIN COIN

## Data
- Extracted frames:
Extract 16 frames for each action
`/opt/data5/COIN_COIN/{video_name}/{action_index}/img_*.jpg`

- Washed data:
Ensure there is only one task in each clip.

`/opt/data5/COIN_COIN_washed/{video_name}/{clip_index}/{action_index}/img_*.jpg`

## Files
- COIN.json: original annotation of COIN
- COIN_COIN.json: annotation of COIN_COIN, the format is (only useful keys are listed): 
```python
[
  {
    "pk": 1, # primary key
    "fields": {
      "video_name": "4MiubN1oQkg",
      "video_class": "ArcWeld",
      "cut_points": "",
      "state": 2, # 2 for finished
      "steps": 3,
      "train": false, # belongs to the train/val set
      "action_ids": "587,585,587",
    }
  },
]
```
- gen_actions.py: extract 16 frames for each action
- gen_dataset.py: generate washed COIN_COIN dataset
- anno_tool: a web annotation tool
- data/data_washed: symlinks to /opt/data5/COIN_COIN and /opt/data5/COIN_COIN_washed


## Steps
- generate split json file
```python
[
  {
	  "video_name": "4MiubN1oQk
	  "video_class": "ArcWeld",
	  "action_ids": "587,585,587",
	  "clips": [[0, 2), [2, 3)]
	  "num_clips": 2,
  },
]
```

- use gurobi to split train and val

```python
[
  {
	  "video_name": "4MiubN1oQkg",
	  "video_class": "ArcWeld",
	  "clips": [[0, 1], [2, 3]]
	  "steps": 3,
	  "action_ids": "587,585,587",
	  "train": false
  },
]
```
- generate question and answer pair
```python

[
	{
		"question": [path/to/img1, path/to/img2]
		"choices": [
			[path/to/choices/1],
			[path/to/choices/2],
			[path/to/choices/3],
			[path/to/choices/4],
		]
	}
]
```

# COIN COIN

## Files
- COIN.json: original annotation of COIN
- anno_tool: annotation tool
- data_gen: codes to generate COIN COIN
	- gen_frames.py: extract 16 frames per action
	- gen_dataset.py: generate metadata of COIN COIN dataset
	- gen_gifs.py: generate gif for each action for visualization

- data_raw: 

## Usage
### Annotation
Extract 16 frames for each action:
```
python data_gen/gen_frames.py
```

After finished annotating using anno_tool, dump annotation results to json:

```
cd anno_tool
python manage.py dumpdata anno -o ../data_gen/anno.json
```

The format of annotation is (only useful keys are listed): 

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

### Generate COIN_COIN metadata
```
python data_gen/gen_dataset.py -s <setting> -m <min length of clip> -M <max length of clip> -r <test-ratio>
```

- setting: `short` or `long`
- the number of actions in each clip must between `m` and `M`. For `short` setting, `(m, M) = (1, 1)` by default; For `long` setting, `(m, M) = (2, 5)` by default
- percentage of test set is <test-ratio> approximately (default: 0.1)

data_gen/gen_dataset.py will perform the following steps:

1. filter_clips: Cut the clips longer than `M` and drop the clips shorter than `m`
2. split_train_test: Split the whole dataset into train and test set, ensuring that the clips from the same video are not seperated.
3. gen_QA: Generate questions and choices. There are 4 types of wrong answers:
	- missing step
	- swapped steps
	- extra step, from the same video
	- replaced step, from other videos in the same class
In `long` setting, all of the above types of wrong answers will appear; in `short` setting only `replaced step` will appear.

The metadata will saved in `metadata/<setting>/<phase>.json` in the following format:
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
	...
]
```
To visualize the dataset, run
```
python data_gen/gen_gifs.py
```
and visit `http://166.111.72.69:61081` and go to `Dataset` tab.

### Training
`dataset.py` provides the way to load the dataset. Each batch contains 
- question: `(batch_size, 2, channel=3, height, width)`
- choices: `(batch_size, 4, max_length, num_frames=8, channel=3, height, width)`
- label: `(batch_size, 4)`

For `long` setting, `max_legnth = M + 1` (the length of choice with wrong type of `extra` is `M + 1`); For `short` setting, `max_legnth = 1`. Currently, all the images are padded and resized to `(256, 256)`.

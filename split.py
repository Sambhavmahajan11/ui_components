import os
import random

# Path to the directory containing converted annotations
annotations_dir = './yolo_train/annotations'

# Split ratio for training and validation (e.g., 80% training, 20% validation)
train_ratio = 0.8

# Output file paths for training and validation files
train_file = './training.txt'
valid_file = './validation.txt'

# Collect all annotation file paths
annotation_files = []
for filename in os.listdir(annotations_dir):
    if filename.endswith('.txt'):
        annotation_files.append(os.path.join(annotations_dir, filename))

# Shuffle the list of annotation files
random.shuffle(annotation_files)

# Calculate the split index based on the train_ratio
split_index = int(len(annotation_files) * train_ratio)

# Split the annotation files into training and validation sets
train_annotations = annotation_files[:split_index]
valid_annotations = annotation_files[split_index:]

# Write the training file
with open(train_file, 'w') as f_train:
    for annotation in train_annotations:
        f_train.write(annotation + '\n')

# Write the validation file
with open(valid_file, 'w') as f_valid:
    for annotation in valid_annotations:
        f_valid.write(annotation + '\n')

import re
import json
from collections import defaultdict
"""
This script is used to standardize the tags in the datasets found in the dataset directory
""" 

dataset_paths = {
    "cora": "./dataset/cora-ie/tagged_references.txt",
    "umass_1": "./dataset/umass-citation/training.docs",
    "umass_2": "./dataset/umass-citation/testing.docs",
    "umass_3": "./dataset/umass-citation/dev.docs",
}

# to collate tags available in dataset (tags are manually matched)
dataset_tags = dict()
for dataset in dataset_paths:
    with open(dataset_paths[dataset], encoding='utf-8', errors='ignore') as f:
        text = f.read()
        tags = set(re.findall(r'(?<=<)\w+(?=>)', text))
        dataset_tags[dataset] = tags

# manual mapping is done to match tags in cora dataset to those in the umass-citation dataset
cora_to_umass_mapping = {
    "author": "authors",
    "booktitle": "booktitle",
    "date": "date",
    "editor": "editor",
    "journal": "journal",
    "location": "address",
    "institution": "institution",
    "note": "note",
    "publisher": "publisher",
    "pages": "pages",
    "tech": "tech",
    "title": "title",
    "volume": "volume"
}

tag_mapping = {
    "cora": {key: key for key in dataset_tags["cora"]},
    "umass_1": cora_to_umass_mapping,
    "umass_2": cora_to_umass_mapping,
    "umass_3": cora_to_umass_mapping
}

def replaceTags(standardized_tags, tag_mapping, reference):
    standardized_reference = reference
    for standardized_tag in standardized_tags:
        reference_tag = tag_mapping[standardized_tag]
        standardized_reference = re.sub(r'(?<=\<)' + reference_tag + r'(?=\>)', standardized_tag, standardized_reference)
        standardized_reference = re.sub(r'(?<=\<\/)' + reference_tag + r'(?=\>)', standardized_tag, standardized_reference)
    return str.rstrip(standardized_reference)


standardized_references = []

for dataset in dataset_paths:
    with open(dataset_paths[dataset], encoding='utf-8', errors='ignore') as f:
        references = f.readlines()
        for reference in references:
            standardized_references.append(replaceTags(dataset_tags["cora"], tag_mapping[dataset], reference))

output_file = "./dataset/standardized_dataset.txt"
with open(output_file, 'w', errors='ignore') as f:
    f.write("\n".join(standardized_references))
    
tag_file = "./utils/tags.txt"
with open(tag_file, 'w', errors='ignore') as f:
    f.write("\n".join(dataset_tags["cora"]))

"""
For reference:
print(dataset_tags)
"""
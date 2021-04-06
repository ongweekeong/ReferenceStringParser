import re
with open("./dataset/standardized_dataset.txt") as f:
    lines = f.readlines()
    unlabelled = []
    for line in lines:
        unlabelled.append(re.sub(r'\<\/?[\w-]*\>\s*', "", line).strip())

with open("./dataset/unlabelled_dataset.txt", 'w', encoding="utf-8") as f:
    f.write("\n".join(unlabelled))
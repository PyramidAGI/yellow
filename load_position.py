import os

DIR = os.path.dirname(__file__)
TARGET = os.path.join(DIR, "position_tree.csv")

filename = input("Filename to load into position_tree.csv: ").strip()
src = os.path.join(DIR, filename)

with open(src) as f:
    content = f.read()

with open(TARGET, "w") as f:
    f.write(content)

print(f"position_tree.csv updated from {filename}")

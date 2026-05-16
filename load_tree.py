import os

DIR = os.path.dirname(__file__)
TARGET = os.path.join(DIR, "tree1.csv")

filename = input("Filename to load into tree1.csv: ").strip()
src = os.path.join(DIR, filename)

with open(src) as f:
    content = f.read()

with open(TARGET, "w") as f:
    f.write(content)

print(f"tree1.csv updated from {filename}")

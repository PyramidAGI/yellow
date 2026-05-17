# Sign Tree

## Requirements

```
pip install pygame-ce
```


A visual tool for arranging symbolic signs in a binary tree structure.

## Programs

### tree.py

Displays 12 signs in a tree with 1 root, 3 branches, and 8 leaves. Signs are drawn from the custom sign library in `zodiac_lines.py`.

**Controls:**

| Key | Action |
|-----|--------|
| R | Randomize signs |
| N | Launch a ball along a random path from root to leaf |
| B | Toggle black / white background |
| S | Save current tree to `tree1.csv` |
| L | Load tree from `tree1.csv` |

### load_tree.py

Command-line utility to replace the active tree file (`tree1.csv`) with another saved tree file.

**Usage:**
```
python load_tree.py
```
Enter a filename (e.g. `tree2.csv`) when prompted. The contents will be copied into `tree1.csv`, which `tree.py` uses for save/load.

### template_program.py

A command-line tool for logging and inspecting clusters in `log.csv`. A cluster is a group of rows belonging to one natural language sentence, delimited by empty rows.

**CSV format** (semicolon-delimited, 9 fields):

| natural language input | e0 | e1 | e2 | e3 | e4 | v | threshold | message output |

Only the first row of a cluster has the sentence; subsequent rows in the same cluster leave it empty.

**Commands:**

| Input | Action |
|-------|--------|
| `l` | Log the example cluster from `examplecluster.txt` to `log.csv` |
| `c` | Check `log.csv` for formatting errors |
| `count` | Print the number of clusters in `log.csv` |
| `g` | Get a cluster by number and print its rows |
| `recall` | Append a cluster to the end of `log.csv` |
| `s` | Solve a cluster (calls LLM, prints result) |
| `q` | Quit |

## Tree files

- `tree1.csv` — active tree (used by tree.py)
- `tree2.csv`, `tree3.csv` — additional saved trees, load with `load_tree.py`

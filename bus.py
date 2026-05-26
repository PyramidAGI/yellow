# Runs in the batch (run_yellow.bat). Each node has its own log file (log0.csv, log1.csv, ...).
# For each node, messages are pulled from source nodes and written to the current node's log.
# direction="up"   → source nodes are the children (up to 3), aggregating upward
# direction="down" → source node is the parent (1), propagating downward
import template_program

CHILDREN = {0: [1, 2, 3], 1: [4, 5, 6], 2: [7, 8, 9], 3: [10, 11]}
PARENT = {child: parent for parent, children in CHILDREN.items() for child in children}
NUM_NODES = 12

def routing(direction, node):
    if direction == "up":
        return CHILDREN.get(node, [])
    if direction == "down":
        return [PARENT[node]] if node in PARENT else []
    return []

def get_log(node):
    template_program.CONST = node
    return template_program.get_cluster(-1)

def put_log(node, rows):
    template_program.CONST = node
    sentence = rows[0][0] or f"node {node}"
    matches = [";".join(row[1:]) for row in rows]
    template_program.log(sentence, matches)

def iterate_nodes():
    for node in range(NUM_NODES):
        for direction in ("up", "down"):
            for src in routing(direction, node):
                rows = get_log(src)
                if rows:
                    put_log(node, rows)

if __name__ == "__main__":
    iterate_nodes()
    print("Bus iteration complete.")

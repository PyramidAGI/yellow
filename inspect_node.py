#                  0
#              /   |   \
#             1    2    3
#           / | \ /|\ / \
#          4  5  6 7 8 9 10 11

CHILDREN = {0: [1, 2, 3], 1: [4, 5, 6], 2: [7, 8, 9], 3: [10, 11]}
PARENT = {child: parent for parent, children in CHILDREN.items() for child in children}

NUM_NODES = 12
NODE = 2

def routing(direction, node):
    if direction == "up":
        return CHILDREN.get(node, [])
    if direction == "down":
        return [PARENT[node]] if node in PARENT else []
    return []

print("                 0")
print("             /   |   \\")
print("            1    2    3")
print("          / | \\ /|\\ / \\")
print("         4  5  6 7 8 9 10 11")
print()

for node in range(NUM_NODES):
    for direction in ("up", "down"):
        for src in routing(direction, node):
            print(f"node {node} <- {direction} <- node {src}")

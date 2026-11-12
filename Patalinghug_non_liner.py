
import sys
from collections import deque



def make_labels(name):
    letters = [c for c in name.upper() if c.isalpha()]
    if not letters:
        raise ValueError("Please enter a name with letters.")
    total = {c: letters.count(c) for c in set(letters)}
    seen = {}
    labels = []
    for c in letters:
        seen[c] = seen.get(c, 0) + 1
        labels.append(c if total[c] == 1 else f"{c}{seen[c]}")
    return labels


def plain(labels):
    """A1 -> A (drop the numbers for the printed result)."""
    return " - ".join(label[0] for label in labels)



class Node:
    def __init__(self, label):
        self.label = label
        self.left = None
        self.right = None


def build_tree(name):
    nodes = [Node(label) for label in make_labels(name)]
    for i, node in enumerate(nodes):
        left, right = 2 * i + 1, 2 * i + 2
        if left < len(nodes):
            node.left = nodes[left]
        if right < len(nodes):
            node.right = nodes[right]
    return nodes[0]


def tree_levels(root):
    result, queue = [], deque([(root, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth == len(result):
            result.append([])
        result[depth].append(node.label)
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return result


def tree_children(root):
    lines, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        kids = [k.label for k in (node.left, node.right) if k]
        if kids:
            lines.append(f"{node.label} has {' and '.join(kids)}.")
        for k in (node.left, node.right):
            if k:
                queue.append(k)
    return lines


def tree_bfs(root):

    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.label)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


def tree_preorder(node, result=None):

    if result is None:
        result = []
    if node is None:
        return result
    result.append(node.label)
    tree_preorder(node.left, result)
    tree_preorder(node.right, result)
    return result


def tree_inorder(node, result=None):

    if result is None:
        result = []
    if node is None:
        return result
    tree_inorder(node.left, result)
    result.append(node.label)
    tree_inorder(node.right, result)
    return result


def tree_postorder(node, result=None):
    
    if result is None:
        result = []
    if node is None:
        return result
    tree_postorder(node.left, result)
    tree_postorder(node.right, result)
    result.append(node.label)
    return result



BASE_EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (1, 5), (4, 5), (5, 6),
              (2, 6), (2, 7), (2, 3), (6, 7), (7, 8), (8, 3), (8, 9), (3, 9)]


def get_edges(n):
    edges = [(a, b) for a, b in BASE_EDGES if a < n and b < n]
    for i in range(10, n):              # extra letters beyond 10
        edges += [(i - 2, i), (i - 1, i)]
    return edges


def build_graph(name):
    vertices = make_labels(name)
    edges = get_edges(len(vertices))
    graph = {v: [] for v in vertices}
    for a, b in edges:
        graph[vertices[a]].append(vertices[b])
        graph[vertices[b]].append(vertices[a])
    for v in graph:
        graph[v].sort(key=vertices.index)
    named_edges = [(vertices[a], vertices[b]) for a, b in edges]
    return vertices, named_edges, graph


def graph_bfs(graph, start):
    visited = [start]
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
    return visited


def graph_dfs(graph, start):
    """
    One DFS gives all three orders:
    - preorder : the order vertices are first visited
    - postorder: the order vertices are finished (all neighbors done)
    - inorder  : a graph has no left/right, so it is taken on the DFS tree:
                 first child's subtree, then the vertex, then the other
                 children's subtrees (children in the order they were visited)
    """
    visited, pre, post = set(), [], []
    kids = {v: [] for v in graph}

    def visit(v):
        visited.add(v)
        pre.append(v)                           # preorder
        for neighbor in graph[v]:
            if neighbor not in visited:
                kids[v].append(neighbor)
                visit(neighbor)
        post.append(v)                          # postorder

    visit(start)

    def inorder(v):
        out = []
        if kids[v]:
            out += inorder(kids[v][0])
        out.append(v)
        for child in kids[v][1:]:
            out += inorder(child)
        return out

    return pre, inorder(start), post



def main():
    name = sys.argv[1] if len(sys.argv) > 1 else input("Enter last name: ")
    print(f"\nName: {name.upper()}\n")

    # Diagram 1
    root = build_tree(name)
    print("=== DIAGRAM 1: BINARY TREE ===")
    for depth, group in enumerate(tree_levels(root)):
        print(f"Level {depth}: {', '.join(group)}")
    print("Children:", " ".join(tree_children(root)))
    print("BFS result:           ", plain(tree_bfs(root)))
    print("DFS Preorder result:  ", plain(tree_preorder(root)))
    print("DFS Inorder result:   ", plain(tree_inorder(root)))
    print("DFS Postorder result: ", plain(tree_postorder(root)))
    print()

    # Diagram 2
    vertices, edges, graph = build_graph(name)
    start = vertices[0]
    pre, ino, post = graph_dfs(graph, start)
    print("=== DIAGRAM 2: GRAPH ===")
    print("Vertices:", ", ".join(vertices))
    print("Edges:", ", ".join(f"{a}-{b}" for a, b in edges))
    print("Start vertex:", start)
    print("Adjacency list:")
    for v in vertices:
        print(f"  {v} -> {' -> '.join(graph[v])}")
    print("BFS result:           ", plain(graph_bfs(graph, start)))
    print("DFS Preorder result:  ", plain(pre))
    print("DFS Inorder result:   ", plain(ino))
    print("DFS Postorder result: ", plain(post))


if __name__ == "__main__":
    main()
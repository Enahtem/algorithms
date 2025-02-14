# Starts with nodes that have no links pointing to it.
# removes them to add to sorted node list, then remove the link that points to their children
# loop for nodes that now have no nodes without links.

# Used to extract a linear order to a complex interlinked list of dependencies


def topological_sort(graph, nodes):
    # Step 1: Compute in-degree for each node
    in_degree = {node: 0 for node in nodes}
    for node in nodes:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Step 2: Identify nodes with zero in-degree
    queue = []
    for node in nodes:
        if in_degree[node] == 0:
            queue.append(node)

    result = []

    while queue:
        node = queue.pop(0)  # Remove the first element (FIFO)
        result.append(node)

        # Step 3: For each neighbor of the node, reduce in-degree
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If the result contains all the nodes, return it; otherwise, there's a cycle
    if len(result) == len(nodes):
        return result
    else:
        return "Graph has a cycle, topological sort not possible"


# Example usage:
graph = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []}
nodes = ["A", "B", "C", "D", "E"]

print(topological_sort(graph, nodes))

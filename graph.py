# There are no restrictions on how you must store
# class or instance variables for this project.
# Use whatever makes the most sense for your
# design and implementation.


"""

graph.py - This file implements various properties of a graph.

Considered Graph representation in the Implementation
G = {"vertex1":[{'vertex2':weight},{'vertex3':weight1}]} 

"""


class node:
    """
    node - Creats a node for the graph

    """

    def __init__(self, label):
        """
        Parameter: a string indicating the label of the new node
        """
        self.node_val = label
        self.edges = []
        self.indegree = 0
        self.outdegree = 0

    def in_degree(self):
        """
        Parameter: none
        Return value: integer representing the in-degree of
        this node
        """
        return self.indegree

    def out_degree(self):
        """
        Parameter: none
        Return value: integer representing the out-degree of
        this node
        """
        return self.outdegree

    def __str__(self):
        """
        Parameter: none
        Return value: string label of the node
        """
        return str(self.node_val)


class Graph:
    def __init__(self, directed):
        """
        Parameter: a boolean indicating whether the new instance
        of Graph will be directed (True) or undirected (False)
        Post condition: new instance of an empty graph is
        created
        """
        if directed:
            self.isdirected = True
        else:
            self.isdirected = False
        self.graph = {}

    def num_vertices(self):
        """
        Parameters: none
        Return value: integer corresponding to the total number
        of vertices in the graph
        """
        return len(list(self.graph.keys()))

    def num_edges(self):
        """
        Parameters: none
        Return value: integer corresponding to the total number
        of edges in the graph
        """
        total_len = 0
        for i in list(self.graph.values()):
            total_len += len(i)
        if self.isdirected:
            return total_len
        else:
            """
            Since the number of edges in a Undirected graph
            is half times the directed graph.
            """
            return int(total_len / 2)

    def is_directed(self):
        """
        Parameters: none
        Return value: boolean - True if this instance of the
        Graph class is a directed graph, False otherwise
        """
        if self.isdirected:
            return True
        else:
            return False

    def is_weighted(self):
        """
        Parameters: none
        Return value: boolean - True if any edge in the Graph
        has a weight other than 1, False otherwise
        """
        # Traverse the list of edges of every vertex, here we traverse list of dictionaries
        for i in list(self.graph.values()):
            for dic in i:
                for key in dic:
                    if dic[key] != 1:
                        return True
        return False

    def add_node(self, label):
        """
        Parameter: a string indicating the label of a new node
        in the Graph
        Return value: none
        Assumptions: labels of nodes in the Graph must be unique
        """
        if label in list(self.graph.keys()):
            raise (DuplicateNode("Duplicated node inserted"))

        n = node(label)
        self.graph[label] = n.edges

    def remove_node(self, label):
        """
        Parameter: a string indicating the label of an existing
        node in the Graph
        Return value: none
        Post conditions: the node with the given label, as well
        as any edges to/from that node, are removed from the
        graph
        """
        if label not in list(self.graph.keys()):
            raise NodeNotFound("Given Node not found.")

        # Deleting the vertex
        del self.graph[label]
        # Deleting corresponding edges of vertex, by traversing the corresponding edges
        for k, v in self.graph.items():
            for edges in v:
                for key in edges:
                    if key == label:
                        idx = v.index(edges)
                    del v[idx]

    def add_edge(self, n1, n2, weight=1):
        """
        Parameters:
            two strings, indicating the labels of the
            nodes connected by the new edge. If this is a directed
            Graph, then the edge will be FROM n1 TO n2.

            a numeric value (int/float) for a weight of the edge
        Return value: none
        Assumptions: the combination of (n1, n2, weight) must
        be unique in the Graph
        Post conditions: one new edge is added to the Graph
        """
        if (n1 not in list(self.graph.keys())) or (n2 not in (self.graph.keys())):
            raise NodeNotFound("Given Node not found.")

        for k in self.graph:
            if k == n1:
                for v in self.graph[k]:
                    for key, w in v.items():
                        # since combination of (n1, n2, weight) is unique
                        if key == n2 and weight == w:
                            raise DuplicateEdge("Duplicate Edge Inserted")

        self.graph[str(n1)].append({str(n2): weight})
        if not self.isdirected:
            # In undirected graph (a,b) = (b,a) edge.
            self.graph[str(n2)].append({str(n1): weight})

    def remove_edge(self, n1, n2, weight=1):
        """
        Parameters:
            two strings, indicating the labels of the
            nodes connected by the edge. If this is a directed
            Graph, then the edge will be FROM n1 TO n2.

            a numeric value (int/float) for a weight of the edge
        Return value: none
        Post conditions: the edge with the given nodes and weight
        is removed from the graph
        """
        flag = 0
        # Traversing all the vertices and their corresponding edges
        for k in self.graph:
            if k == n1:
                for v in self.graph[k]:
                    for key, w in v.items():
                        if key == n2 and weight == w:
                            flag = 1
                            idx1 = self.graph[k].index({key: w})
                            del self.graph[k][idx1]
                            if not self.isdirected:
                                # For a undirected graph we delete edges from both the vertices
                                idx2 = self.graph[key].index({k: w})
                                del self.graph[key][idx2]
        # Flag is not invoked if the edge is not present
        if flag == 0:
            raise EdgeNotFound("Given Edge Not Found")

    def BFS(self, source):
        """
        Parameter: a string indicating the label of an existing
        node in the Graph
        Return value: a list of node objects, which is the
        Breadth First Search starting at source
        """
        visited, remaining = [], [source]

        if list(self.graph.keys()) is None:
            return []
        while remaining:
            _n = remaining.pop()
            visited.append(_n)
            for edge in self.graph[_n]:
                for k, v in edge.items():
                    if k not in visited and k not in remaining:
                        remaining.insert(0, k)

        nodes_visited = []
        for i in visited:
            nodes_visited.append(node(i))
        return nodes_visited

    def DFS(self, source):
        """
        Parameter: a string indicating the label of an existing
        node in the Graph
        Return value: a list of node objects, which is the
        Depth First Search starting at source
        """
        visited, remaining = [], [source]

        if list(self.graph.keys()) is None:
            return []
        while remaining:
            _n = remaining.pop()
            visited.append(_n)
            for edge in self.graph[_n]:
                for k, v in edge.items():
                    if k not in visited and k not in remaining:
                        remaining.append(k)

        nodes_visited = []
        for i in visited:
            nodes_visited.append(node(i))
        return nodes_visited

    def has_edge(self, n1, n2):
        """
        Parameters:
            two strings, indicating the labels of the
            nodes connected by the new edge. If this is a directed
            Graph, then the edge will be FROM n1 TO n2.
        Return value: a boolean - True if there is an edge in the
            Graph from n1 to n2, False otherwise
        """
        if n1 not in self.graph:
            raise NodeNotFound("Nodenotfound Exception: Given Node not found.")

        for k in self.graph:
            if k == n1:
                for v in self.graph[k]:
                    for key, w in v.items():
                        if key == n2:
                            return True

        return False

    def get_path(self, n1, n2, graph_path=[]):
        """
        Parameters:
            two strings, indicating the labels of the
            nodes you wish to find a path between. The path will be
            FROM n1 TO n2.
        Return value: a list L of node objects such that L[0] has
            label n1, L[-1] has label n2, and for 1 <= i <= len(L) - 1,
            the Graph has an edge from L[i-1] to L[i]
        """
        if (n1 not in list(self.graph.keys())) or (n2 not in (self.graph.keys())):
            raise NodeNotFound("Given Node not found.")

        graph_path = graph_path + [n1]
        if n1 == n2:
            return graph_path
        if n1 not in self.graph:
            return None

        # Traversing edges of the particular n1 vertex
        for edge_ in self.graph[n1]:
            for key, _ in edge_.items():
                if key not in graph_path:
                    # Recursively exploring all the edges of vertex
                    new_path = self.get_path(key, n2, graph_path)
                    if new_path:
                        return new_path
        return None

    def get_adjacent_nodes(self, label):
        """
        Parameter: a string indicating the label of an existing
        node in the Graph
        Return value: a list of node objects containing all nodes
        adjacent to the node with the given label
        """
        if label not in list(self.graph.keys()):
            raise NodeNotFound("Given Node not found.")

        adjacent_nodes = []
        for k in self.graph:
            if k == label:
                for v in self.graph[k]:
                    for key, w in v.items():
                        adjacent_nodes.append(node(key))
        return adjacent_nodes


class NodeNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        print(self.message)


class EdgeNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        print(self.message)


class DuplicateNode(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        print(self.message)


class DuplicateEdge(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        print(self.message)


"""
If a label is provided that is supposed to exist in the Graph
and a node with that label does not exist, the method should raise 
a "NodeNotFound" exception.

If the remove_edge method is called for an edge that does not 
exist in the Graph, the method should raise an "EdgeNotFound"
exception.

If a method call would result in a duplicate label or duplicate 
edge being added to the Graph, a "DuplicateNode" or "DuplicateEdge"
exception should be raised.

If you are not familiar with defining custom exceptions in Python3,
it's not too complicated. Check out this source for explanation and
examples:
https://www.askpython.com/python/python-custom-exceptions
"""

"""
--- Day 23: LAN Party ---
https://adventofcode.com/2024/day/23


"""


from collections import defaultdict, deque
from time import perf_counter
import duckdb


def load_graph(network_map: str) -> dict[str, set[str]]:
    graph = defaultdict(set)
    for line in network_map.strip().split():
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)
    return graph

def find_cycles(startNode: str, graph: dict[str, set[str]]) -> deque[set[str]]:
    cycles = deque()
    for midNode in graph[startNode]:
        triNodes = [node for node in graph[midNode] if node != startNode]
        for triNode in triNodes:
            cycle = {startNode, midNode, triNode}
            if (startNode in graph[triNode]) and (cycle not in cycles):
                cycles.append(cycle)
    return cycles


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"), help="file input to run the code with")
    parser.add_argument("-v", action="store_true", help="verbose")
    parser.add_argument(
        "--test",
        action="store_true",
        help="ignores file input and runs test file `example`",
    )
    args = parser.parse_args()

    if args.test:
        filename = "example.txt"
        file = open(filename, "r")
    elif args.f:
        file = args.f
    else:
        raise Exception("File or test must be specified")

    print()
    print(" Part I ".center(50, "-"))
    # network_graph = load_graph(file.read())
    oneway_conn = duckdb.read_csv(file.name, sep="-", header=False, names=["con_from", "con_to"])
    connections = oneway_conn.union(oneway_conn.select("con_to", "con_from")).order("con_from ASC")

    # party = duckdb.sql(query="""
    # WITH RECURSIVE parties(startNode, endNode, party, cycle) AS (
    #     SELECT
    #         con_from AS startNode
    #         , con_to AS endNode
    #         , [startNode] AS party
    #         , False AS cycle
    #     FROM connections
    #     -- WHERE con_from ^@ 't'
    #     UNION ALL
    #     SELECT
    #         parties.startNode AS startNode
    #         , conn.con_to AS endNode
    #         , array_append(party, endNode) AS party
    #         , startNode = endNode AS cycle
    #     FROM parties
    #     JOIN connections conn ON parties.endNode = conn.con_from
    #     WHERE
    #           (len(party) < 2 AND parties.startNode <> conn.con_to)
    #        OR (len(party) = 2 AND parties.startNode =  conn.con_to)
    # )

    # SELECT party FROM parties
    # WHERE len(party) = 3
    # QUALIFY ROW_NUMBER() OVER (PARTITION BY LIST_SORT(party) ORDER BY party) = 1
    # """)

    party = duckdb.sql(query="""
    SELECT
        [p1.con_from, p2.con_from, p3.con_from] AS party
    FROM connections AS p1
    INNER JOIN connections AS p2
      ON p1.con_to = p2.con_from
      AND p1.con_from <> p2.con_to
    INNER JOIN connections AS p3
      ON p2.con_to = p3.con_from
      AND p1.con_from = p3.con_to
    WHERE p1.con_from ^@ 't'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY LIST_SORT(party) ORDER BY party) = 1
    """)

    start = perf_counter()
    graph = load_graph(file.read())
    nodes = (node for node in graph if node.startswith('t'))
    cycles = deque(find_cycles(next(nodes), graph))
    for node in nodes:
        [cycles.append(cycle) for cycle in find_cycles(node, graph) if cycle not in cycles]

    t_parties = len(cycles)
    # t_parties = party.shape[0]
    timing = perf_counter() - start
    print(f"The number of multiplayer parties with a T computer are ({t_parties})")
    print(f"Elapsed time: {timing: 0.7f} s")

    if args.test:
        ans = 7
        assert t_parties == ans, f"The number of multiplayer parties didn't match the expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    start = perf_counter()
    degrees = duckdb.sql(query="""
    SELECT
        con_from AS node
        , list(con_to) AS neighbors
        , len(neighbors) AS degrees
    FROM connections
    GROUP BY con_from
    ORDER BY node
    """)

    connect_components = duckdb.sql(query="""
    SELECT
        list_sort(list_cat([d1.node, d2.node], list_intersect(d1.neighbors, d2.neighbors))) AS clique
        , len(clique) k_clique
    FROM degrees d1
    JOIN degrees d2
      ON d2.node IN d1.neighbors
    """)

    cliques = (
        connect_components.aggregate("clique, k_clique, COUNT(*) AS count_clique")
        .filter("count_clique > k_clique")
        .order("count_clique DESC")
    )

    maximum_clique = cliques.project("clique")
    password = ",".join(*maximum_clique.fetchone())
    timing = perf_counter() - start
    print(f"The password is '{password}'")
    print(f"Elapsed time: {timing: 0.7f} s")

    if args.test:
        ans = 'co,de,ka,ta'
        assert password == ans, f"Password did not match '{ans}'"

    # _ = duckdb.sql(query="""
    # WITH RECURSIVE bronker(R, P, X, clique) AS (
    # ...
    # )
    # """)


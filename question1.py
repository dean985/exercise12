#!/usr/bin/env python3
from typing import List
import networkx as nx
import doctest


def count_instances(ls: List[int], x: int) -> int:
    """
    Simple function to return amount of instances of x in ls
    """
    counter = 0
    for i in ls:
        if i == x:
            counter += 1

    return counter


def find_trading_cycle(preferences: List[List[int]]) -> List[int]:
    # list of tuples of edges of the graph
    edges = []
    amount_agents = len(preferences)
    for i in range(amount_agents):
        pref_agent_i = preferences[i]
        if len(pref_agent_i) > 0:
            # edge for agent i and favorite house
            edges.append((i, pref_agent_i[0]))
            # edge for agent i and the house he owns
            edges.append((i, i))

    G = nx.DiGraph(edges)
    nx.set_node_attributes(G, False, "visited")

    next_node = list(G)[0]  # The first node in the graph
    cycle = [next_node]  # init for the cycle

    while not G.nodes[next_node]["visited"]:
        # finding the cycle
        G.nodes[next_node]["visited"] = True
        next_node = list(G[next_node])[0]

        if next_node != cycle[-1] or list(G[next_node])[0] == next_node:
            cycle.append(next_node)

    cycle = cycle[cycle.index(cycle[-1]) :]

    if len(cycle) > 1:
        return cycle
    return cycle * 2


def top_trading_cycles(preferences: List[List[int]]) -> List:
    """
    >>> top_trading_cycles([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
    [0, 1, 2]
    >>> top_trading_cycles([[2, 0, 1, 3], [0, 3, 1, 2], [3, 0, 2, 1], [2, 3, 0, 1]])
    [0, 1, 3, 2]
    >>> top_trading_cycles([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]])
    [0, 1, 2, 3]
    >>> top_trading_cycles([[2, 3, 1, 4, 0], [2, 3, 4, 0, 1], [3, 0, 4, 1, 2], [4, 0, 1, 2, 3], [0, 1, 2, 3, 4]])
    [2, 1, 3, 4, 0]
    >>> top_trading_cycles([[2, 0, 1, 3], [0, 3, 1, 2], [0, 3, 2, 1], [2, 3, 0, 1]])
    [2, 1, 0, 3]
    >>> top_trading_cycles([[0, 3, 1, 2], [0, 3, 2, 1], [0, 1, 2, 3], [0, 1, 3, 2]])
    [0, 3, 2, 1]
    """

    # init of the agent_house assignments
    agent_house = [-1] * len(preferences)
    total_agents = len(preferences)
    assigned_agents = 0
    # In words, as long as there are
    # agents that didnt get a house
    while assigned_agents < total_agents:
        cycle = find_trading_cycle(preferences)

        for i in range(len(cycle) - 1):
            assigned_agents += 1
            agent_house[cycle[i]] = cycle[i + 1]

        for i in range(total_agents):
            # remove house that were assigned
            n = agent_house[i]
            if n != -1:
                preferences[i] = list()
                for p in preferences:
                    if count_instances(p, n) != 0:
                        if len(p) > 0:
                            p.remove(n)

    # agent_house[i] is the index of house assigned to agent i
    return agent_house


if __name__ == "__main__":
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

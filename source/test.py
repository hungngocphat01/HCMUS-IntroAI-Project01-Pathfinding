import matplotlib.pyplot as plt
from Graph import Graph
from Queue import Queue
from Stack import Stack
from heuristic_func import *
from searching_algorithms import Astar, DFS
from maze_preprocess import Node
from copy import deepcopy

g = Graph('testcases/bonus2.txt')
fs = (5, 5)
g.visualize(figsize=fs)

g.clear()
print(g.end)
Astar(g, manhattan_heuristic, custom_start=(19, 11))

path, cost = g.get_path(custom_start=(19, 11))
g.visualize(path, figsize=(5,5))

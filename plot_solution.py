# this script obtains the dissimilarity metrics that optimizes the correlation

import operator
import random
import correlation_gp
import matplotlib
import matplotlib.pyplot as plt
import math
import pandas as pd
matplotlib.use('Agg')

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

depth = 4

# Define new functions
def safeDiv(left, right):
    try:
        return left / float(right)
    except ZeroDivisionError:
        return 0

def safeLog(a):
    if a > 0:
        return math.log(a)
    else:
        return 0

def safeSqrt(a):
    if a >= 0:
        return math.sqrt(a)
    else:
        return 0

pset = gp.PrimitiveSet("MAIN", 3,"a")
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safeDiv, 2)
pset.addPrimitive(safeLog, 1)
pset.addPrimitive(safeSqrt, 1)

creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_= 4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evaluation(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    result = correlation_gp.correlation(func)
    if numpy.isnan(result) == True:
        result = -1
    return result,

toolbox.register("evaluate", evaluation)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("select2", tools.selBest)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_= 4)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

#toolbox.decorate("mate", gp.staticLimit(operator.attrgetter('height'), 4))
#toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter('height'), 4))
#toolbox.decorate("expr", gp.staticLimit(operator.attrgetter('height'), 4))

toolbox.decorate("mate", gp.staticLimit(len, 80))
toolbox.decorate("mutate", gp.staticLimit(len, 80))
toolbox.decorate("expr", gp.staticLimit(len, 80))
    
def genetic():
    expr = toolbox.individual()
    sol = "safeDiv(safeSqrt(add(safeSqrt(safeSqrt(a2)), a0)), add(add(safeSqrt(safeSqrt(a0)), add(safeSqrt(a0), add(a1, a2))), add(add(safeSqrt(a0), add(a1, a2)), safeSqrt(safeSqrt(a2)))))"
    expr2 = expr.from_string(sol, pset)
    nodes, edges, labels = gp.graph(expr2)

    ### Graphviz Section ###
    import pygraphviz as pgv

    g = pgv.AGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="dot")

    for i in nodes:
        n = g.get_node(i)
        n.attr["label"] = labels[i]
        
    g.draw("tree.png")

def plot_metric_vs_euclidean():
    expr = toolbox.individual()
    sol = "safeDiv(safeSqrt(add(safeSqrt(safeSqrt(input2)), input0)), add(add(safeSqrt(safeSqrt(input0)), add(safeSqrt(input0), add(input1, input2))), add(add(safeSqrt(input0), add(input1, input2)), safeSqrt(safeSqrt(input2)))))"
    individual = expr.from_string(sol, pset)
    func = toolbox.compile(expr=individual)
    result, l_metric, l_euclidean = correlation_gp.correlation(func)
    print(len(l_metric))
    print(len(l_euclidean))
    print(l_metric[0])
    plt.scatter(l_metric[2], l_euclidean[2])
    plt.xlabel("Dissimilarity metric")
    plt.ylabel("Euclidean distance [m]")
    plt.grid(True)
    print("result", result)
        
if __name__ == "__main__":
    genetic()
    #plot_metric_vs_euclidean()
        
    
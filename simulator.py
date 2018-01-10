# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:49:48 2017

@author: DaniG
"""

import read_scenario_tcl
import math
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

import operator

from deap import base
from deap import creator
from deap import tools
from deap import gp

#depth = 4

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

pset = gp.PrimitiveSet("MAIN", 3,"input")
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

class Neighbor(object):
    """It defines a neighbor node"""
    def __init__(self,id, d):
        self.id = id
        self.distance = d
        self.jaccard = 0.0
        self.dice = 0.0
        self.kulczynski = 0.0
        self.folkes = 0.0
        self.sokal = 0.0
        self.bnr = 0.0

class Node(object):
    """ It defines a node, constructor receives the x,y coordinates"""
    def __init__(self, id, x, y):
        self.id = id
        self.node_x = x
        self.node_y = y
        self.neighbors = list()
        self.neighbors_id = list()
        self.received_messages = list() # we store the ID of messages
        self.sent_messages = list() # we store the ID of messages
        self.redundant_messages = int()
        self.r = 250
    def check_redundant(self, m_id):
        for m in self.received_messages:
            if m_id == m:
                return True # repeated message
        return False

class Message(object):
    """ Broadcasting message"""
    def __init__(self, id):
        self.id = id
        self.source = int()
        self.transmitters = list()
        self.redudant = int()
        self.hops = int() # number of hops
        
def jaccard(l1, l2):
    """ It calculates the Jaccard distance between two lists"""
    l1 = set(l1)
    l2 = set(l2)
    a1 = l1.intersection(l2)
    a2 = l1.difference(l2)
    a3 = l2.difference(l1)
    jaccard = float(len(a1)) /float(len(a1) + len(a2) + len(a3))
    jaccard = 1 - jaccard
    return jaccard

def dice(l1, l2):
    """ It calculates the Dice distance between two lists """
    l1 = set(l1)
    l2 = set(l2)
    a1 = l1.intersection(l2)
    a2 = l1.difference(l2)
    a3 = l2.difference(l1)
    dice = (2* float(len(a1))) /((2*float(len(a1))) + len(a2) + len(a3))
    dice = 1 - dice
    return dice

def kulczynski(l1, l2):
    """ It calculates the Kulczynski distance between two lists"""
    kulczynski = 0.0
    l1 = set(l1)
    l2 = set(l2)
    a1 = l1.intersection(l2)
    a2 = l1.difference(l2)
    a3 = l2.difference(l1)
    a1 = len(a1)
    a2 = len(a2)
    a3 = len(a3)

    if((a1 + a2) != 0) and ((a1 + a3) != 0):
        kulczynski1 = float(a1) / (float(a1) + float(a2))
        kulczynski2 = float(a1) / (float(a1) + float(a3))
        kulczynski = 0.5 * (kulczynski1 + kulczynski2)
        kulczynski = 1 - kulczynski
    else:
        kulczynski = 0.0

    return kulczynski

def folkes(l1,l2):
    """ It calculates the folkes distance between two lists"""
    l1 = set(l1)
    l2 = set(l2)
    a1 = l1.intersection(l2)
    a2 = l1.difference(l2)
    a3 = l2.difference(l1)
    a1 = len(a1)
    a2 = len(a2)
    a3 = len(a3)
    if ((a1 + a2) != 0) and ((a1 + a3) != 0):
        folkes = float(a1) / math.sqrt((a1 + a2) * (a1 + a3))
        folkes = 1 - folkes
    else:
        folkes = 0.0
    return folkes    


def sokal(l1,l2):
    """ It calculates the sokal distance between two lists """
    l1 = set(l1)
    l2 = set(l2)
    a1 = l1.intersection(l2)
    a2 = l1.difference(l2)
    a3 = l2.difference(l1)
    a1 = len(a1)
    a2 = len(a2)
    a3 = len(a3)
    sokal = float(a1) /float(a1 + 2*(a2 + a3))
    sokal = 1 - sokal
    return sokal

def bnr(l1,l2):
    """ It calculates the bnr metric between two lists"""
    l1 = set(l1)
    l2 = set(l2)
    a1 = l1.intersection(l2)
    a2 = l1.difference(l2)
    a3 = l2.difference(l1)
    a1 = len(a1)
    a2 = len(a2)
    a3 = len(a3)
    #print (a3 + a2)
    #print (a3)
    bnr = float(a3) / float(a3 + a2)
    #print bnr
    return bnr

def new_metric(l1,l2):
    """ It calculates the new distance"""
    expr = toolbox.individual()
    sol = "safeDiv(safeSqrt(add(safeSqrt(safeSqrt(input2)), input0)), add(add(safeSqrt(safeSqrt(input0)), add(safeSqrt(input0), add(input1, input2))), add(add(safeSqrt(input0), add(input1, input2)), safeSqrt(safeSqrt(input2)))))"
    individual = expr.from_string(sol, pset)
    func = toolbox.compile(expr=individual)
    inputs = [None] * 3
    l1 = set(l1)
    l2 = set(l2)
    inputs[0] = len(l1.intersection(l2))
    inputs[1] = len(l1.difference(l2))
    inputs[2] = len(l2.difference(l1))
    metric = func(*inputs)
    metric = 1 - metric
    return metric

def plot_transmitters(source, trans, list_nodes):
    """ Plots the nodes that retransmit the messages"""
    x_list = list()
    y_list = list()
    for i in trans:
        for j in list_nodes:
            if i == j.id:
                x_list.append(j.node_x)
                y_list.append(j.node_y)
    
    x_source = list_nodes[source].node_x
    y_source = list_nodes[source].node_y
    
    plt.figure(figsize= (5,5))
    #plt.subplot(221)
    plt.scatter(x_list, y_list)
    plt.scatter(x_source,y_source, color = 'r')
    plt.xlim([0, 2000])
    plt.ylim([0, 2000])
    plt.xlabel("Nodes")
    plt.grid(True)


def scenario(tcl, n_nodes, list_nodes):
    """ create the scenario from the tcl"""
    nodes_positions= read_scenario_tcl.read_tcl_function(tcl, n_nodes, 1)
    nodes_x = nodes_positions[0]
    nodes_y = nodes_positions[1]

    for k in range(0,n_nodes):
        x_cor = nodes_x[k][0]
        y_cor = nodes_y[k][0]
        list_nodes.append(Node(k,x_cor,y_cor)) # create a node

    # Calculate the relative Euclidean distance between nodes
    for node in list_nodes:
        for nb in list_nodes:
            if(node.id != nb.id):
                x = (node.node_x - nb.node_x) * (node.node_x - nb.node_x)
                y = (node.node_y - nb.node_y) * (node.node_y - nb.node_y)
                distance = math.sqrt(x + y)
                if distance <= 250:
                    node.neighbors.append(Neighbor(nb.id, distance))
                    node.neighbors_id.append(nb.id)

source_id = 0
def sources_selection(list_nodes, n_sources, list_messages, list_event):
    """ Selection of source nodes that start the broadcasting procedure"""
    global source_id
    for s in range(0, n_sources):
        source = random.randint(0, len(list_nodes)-1)
        message = Message(source_id)
        message.transmitters.append(source)
        message.source = source
        list_messages.append(message)
        source_id = source_id + 1
        list_event.append(("s", source, message.id)) # add a new event in the list

def calc_distance(receiver, sender, list_nodes):
    x_receiver = list_nodes[receiver].node_x
    y_receiver = list_nodes[receiver].node_y
    x_sender = list_nodes[sender].node_x
    y_sender = list_nodes[sender].node_y
    distance = math.sqrt((x_receiver-x_sender)*(x_receiver-x_sender) + (y_receiver-y_sender)*(y_receiver-y_sender))
    return distance

def calc_dissimilarity(receiver, sender, list_nodes, type_metric):
    l_receiver = list_nodes[receiver].neighbors_id
    l_sender = list_nodes[sender].neighbors_id
    if (type_metric == "Jaccard"):
        dissimilarity = jaccard(l_receiver, l_sender)
    if (type_metric == "Dice"):
        dissimilarity = dice(l_receiver, l_sender)
    if (type_metric == "Sokal"):
        dissimilarity = sokal(l_receiver, l_sender)
    if (type_metric == "Kulcyznski"):
        dissimilarity = kulczynski(l_receiver, l_sender)
    if (type_metric == "Folkes"):
        dissimilarity = folkes(l_receiver, l_sender)
    if (type_metric == "New"):
        dissimilarity = new_metric(l_receiver, l_sender)
    return dissimilarity        
    
def calc_probability(receiver, sender, list_nodes, algorithm, metric):
    """ This function calculates the forwarding probability depending on the algorithm"""
    
    if (algorithm == "dpersistence"):
        dissimilarity = calc_dissimilarity(receiver, sender, list_nodes, metric)
        probability = dissimilarity * 10
        rand = random.randint(0, 10)
        if rand < probability:
            return True
        else:
            return False        
        
    if (algorithm == "epersistence"):
        distance = calc_distance(receiver, sender, list_nodes)
        probability = (float(distance) / 250) * 10
        rand = random.randint(0, 10)
        if rand < probability:
            return True
        else:
            return False
        
    if (algorithm == "gossip"):
        rand = random.randint(0, 10)
        probability = 10
        if rand < probability:
            return True
        else:
            return False
    if (algorithm == "flooding"):
        return True

#def send_message(event, t_file, list_nodes, list_event):
def send_message(event, list_nodes, list_event):    
    """
    function that sends a message and creates an event for receiving a message
    trace file: "event+sender+message" 
    event: "event+receiver+sender+message"
    """
    ev = str(event[0]) + " " + str(event[1]) + " " + str(event[2]) + "\n"
    #t_file.write(ev) # add line in trace_file
    try:
        node = list_nodes[event[1]] # node that sends the message
        node.sent_messages.append(event[2]) # add the message sent
        for nb in node.neighbors: 
            list_event.append(("r",nb.id ,node.id, event[2]))
    except:
        print event[1]
        
#def received_message(event, t_file, list_nodes, list_event, algorithm, metric):
def received_message(event, list_nodes, list_event, algorithm, metric):    
    """
    function that receives a message and creates an event for sending a message
    trace file: "event+receiver+sender+message" 
    event: "event+sender+message"
    """
    
    #ev = str(event[0]) + " " +  str(event[1]) + " " + str(event[2]) + " " + str(event[3]) + "\n"
    #t_file.write(ev) # add line in trace_file
    node = list_nodes[event[1]] # node that sends the message
    if node.check_redundant(event[3]) == False:
        node.received_messages.append(event[3]) # add the message sent
        if calc_probability(event[1], event[2], list_nodes, algorithm, metric) == True:
            list_event.append(("s", node.id, event[3]))
    else:
        node.redundant_messages = node.redundant_messages + 1

#def scheduler(list_event, t_file, list_nodes, algorithm, metric):
def scheduler(list_event, list_nodes, algorithm, metric):    
    while len(list_event) >0:
        event= list_event[0]
        if event[0] == "s":
            #send_message(event, t_file, list_nodes, list_event)
            send_message(event, list_nodes, list_event)
            del(list_event[0])
        else:
            #received_message(event, t_file, list_nodes, list_event, algorithm, metric)
            received_message(event, list_nodes, list_event, algorithm, metric)
            del(list_event[0])
    
#def calc_received(list_nodes, trace_file, n_sources):
def calc_received(list_nodes, n_sources):    
    total_redundant = 0
    for i in list_nodes:
        total_redundant = total_redundant + i.redundant_messages
    
    total_redundant = total_redundant / float(n_sources)
    return total_redundant    
    #trace_file.write("Rd " + str(total_redundant) + "\n")
    
#def calc_reachability(list_nodes, trace_file, sources):
def calc_reachability(list_nodes, sources):    
    total_received = 0
    for i in list_nodes:
        total_received = total_received + len(i.received_messages)
    
    reach = total_received / float(sources*len(list_nodes))
    #trace_file.write("Re " + str(reach)+ "\n")
    return reach
    
def main():
    dict_results_mean = {"Euclidean":list(),"Flooding":list(), "Kulcyznski": list(), "Jaccard":list(), "Folkes":list(), "Dice":list(), "New":list(), "Sokal":list()}
    dict_results_std = {"Euclidean":list(),"Flooding":list(), "Kulcyznski": list(), "Jaccard":list(), "Folkes":list(), "Dice":list(), "New":list(), "Sokal":list()}
    datos = pd.read_excel('simulation_broadcast2.xlsx', 'Hoja1', index_col=None, na_values=['NA'])
    for i, row in datos.iterrows():
        algorithm = str(row['algorithm']) # k level
        metric = str(row['metric']) # type of algorithm
        t_scenario = str(row['scenario']) # name of the file to write results
        nodes = int(row['nodes']) # crossover layout
        results = str(row['results']) #
        n_sources = int(row['sources'])
        trials = int(row['trials'])
        re = list()
        
        for i in range(trials-1):
            global source_id
            source_id = 0
            random.seed(i)
            list_event= list() # list of events in the network
            #trace_file = open(results+metric+str(i)+".txt", 'w')    
            list_nodes = list() # list of nodes in the network
            list_messages = list() # list of messages to transmit from the source

            #list_scenarios = ["Seville_2x2_100_1.tcl", "Seville_2x2_110_1.tcl", "Seville_2x2_120_1.tcl", "Seville_2x2_130_1.tcl", "Seville_2x2_140_1.tcl","Seville_2x2_150_1.tcl", "Seville_2x2_160_1.tcl", "Seville_2x2_170_1.tcl", "Seville_2x2_180_1.tcl", "Seville_2x2_190_1.tcl", "Seville_2x2_200_1.tcl"]
            #list_num_nodos = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

            scenario(t_scenario, nodes, list_nodes)
            list_nodes.sort(key=lambda x: x.id)

            #random.seed(6)
            sources_selection(list_nodes, n_sources, list_messages, list_event)
            scheduler(list_event, list_nodes, algorithm, metric)
        
            calc_received(list_nodes, n_sources)
            re.append(calc_reachability(list_nodes, n_sources))
           # trace_file.close()
            
        dict_results_mean[metric].append(np.mean(re))
        dict_results_std[metric].append(np.std(re))
        #datos_media = pd.DataFrame.from_dict(dict_results_mean)
        #datos_media.to_csv("resultados_media")
        #datos_desviacion = pd.DataFrame.from_dict(dict_results_std)
        #datos_desviacion.to_csv("resultados_desviacion")
        
    return dict_results_mean, dict_results_std
    
results_mean, results_std = main()

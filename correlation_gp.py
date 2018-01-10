#!/usr/bin/python

import math
import genetic_metric
import read_scenario_tcl
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import numpy as np

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
        self.r = 250

def find_node(list_nodes, id):
    """ It finds a given node in a list"""
    for nb in list_nodes:
        if nb.id == id:
            return nb

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
    bnr = float(a3) / float(a3 + a2)
    return bnr

def new_metric(l1,l2,func):
    """ It calculates the new distance"""
    inputs = [None] * 3
    l1 = set(l1)
    l2 = set(l2)
    inputs[0] = len(l1.intersection(l2))
    inputs[1] = len(l1.difference(l2))
    inputs[2] = len(l2.difference(l1))
    metric = func(*inputs)
    #print metric    
    if metric >= 1:
        metric = -1
        return metric
    if metric <= 0:
        metric = -1
        return metric
    """    
    # symmetric condition
    inputs[0] = len(l1.intersection(l2))
    inputs[1] = len(l1.difference(l1))
    inputs[2] = len(l2.difference(l2))
    metric2 = func(*inputs)
    if metric == metric2:
        return metric
    else:
        return -1
    """        
    return metric
    
def create_scenario(list_nodes, n_nodes, nodes_x, nodes_y):
    for k in range(n_nodes):
        x_cor = nodes_x[k][0]
        y_cor = nodes_y[k][0]
        list_nodes.append(Node(k,x_cor,y_cor))
        
def topology(list_nodes, list_distance):
    for node in list_nodes:
        for nb in list_nodes:
            if(node.id != nb.id):
                x = (node.node_x - nb.node_x) * (node.node_x - nb.node_x)
                y = (node.node_y - nb.node_y) * (node.node_y - nb.node_y)
                distance = math.sqrt(x + y)
                #print distance
                # to check if both nodes are neighbors
                if distance <= 250:
                    # create a neighbor node
                    node.neighbors.append(Neighbor(nb.id, distance))
                    node.neighbors_id.append(nb.id)

def calc_dissimilarity(list_nodes, list_jaccard, list_dice, list_kulczynski, list_sokal, list_folkes, list_distance):                
		# Calculate the dissimilarity metrics
    for node in list_nodes:
        for nb in node.neighbors:
            current_nb = find_node(list_nodes,nb.id) # we get the nodes
            # we calculate the dissimilarity distances
            nb.jaccard = jaccard(node.neighbors_id, current_nb.neighbors_id)
            nb.dice = dice(node.neighbors_id, current_nb.neighbors_id)
            nb.kulczynski = kulczynski(node.neighbors_id, current_nb.neighbors_id)
            nb.folkes = folkes(node.neighbors_id, current_nb.neighbors_id)
            nb.sokal = sokal(node.neighbors_id, current_nb.neighbors_id)
                        # we add the metrics in the lists of results						
            list_jaccard.append(nb.jaccard)
            list_dice.append(nb.dice)
            list_kulczynski.append(nb.kulczynski)
            list_folkes.append(nb.folkes)
            list_sokal.append(nb.sokal)
            list_distance.append(nb.distance)
                #list_metric.append(nb.metric)

def calc_dissimilarity_metric(list_nodes, list_metric, func):
    res = 1
    for node in list_nodes:
        for nb in node.neighbors:
            current_nb = find_node(list_nodes,nb.id)
            nb.metric = new_metric(node.neighbors_id, current_nb.neighbors_id, func)
            if nb.metric < 0:
                return -1
            else:
                list_metric.append(nb.metric)
    return res
            
def calc_correlation(list_correlation_jaccard, list_correlation_dice, list_correlation_folkes, list_correlation_kulczynski, list_correlation_sokal):
    media_jaccard = mean_tuple_list(list_correlation_jaccard)
    print "Correlacion media Jaccard %f" % media_jaccard
    media_dice = mean_tuple_list(list_correlation_dice)
    print "Correlacion media Dice %f" % media_dice
    media_folkes = mean_tuple_list(list_correlation_folkes)
    print "Correlation media Folkes %f" % media_folkes
    media_kulczynski = mean_tuple_list(list_correlation_kulczynski)
    print "Correlation media Kylczynski %f" % media_kulczynski
    media_sokal = mean_tuple_list(list_correlation_sokal)
    print "Correlation media Sokal %f" % media_sokal

def calc_correlation_metric(list_correlation_metric):
    media_metric = mean_tuple_list(list_correlation_metric)
    print "Correlation media New Metric %f" % media_metric
    result = media_metric
    #result = 1
    return result
    
def mean_tuple_list(mylist):
    cor = list()
    for i in mylist:
        if math.isnan(i[0]) == False:
            cor.append(float(i[0])) 
    res = np.mean(cor)
    return res

def correlation():
    # list of scenarios that we use for the correlation
    list_scenarios = ["Seville_2x2_100_1.tcl", "Seville_2x2_110_1.tcl", "Seville_2x2_120_1.tcl", "Seville_2x2_130_1.tcl", "Seville_2x2_140_1.tcl","Seville_2x2_150_1.tcl", "Seville_2x2_160_1.tcl", "Seville_2x2_170_1.tcl", "Seville_2x2_180_1.tcl", "Seville_2x2_190_1.tcl", "Seville_2x2_200_1.tcl"]
    list_num_nodos = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    # the list of correlations between the dissimilarity metric and the Euclidean distance for all scenarios
    list_correlation_jaccard = list()
    list_correlation_dice = list()
    list_correlation_kulczynski = list()
    list_correlation_folkes = list()
    list_correlation_sokal = list()
    list_correlation_metric = list()
    l_plot_metric = list()
    l_plot_euclidean = list()
    for i, j in zip(list_scenarios, list_num_nodos):
        # the following lists will contain the results
        list_nodes = list()
        list_jaccard = list()
        list_distance = list() # list of Euclidean distances
        list_dice = list()
        list_kulczynski = list()
        list_folkes = list()
        list_sokal = list()
        #list_bnr = list()
        list_metric = list()
        # we get the positions from the tcl
        nodes_positions= read_scenario_tcl.read_tcl_function(i, j, 1)
        nodes_x = nodes_positions[0]
        nodes_y = nodes_positions[1]
        n_nodes = j
        create_scenario(list_nodes, n_nodes, nodes_x, nodes_y) # create nodes
        topology(list_nodes, list_distance) # create topology of nodes      
        calc_dissimilarity(list_nodes, list_jaccard, list_dice, list_kulczynski, list_sokal, list_folkes, list_distance)
        #res_metric = calc_dissimilarity_metric(list_nodes, list_metric, func)
        #if res_metric < 0:
            #print "INVALID INDIVIDUAL"
        #    return -1
        # CALCULATE CORRELATION BETWEEN DISSIMILARITY DISTANCES AND EUCLIDEAN DISTANCE
        list_correlation_jaccard.append(pearsonr(list_distance, list_jaccard))
        list_correlation_dice.append(pearsonr(list_distance, list_dice))
        list_correlation_folkes.append(pearsonr(list_distance, list_folkes))
        list_correlation_kulczynski.append(pearsonr(list_distance, list_kulczynski))
        list_correlation_sokal.append(pearsonr(list_distance, list_sokal))
        #list_correlation_metric.append(pearsonr(list_distance, list_metric))
        #l_plot_euclidean.extend(list_distance)
        #l_plot_metric.extend(list_metric)
        l_plot_euclidean.append(list_distance)
        l_plot_metric.append(list_metric)
    # CALCULATE TOTAL CORRELATION FOR ALL THE SCENARIOS
    calc_correlation(list_correlation_jaccard, list_correlation_dice, list_correlation_folkes, list_correlation_kulczynski, list_correlation_sokal)
    #res = abs(calc_correlation_metric(list_correlation_metric))
    return l_plot_metric, l_plot_euclidean
    
if __name__ == "__main__":
    correlation()


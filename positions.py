# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:15:51 2017

@author: DaniG
"""

import read_scenario_tcl
import matplotlib.pyplot as plt

# script for plotting the nodes positions

class Node(object):
    """ It defines a node, constructor receives the x,y coordinates"""
    def __init__(self, id, x, y):
        self.id = id
        self.node_x = x
        self.node_y = y
        self.neighbors = list()
        self.neighbors_id = list()
        self.r = 250


list_scenarios = ["Seville_2x2_100_1.tcl", "Seville_2x2_110_1.tcl", "Seville_2x2_120_1.tcl", "Seville_2x2_130_1.tcl", "Seville_2x2_140_1.tcl","Seville_2x2_150_1.tcl", "Seville_2x2_160_1.tcl", "Seville_2x2_170_1.tcl", "Seville_2x2_180_1.tcl", "Seville_2x2_190_1.tcl", "Seville_2x2_200_1.tcl"]
list_num_nodos = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

nodes_positions= read_scenario_tcl.read_tcl_function(list_scenarios[0], list_num_nodos[0], 1)
nodes_x = nodes_positions[0]
nodes_y = nodes_positions[1]

nodes_positions2= read_scenario_tcl.read_tcl_function(list_scenarios[3], list_num_nodos[3], 1)
nodes_x2 = nodes_positions2[0]
nodes_y2 = nodes_positions2[1]

nodes_positions3= read_scenario_tcl.read_tcl_function(list_scenarios[7], list_num_nodos[7], 1)
nodes_x3 = nodes_positions3[0]
nodes_y3 = nodes_positions3[1]

nodes_positions4= read_scenario_tcl.read_tcl_function(list_scenarios[9], list_num_nodos[9], 1)
nodes_x4 = nodes_positions4[0]
nodes_y4 = nodes_positions4[1]


list_nodes = list()

"""
for k in range(0, list_num_nodos[0]):
    x_cor = nodes_x[k][0]
    #print x_cor
    y_cor = nodes_y[k][0]
    #print y_cor 
    list_nodes.append(Node(k,x_cor,y_cor))
"""

ax= plt.figure(figsize= (10,10))
plt.subplot(221)
plt.scatter(nodes_x, nodes_y)
plt.xlim([0, 2000])
plt.ylim([0, 2000])
plt.xlabel("a) 100 nodes")
plt.grid(True)

plt.subplot(222)
plt.scatter(nodes_x2, nodes_y2, color = 'r')
plt.xlim([0, 2000])
plt.ylim([0, 2000])
plt.xlabel("b) 130 nodes")
plt.grid(True)

plt.subplot(223)
plt.scatter(nodes_x3, nodes_y3, color = 'c')
plt.xlim([0, 2000])
plt.ylim([0, 2000])
plt.xlabel("c) 170 nodes")
plt.grid(True)

plt.subplot(224)
plt.scatter(nodes_x4, nodes_y4, color = 'k')
plt.xlim([0, 2000])
plt.ylim([0, 2000])
plt.xlabel("d) 200 nodes")
plt.grid(True)


         

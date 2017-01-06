from gurobipy import *
import networkx as nx
from networkx.generators.random_graphs import *
from networkx.algorithms.bipartite.generators import *
nodes=50

#Create a random graph
#G = erdos_renyi_graph(nodes, 0.5, seed=None, directed=False)
G = complete_bipartite_graph(nodes/2, nodes/2, create_using=None)
print G.edges()

#Max cut Integer Program

m = Model("maxcut")

#Create Variables
node_var=[]
edge_var={}

for i in range(nodes):
    node_var.append(m.addVar(vtype=GRB.BINARY, name='v'+str(i)))

for edge in G.edges_iter():
    edge_var[(edge[0],edge[1])]=m.addVar(vtype=GRB.BINARY)


#Constraints: z
#1.z_e <= x_u + x_v
#2.z_e <= 2 - (x_u + x_v)

for edge in G.edges_iter():
    m.addConstr(edge_var[edge], GRB.LESS_EQUAL, node_var[edge[0]]+node_var[edge[1]]     )
    m.addConstr(edge_var[edge], GRB.LESS_EQUAL, 2-(node_var[edge[0]]+node_var[edge[1]]) )

#Objective: Max Sigma_{e in E} z_e
obj=QuadExpr()

#Iterate through edges to build objective function
for edge in G.edges_iter():
    obj += edge_var[(edge[0],edge[1])]

m.setObjective(obj, GRB.MAXIMIZE)

#Solve
m.optimize()


#Write to file 
m.write('opt.sol')




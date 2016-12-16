from gurobipy import *
import networkx
from networkx.generators.random_graphs import *

nodes=4

#Create a random graph
#G = erdos_reyni_graph(nodes, 0.5, seed=None, directed=False)
G=[[0 for x in range(nodes)]for y in range(nodes)]
G[0][1]=1
G[0][2]=1
G[0][3]=1
G[1][0]=1
G[1][3]=1
G[2][0]=1
G[2][3]=1
G[3][0]=1
G[3][1]=1
G[3][2]=1


#Max cut Integer Program

m = Model("maxcut")

#Create Variables
var=[]

for i in range(nodes):
    var.append(m.addVar(vtype=GRB.INTEGER,lb=-1.0, ub=1.0))

#Constraints: x_i , x_j = {-1, 1} for all i, j in [n]
#for i in range(nodes):
#    m.addConstr(var[i], GRB.GREATER_EQUAL, 0.5)
#    m.addConstr(var[i], GRB.LESS_EQUAL, -0.5)

#Objective: Max_x (1/4)( Sum^n_1 Sum^n_1 w_{i,j}(1 - x_i*x_j))
obj=QuadExpr()
for i in range(nodes):
    for j in range(nodes):
        #if edge exists
        if G[i][j]:
            obj += (1-var[i]*var[j])

obj = obj/4

m.setObjective(obj, GRB.MAXIMIZE)

#Solve
m.optimize()

#Write to file 
m.write('maxcut.ip')





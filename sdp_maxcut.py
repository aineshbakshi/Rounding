import cvxopt as cvx
import cvxopt.lapack
import numpy as np

import picos as pic
import networkx as nx
from networkx.generators.random_graphs import *

nodes = 10

#Create a random graph
G = erdos_renyi_graph(nodes, 0.5, seed=None, directed=False)

#Max Cut SDP

maxcut= pic.Problem()

#Matrix X of variables

X = maxcut.add_variable('X',(nodes,nodes), 'symmetric')

#Laplacian of the Graph G
LL = 1/4.*nx.laplacian_matrix(G).todense()
L = pic.new_param('L', LL)

#Constraints

#v_{i,i} = 1
maxcut.add_constraint(pic.tools.diag_vect(X)==1)

#X is PSD
maxcut.add_constraint(X>>0)

#Objective function: max 1/4 <L, X>
maxcut.set_objective('max', L|X)

print maxcut

maxcut.solve(verbose=0)

#Random Projection Algorithm

V = X.value

cvxopt.lapack.potrf(V)

for i in range(nodes):
    for j in range(i+1,nodes):
        V[i,j]=0

count = 0
obj_sdp = maxcut.obj_value()
obj = 0

while ( count < 100 or obj < 0.878*obj_sdp ):
    r = cvx.normal(nodes, 1)
    x = cvx.matrix(np.sign(V*r))
    o = (x.T*L*x).value[0]
    if o > obj:
        x_cut = x
        obj = o
    count +=1

print 'Value of cut: ', obj
S1=[n for n in range(nodes) if x[n]<0]
S2=[n for n in range(nodes) if x[n]>0]
cut = [(i,j) for (i,j) in G.edges() if x[i]*x[j]<0]

print "S1: ", S1
print "S2: ", S2

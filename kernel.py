from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.datasets import dump_svmlight_file
import numpy as np

import math
import sdp_maxcut
import ip_maxcut

nodes = 60
prob = 0.1
alpha = 0.6

def fit_svm(X, y):
    clf = svm.SVC()
    clf.fit(X, y)
    return clf

if __name__ == '__main__':
    
    #Call IP
    G = ip_maxcut.create_graph(nodes, prob)
    y = ip_maxcut.maxcut_ip(G, nodes)
    y = np.asarray(y)

    #Call SDP
    maxcut, X, L = sdp_maxcut.maxcut_sdp(G, nodes)
    X = X.value

    t = int(math.floor(alpha*nodes))
    #Divide into train and test set
    y_train = y[: t]
    y_test = y[t :]

    X_train = X[: t, :]
    X_test = X[t:, :]

    #fit svm
    clf = fit_svm(X_train, y_train)
    y_pred = clf.predict(X_test)

    f = open('g1_data.dump', 'wb')
    dump_svmlight_file(X, y, f, zero_based=True, comment=None, query_id=None, multilabel=False)

    
    print 'y_true: ', y_test
    print 'y_pred: ', y_pred
    #accuracy score 
    print 'accuracy score: ', accuracy_score(y_test, y_pred)


    

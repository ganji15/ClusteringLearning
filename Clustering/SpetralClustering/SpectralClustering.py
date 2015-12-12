'''
Author: GanJi
No.201518008629004

Spectral Clustering
'''

import numpy as np
import matplotlib.pyplot as plt
import os

location = os.path.split(os.path.realpath(__file__))[0] + '\\'
data_name = 'spectrum_data.txt'
fig_name = 'SpectralClustering.png'

calc_dist = lambda x, y: sum(i * i for i in (x - y))
norm_vec = lambda x : x / np.sqrt(sum(i * i for i in x))

def nearest_neigbor(neigbors, point):
    m = len(neigbors)
    min_index = 0    
    min_dist = calc_dist(neigbors[0], point)

    for i in range(1, m):
        dist = calc_dist(neigbors[i], point)
        if min_dist > dist:
            min_index = i
            min_dist = dist

    return min_index

def k_means(data, k):
    iter_times_limit = 4
    
    means = []
    groups = []

    m = len(data)

    for i in range(0, k):
        means.append(data[i * m / k + m / k / 2.5])
        groups.append(list([]))

    for iter_time in range(0, iter_times_limit): 
        print '\n'
        for i in range(0, k):
            groups[i] = []

        for i in range(0, m):
            groups[ nearest_neigbor(means, data[i])].append( i)
        
        for i in range(0, k):
            print len(groups[i])
            means[i] = sum(data[j] for j in groups[i]) * 1.0 / len(groups[i])            
    
    return groups

def k_nearest_neigbor_weights(data, point, k_edge, varance = 10):
    dist_index = []
    dists = []
    m = len(data)
 
    for i in range(0, m):
        dists.append(calc_dist(data[i], point))
    dist_index =  np.argsort(dists)[1 : k_edge + 1]
    weights = [np.exp(- dists[i] * 1.0 / (2 * varance * varance)) for i in dist_index]
    
    return dist_index, weights

def calc_Lsym(data, k_edge = 10, varance = 10):
    m = len(data)
    W = np.zeros((m, m), dtype = 'float')
    for i in range(0, m):
        index, weights =  k_nearest_neigbor_weights(data, data[i], k_edge, varance)
        for j in range(0, len(index)):
            W[i, index[j]] = weights[j]

    D = np.zeros((m, m), dtype = 'float')
    for i in range(0, m):
        D[i, i] = sum(W[i])

    D = np.mat(D)
    W = np.mat(W)
    L = D - W
    D_inv_sqrt = np.zeros((m, m), dtype = 'float')
    for i in range(0, m):
        D_inv_sqrt[i, i] = 1.0 / np.sqrt(D[i, i])
    D_inv_sqrt = np.mat(D_inv_sqrt)
    Lsym = D_inv_sqrt * L * D_inv_sqrt
    
    return Lsym

def get_uniform_k_eig_mat(Lsym, k):
    eig_values, eig_vecs = np.linalg.eig(Lsym)
    eig_values = eig_values.real
    eig_vecs = eig_vecs.real

    counts = 0
    U = []
    T = []
    for i in np.argsort(eig_values):
        print eig_values[i]

    for i in np.argsort(eig_values):
        if (eig_values[i] > 0.0000001):
            T.append( norm_vec(eig_vecs[:, i]))
            counts = counts + 1
        if counts >= k:
            break

    T = np.array(np.hstack(T))
    return T             

def plot_regresstion(groups, data):
    m = len(groups)
    color_map = ['c', 'b', 'k', 'g', 'm', 'r']
    
    plt.figure()
    plt.title('Spectral Clustering')

    for i in range(0, m):
        group = np.vstack([data[j] for j in groups[i]]);
        plt.scatter(group[:, 0], group[:, 1], color = color_map[i], marker = '.')
       
    plt.savefig(location + fig_name)
    plt.show()

def spectrum_regression(data, k, k_edge = 10, varance = 10):
    t_data = get_uniform_k_eig_mat( calc_Lsym(data, k_edge, varance), k)
    groups = k_means(t_data, k)
    return groups
   
def run():
    if os.path.exists(location + data_name) == False:
        print 'CAN\'T find ' + location + data_name +',\nthe Data for spectral clustering is MISSING!\n'
        raw_input('press any key')
        return
    data = np.loadtxt(location + data_name, delimiter = ' ')
    groups = spectrum_regression(data, 2, 10, 10)
    plot_regresstion(groups, data)

run()

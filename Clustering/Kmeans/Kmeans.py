'''
Author: GanJi
No.201518008629004

K-means Clustering
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os

location = os.path.split(os.path.realpath(__file__))[0] + '\\'
mat_name = 'mvn_data.mat'
origin_data_fig = 'mvn_origin_data.png'
k_means_fig = 'k-mean.png'

calc_dist = lambda x,y : sum(i * i for i in (x - y))

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

def mean_square_error(means, data):
    error = 0
    m = len(means)
    true_means = []

def plot_regresstion(means, groups, data):
    m = len(means)
    color_map = ['c', 'b', 'k', 'g', 'm', 'r']
    
    plt.figure()
    plt.title('K-means Clustering')

    for i in range(0, m):
        group = np.vstack([data[j] for j in groups[i]]);
        plt.scatter(group[:, 0], group[:, 1], color = color_map[i], marker = '.')
    
    #means = np.vstack(means)
    #plt.scatter(means[:, 0], means[:, 1], color = 'r', marker = '.')
    plt.savefig(location + k_means_fig)
    plt.show()

def generate_data():
    print 'Data Generating...'
    Sigma = [[1, 0], [0, 1]]
    mu1 = [1, -1]
    x1 = np.random.multivariate_normal(mu1, Sigma, 200)
    mu2 = [5.5, -4.5]
    x2 = np.random.multivariate_normal(mu2, Sigma, 200)
    mu3 = [1, 4]
    x3 = np.random.multivariate_normal(mu3, Sigma, 200)
    mu4 = [6, 4.5]
    x4 = np.random.multivariate_normal(mu4, Sigma, 200)
    mu5 = [9, 0.0]
    x5 = np.random.multivariate_normal(mu5, Sigma, 200)

    X = np.concatenate((x1, x2, x3, x4, x5))

    plt.figure()
    plt.title('mvn_data of K clusters')
    plt.scatter(x1[:, 0], x1[:, 1], color = 'r', marker ='.')
    plt.scatter(x2[:, 0], x2[:, 1], color = 'b', marker ='.')
    plt.scatter(x3[:, 0], x3[:, 1], color = 'k', marker ='.')
    plt.scatter(x4[:, 0], x4[:, 1], color = 'g', marker ='.')
    plt.scatter(x5[:, 0], x5[:, 1], color = 'm', marker ='.')
    plt.savefig(location + origin_data_fig)
    #plt.show()
    sio.savemat(location + mat_name, {'X': X})
    print 'Data Generated in' + location + mat_name
           
def k_means(data, k):
    iter_times_limit = 5
    
    means = []
    groups = []

    m = len(data)

    for i in range(0, k):
        means.append(data[i * m / k + np.random.randint(0, m / k)])
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
    
    return means, groups

def run():
    if os.path.exists(location + mat_name) == False:
        generate_data()
    mvn_data = sio.loadmat(location + mat_name)
    X = mvn_data['X']
    means, groups = k_means(X, 5)
    plot_regresstion(means, groups, X)

run()

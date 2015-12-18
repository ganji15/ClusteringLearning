import numpy as np
import matplotlib.pyplot as plt
import os
import Queue

location = os.path.split(os.path.realpath(__file__))[0] + '\\'
data_name = 'data.txt'
fig_name = 'dbscan.png'

calc_dist = lambda x, y : sum(i * i for i in (x - y))
is_core = lambda x, cnt, bound : sum(ele < bound for ele in x) >= cnt
is_neigbor = lambda x, y, dists, bound: dists[x, y] <= bound
enum = lambda **enums: type('enum', (), enums)

p_type = enum(outlier = 0, core = 1, reachable = 2) 

def calc_all_dists(data):
    m = len(data)

    dists = np.zeros((m, m), dtype = 'float')
    for i in range(0, m):
        for j in range(i, m):
            dists[i, j] = calc_dist(data[i], data[j])
            dists[j, i] = dists[i, j]
    
    return dists    

def get_point_type(dists, core_num, bound):
    m = len(dists)
    
    types = np.ones((m, 1)) * p_type.outlier

    for i in range(0, m):
        if is_core(dists[i], core_num, bound):
            types[i] = p_type.core

    cores = [index for index in range(0, m) if types[index] == p_type.core]
    for core in cores:
            reachs = [ele_index for ele_index in range(0, m)\
                                if dists[core, ele_index] < bound and\
                                types[ele_index] == p_type.outlier]
            for reach in reachs:
                types[reach] = p_type.reachable

    return types

def dbscan_gression_by_types(types, dists, bound):
    m = len(types)
    visit = np.zeros((m, 1))
    groups = []

    cores = [index for index in range(0, m) if types[index] == p_type.core]
    reachs = [index for index in range(0, m) if types[index] == p_type.reachable]

    que = Queue.Queue()
    while len(cores) > 0:
        que.queue.clear()
        que.put(cores[0])
        visit[cores[0]] = 1
        group = []
        while que.empty() == False:
            cur = que.get()
            group.append(cur)

            for reach in reachs:
                if visit[reach] == 0 and is_neigbor(cur, reach, dists, bound):
                    group.append(reach)
                    visit[reach] = 1

            for new_c in cores:
               if visit[new_c] == 0 and is_neigbor(cur, new_c, dists, bound):
                   que.put(new_c)
                   visit[new_c] = 1

        groups.append(group)
        reachs = list(set(reachs) - set(group))
        cores = list(set(cores) - set(group))
    
    outliers = [index for index in range(0, m) if visit[index] == 0]
    if len(outliers) > 0:
        groups.append(outliers)

    return groups

def plot_regresstion(groups, data):
    m = len(groups)
    color_map = ['c', 'b', 'g', 'm', 'r']
    
    plt.figure()
    plt.title('DBSCAN Clustering')

    for i in range(0, m - 1):
        group = np.vstack([data[j] for j in groups[i]])
        plt.scatter(group[:, 0], group[:, 1], color = color_map[i], marker = '.')

    group = np.vstack([data[j] for j in groups[m - 1]]);
    plt.scatter(group[:, 0], group[:, 1], color = 'k', marker = '.')
    
    plt.savefig(location + fig_name)
    plt.show()

def DBSCAN(data, core_num, bound):
    dists = calc_all_dists(data)
    types = get_point_type(dists, core_num, bound)
    return dbscan_gression_by_types(types, dists, bound)

def run():
    if os.path.exists(location + data_name) == False:
        print 'CAN\'T find ' + location + data_name +',\nthe Data for DBSCAN clustering is MISSING!\n'
        raw_input('press any key')
        return
    data = np.loadtxt(location + data_name, delimiter = ' ')
    groups = DBSCAN(data, 4, 0.05)
    plot_regresstion(groups, data)

run()

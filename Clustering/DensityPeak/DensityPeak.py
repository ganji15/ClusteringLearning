'''
Author: Ganji
Email: ganji15@mails.ucas.ac.cn

Clustering by fast search and find of density peaks
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os

location = os.path.split(os.path.realpath(__file__))[0] + '\\'
data_list = ['Spiral.txt', 'Aggregation.txt', 'Compound.txt', 'R15.txt']
fig_list = ['Spiral.png', 'Aggregation.png', 'Compound.png', 'R15.png']
tmp_fig_list = ['Spiral_densitypeak.png', 'Aggregation_densitypeak.png', 'Compound_densitypeak.png', 'R15_densitypeak.png']
params = [[9, 10, 15],\
          [9, 10, 15],\
          [8, 10, 15],\
          [0.1, 1, 10]]
#for param in params: param=>[bound, min_peakdist, min_density]

calc_dist = lambda x, y: ( sum(i * i for i in (x - y)))

def calc_dists(data):
    m = len(data)
    dists = np.zeros((m, m), dtype = 'float')

    for j in range(0, m):
        for i in range(0, j):
            dists[i, j] = calc_dist(data[i], data[j])
            dists[j, i] = dists[i, j]

    return dists

def calc_densities(dists, bound):
    m = len(dists)
    densities = np.zeros((m, 1))

    for i in range(0, m):
        densities[i] = sum([np.exp(-0.5 * dist/bound) for dist in dists[i] if dist < bound])
      
    return densities

def calc_peak_dists(dists, bound, densities):
    m = len(dists)
    peak_dists = np.zeros((m, 1), dtype = 'float')
	
    max_densities = max(densities)
    for i in range(0, m):
        if densities[i] != max_densities:
            peak_dists[i] = min([dists[i, j] for j in range(0, m) if densities[j] > densities[i]])
        else:
            peak_dists[i] = max([dists[i, j] for j in range(0, m)])
    
    return peak_dists

def get_clutering_points(densities, peak_dists, min_peakdist, min_density):
    m = len(densities)
    cores = [i for i in range(0, m) if peak_dists[i] >= min_peakdist and densities[i] >= min_density]   
    return cores

def label_data(densities, dists, cores):
    m = len(dists)

    labels = np.zeros((m, 1))
    for i in range(0, len(cores)):
        labels[ cores[i]] = i + 1
      
    sorted_by_densities = np.argsort(densities, axis = 0)[::-1]
    for i in range(0, m):
        if labels[ sorted_by_densities[i]] == 0:
            min_dist_j = 0
            for j in range(1, i):
                if dists[ sorted_by_densities[j], sorted_by_densities[i]] <=\
                    dists[ sorted_by_densities[min_dist_j], sorted_by_densities[i]]:
                    min_dist_j = j
            labels[ sorted_by_densities[i]] = labels[ sorted_by_densities[min_dist_j]]
    
    return labels, len(cores)

def DensityPeak(data, bound, min_peakdist, min_density):
    m = len(data)

    dists = calc_dists(data) 
    densities = calc_densities(dists, bound)
    peak_dists = calc_peak_dists(dists, bound, densities)
    cores = get_clutering_points(densities, peak_dists, min_peakdist, min_density)
    print 'number of clusters: ' + '%d'%len(cores)
    labels, num_of_clusters = label_data(densities, dists, cores)

    return labels, densities, peak_dists, cores

def plot_density_and_dist(data, origin_label, densities, peak_dists, tmp_fig):
    m = len(densities)
    
    color_map = ['g', 'm', 'r', 'y', 'c', 'b', 'k', '#FF00FF']
    plt.figure()
    plt.title('Densitiy and Dists')
    
    for i in range(0, m):
        plt.scatter(densities[i], peak_dists[i], color = color_map[int(origin_label[i]) % 8])

    plt.savefig(tmp_fig)
    plt.show()

def plot_regresstion(data, labels, result_fig,cores = []):
    m = len(data)
    color_map = ['g', 'm', 'r', 'y', 'c', 'b', 'k', '#FF00FF']
    
    plt.figure()
    plt.title('DensityPeak Clustering')

    for i in range(0, m):
        plt.scatter(data[i, 0], data[i, 1], color = color_map[int(labels[i]) % 8], marker = '.')
    
    for core in cores:
        plt.scatter(data[core, 0], data[core, 1], color = 'r', marker = '.')
       
    plt.savefig(result_fig)
    plt.show()

def example(data_name, param, result_fig, tmp_fig = ''):
    if os.path.exists(data_name) == False:
        print 'CAN\'T find ' + data_name +',\nthe Data for spectral clustering is MISSING!\n'
        raw_input('press any key')
        return
    print '====example begin: ' + data_name + '...===='
    data = np.loadtxt(data_name, delimiter = ',')
    origin_labels = data[:,2]
    data = data[:, 0 : 2]
    labels, densities, peak_dists, cores = DensityPeak(data, param[0], param[1], param[2])
    if tmp_fig.strip():    
        plot_density_and_dist(data, origin_labels, densities, peak_dists, tmp_fig)
    plot_regresstion(data, labels, result_fig)
    print 'save regression result into ' + result_fig
    print '====example end.====\n'

def run():
    for i in range(0, len(data_list)):
        #example(location + data_list[i], params[i], location + fig_list[i], location + tmp_fig_list[i])
        example(location + data_list[i], params[i], location + fig_list[i])
      
run()
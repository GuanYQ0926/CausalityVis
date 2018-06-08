import json
import numpy as np
import pandas as pd
from sklearn import manifold
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import DBSCAN


def mds_layout():
    seed = np.random.RandomState(seed=3)
    dataset = pd.read_csv('./data/matrixC.csv', sep=',', header=None)
    data = dataset.values
    dists = euclidean_distances(data, data)
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-12,
                       dissimilarity='precomputed', random_state=seed)
    pos = mds.fit_transform(dists)
    # phy_pos = pd.read_csv('./data/positionC.csv', sep=',', header=None)
    # delta = np.mean(pos, axis=0) - np.mean(phy_pos, axis=0)
    jsonfile = []
    for i, p in enumerate(pos):
        jsonfile.append(dict(id=i, x=p[0], y=p[1]))
    with open('./data/mds_layout.json', 'w') as f:
        json.dump(jsonfile, f)


def matrix_plot():
    causality = []
    dataset = pd.read_csv('../data/matrixC.csv', header=None)
    dataset = dataset.values
    length = len(dataset[0])
    matrix = [[] for _ in range(length)]
    for i, val in enumerate(dataset):
        for ii, v in enumerate(val):
            causality.append(dict(src=i, dst=ii, value=v))
            matrix[i].append(v)
    with open('../static/matrixC.json', 'w') as f:
        jsonfile = dict(length=length, causality=causality, matrix=matrix)
        json.dump(jsonfile, f)


def forcelayout():
    dataset = pd.read_csv('../data/matrixC.csv', header=None)
    dataset = dataset.values
    nodes = []
    edges = []
    length = len(dataset[0])
    values = [[] for _ in range(length)]
    max_val = -100.0
    min_val = 100.0
    for i in range(len(dataset[0])):
        nodes.append(dict(id=i, x=np.random.rand(), y=np.random.rand(),
                     color='#4682b4', size=1,
                     degree=length-1, label='N'+str(i+1)))
    edge_count = 0
    for i, val in enumerate(dataset):
        for ii, v in enumerate(val):
            edges.append(dict(id=edge_count, source=i, target=ii,
                              color='#eee'))
            values[i].append(v)
            edge_count += 1
            if v > max_val:
                max_val = v
            if v < min_val:
                min_val = v
    iter_num = 500
    gravity = 0.1
    speed = 0.1
    max_displace = 50
    # calculate position
    for iter in range(iter_num):
        dx = 0.0
        dy = 0.0
        for i, node_i in enumerate(nodes):
            for j, node_j in enumerate(nodes):
                if i == j:
                    continue
                x_dist = node_i['x'] - node_j['x']
                y_dist = node_i['y'] - node_j['y']
                dist = (x_dist**2 + y_dist**2)**0.5
                af_src = values[i][j]
                af_dst = values[j][i]
                if dist > 0:
                    rep_f = 2
                    dx += x_dist / dist * rep_f
                    dy += y_dist / dist * rep_f
                    attr_f = 1 + af_src + af_dst
                    dx -= x_dist / dist * attr_f
                    dy -= y_dist / dist * attr_f
            d = (node_i['x']**2+node_i['y']**2)**0.5
            gf = gravity * 1
            dx -= gf * node_i['x'] / d
            dy -= gf * node_i['y'] / d
            dx *= speed
            dy *= speed
            dist = (dx**2+dy**2)**0.5
            if dist > 0.0:
                limited_dist = min(max_displace*speed, dist)
                # limited_dist = 1
                print(max_displace*speed, dist)
                nodes[i]['x'] += dx / dist * limited_dist
                nodes[i]['y'] += dy / dist * limited_dist
    with open('../static/layout.json', 'w') as f:
        jsonfile = dict(nodes=nodes, edges=edges)
        json.dump(jsonfile, f)


def clustering():
    with open('../static/layout.json', 'r') as f:
        dataset = json.load(f)
    nodes = dataset['nodes']
    edges = dataset['edges']
    data = []
    for node in nodes:
        data.append([node['x'], node['y']])
    data = np.array(data)
    print(data)
    # dbscan, color clustering
    clusters = DBSCAN(eps=150, min_samples=3).fit_predict(data)
    print(clusters)
    colors = ['#E3BA22', '#E58429', '#BD2D28', '#D15A86', '#8E6C8A',
              '#6B99A1', '#42A5B3', '#0F8C79', '#6BBBA1', '#5C8100']
    for i, v in enumerate(clusters):
        if v != -1:
            nodes[i]['color'] = colors[v]
        else:
            nodes[i]['color'] = '#4682b4'
    with open('../static/layout.json', 'w') as f:
        jsonfile = dict(nodes=nodes, edges=edges)
        json.dump(jsonfile, f)


if __name__ == '__main__':
    # mds_layout()
    # matrix_plot()
    # forcelayout()
    clustering()

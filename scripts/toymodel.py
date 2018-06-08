import json
import itertools
import numpy as np
import skccm as ccm
from scipy.stats.stats import pearsonr
from skccm.utilities import train_test_split
import matplotlib.pyplot as plt


class ToyModel(object):

    def __init__(self):
        pass

    def generate_test_data(self, time=400):
        '''
        toy model:
        y1(1) = y2(1) = y3(1) = y4(1) = 0.4
        y1(t+1) = y1(t)[3.9-3.9y1(t)]
        y2(t+1) = y2(t)[3.6-0.4y1(t)-3.6y2(t)]
        y3(t+1) = y3(t)[3.6-0.4y2(t)-3.6y3(t)]
        y4(t+1) = y4(t)[3.8-0.35y3(t)-3.8y4(t)]
        '''
        y1s, y2s, y3s, y4s = [0.4], [0.4], [0.4], [0.4]
        for i in range(time-1):
            y1, y2, y3, y4 = y1s[i], y2s[i], y3s[i], y4s[i]
            y1s.append(y1*(3.9-3.9*y1))
            y2s.append(y2*(3.6-0.4*y1-3.6*y2))
            y3s.append(y3*(3.6-0.4*y2-3.6*y3))
            y4s.append(y4*(3.8-0.35*y3-3.8*y4))
        with open('../data/test/testdata.json', 'w') as f:
            jsonfile = dict(y1=y1s, y2=y2s, y3=y3s, y4=y4s)
            json.dump(jsonfile, f)

    def simplex_projection(self, src, embed_E, advance=1, delta_T=1):
        k = embed_E - 1
        # attractor
        attractorX = []
        firstX = delta_T * (embed_E - 1)+1  # 1 index
        lastX = len(src)
        for i in range(firstX-1, lastX):
            attractorX.append(
                src[i-(embed_E-1)*delta_T: i+1: delta_T])
        attractorX = np.array(attractorX)
        test_data = src[firstX-1:]
        # k nearest neighbors
        # distances & sort & predict
        dlt = 0.00000001
        predictY, observeY = [], []
        for veci, vecx in enumerate(attractorX):  # index & observation
            if veci == len(test_data) - advance:
                break
            dists = [np.linalg.norm(vecx-vec)+dlt for vec in attractorX]
            indices = sorted(range(len(dists)), key=lambda i: dists[i])[:k+1]
            assert veci == indices[0]
            indices = indices[1:]
            ordered_dists = [dists[i] for i in indices]
            d1 = ordered_dists[0]
            uis = [np.exp(-di/d1) for di in ordered_dists]
            N = sum(uis)
            ws = [ui / N for ui in uis]
            pred = 0
            for wi, ind in zip(ws, indices):
                if ind+advance >= len(test_data) - advance:
                    continue
                pred += wi*test_data[ind+advance]
            predictY.append(pred/sum(ws))
            observeY.append(test_data[veci+advance])
        assert len(predictY) == len(observeY)
        p, _ = pearsonr(np.array(predictY), np.array(observeY))
        return p

    def embedding_dimension(self, display=False):
        with open('../data/test/testdata.json', 'r') as f:
            dataset = json.load(f)
        elist = range(2, 11)
        results = []
        for key, data in dataset.items():
            src = data
            res = []
            for e in elist:
                res.append(self.simplex_projection(src, e))
            results.append(res)
        if display:
            fig = plt.figure()
            # fig.show()
            ax = fig.add_subplot(111)
            color = ['r', 'g', 'b', 'c']
            label = ['y1', 'y2', 'y3', 'y4']
            for i, v in enumerate(results):
                ax.plot(elist, v, c=color[i], ls='-', label=label[i])
            plt.legend(loc='upper right')
            plt.draw()
            plt.show()

    def calculate_causality(self, lag=1, embed=4, display=False):
        '''
        calculate causality of time series data by CCM
        '''
        with open('../data/test/testdata.json', 'r') as f:
            dataset = json.load(f)
        y1s, y2s, y3s, y4s = np.array(dataset['y1']), \
            np.array(dataset['y2']), np.array(dataset['y3']), \
            np.array(dataset['y4'])
        e1, e2, e3, e4 = ccm.Embed(y1s), ccm.Embed(y2s),\
            ccm.Embed(y3s), ccm.Embed(y4s)
        d1, d2, d3, d4 = e1.embed_vectors_1d(lag, embed),\
            e2.embed_vectors_1d(lag, embed),\
            e3.embed_vectors_1d(lag, embed),\
            e4.embed_vectors_1d(lag, embed)
        libs = np.arange(8, 404, 4, dtype='int')
        results = []
        for data_pair in itertools.combinations([d1, d2, d3, d4], 2):
            xtr, xte, ytr, yte = train_test_split(data_pair[0], data_pair[1],
                                                  percent=.75)
            c = ccm.CCM()
            c.fit(xtr, ytr)
            c.predict(xte, yte, lib_lengths=libs)
            sc1, sc2 = c.score()
            results.append([sc1, sc2])
        # save data to matrix
        index = itertools.combinations(range(4), 2)
        causality_list = [[0.0]*4 for _ in range(4)]
        for res, i in zip(results, index):
            sc1, sc2 = res[0], res[1]
            i1, i2 = i[0], i[1]
            causality_list[i1][i2] = abs((sc1[-1] - sc1[0]) * sc1[-1])
            causality_list[i2][i1] = abs((sc2[-1] - sc2[0]) * sc2[-1])
        causality = []
        for i in range(4):
            for j in range(4):
                causality.append(dict(src=i, dst=j,
                                      value=causality_list[i][j]))
        with open('../static/matrixT.json', 'w') as f:
            jsonfile = {'length': 4, 'causality': causality,
                        'matrix': causality_list}
            json.dump(jsonfile, f)
        # visaulize data
        if display:
            fig = plt.figure()
            # fig.show()
            ax = fig.add_subplot(111)
            items = [{'color': 'r', 'data': ['y1', 'y2']},
                     {'color': 'g', 'data': ['y1', 'y3']},
                     {'color': 'b', 'data': ['y1', 'y4']},
                     {'color': 'c', 'data': ['y2', 'y3']},
                     {'color': 'm', 'data': ['y2', 'y4']},
                     {'color': 'y', 'data': ['y3', 'y4']}]
            for i, v in enumerate(results):
                color = items[i]['color']
                d1, d2 = items[i]['data'][0], items[i]['data'][1]
                ax.plot(libs, v[0], c=color, ls='-', label=d1+'->'+d2)
                ax.plot(libs, v[1], c=color, ls=':', label=d2+'->'+d1)
            plt.legend(loc='upper right')
            plt.draw()
            plt.show()

    def multiview(self, lag_T=1, lag_L=3, embed_E=2):
        with open('../data/test/testdata.json', 'r') as f:
            dataset = json.load(f)
        y1, y2, y3, y4 = dataset['y1'], dataset['y2'], dataset['y3'],\
            dataset['y4']

        def analyize(source, refers):
            '''
            predict src by ref
            '''
            n = 3  # len(ref)
            l = lag_L
            e = embed_E
            # possible combinations
            combinations = []
            for ni in range(n):
                for li in range(l):
                    combinations.append([ni, li])
            results = [dict(coef=-1, data=[], lag=[])] * 5
            for combs in itertools.combinations(combinations, e):
                # skip = True
                # for comb in combs:
                #     if comb[1] == l - 1:
                #         skip = False
                #         break
                # if skip:
                #     continue
                # prepare data
                length = len(source)
                src = source[l-1:]
                reflist = []
                for comb in combs:
                    data, lag = refers[comb[0]], comb[1]
                    reflist.append(data[l-lag-1:length-lag])
                reflist = np.array(reflist)
                nodes = reflist.T
                print(combs, length, len(src), len(reflist[0]))
                pred_num = e - 1
                predictY, observeY = [], []
                dlt = 0.00000001
                for node_i, src_node in enumerate(nodes):
                    dists = [np.linalg.norm(src_node - dst_node) + dlt
                             for dst_node in nodes]
                    indices = sorted(range(len(dists)), key=lambda i: dists[i])
                    assert node_i == indices[0]
                    indices = indices[1:pred_num+1]
                    ordered_dists = [dists[i] for i in indices]
                    d1 = ordered_dists[0]
                    uis = [np.exp(-di/d1) for di in ordered_dists]
                    N = sum(uis)
                    ws = [ui / N for ui in uis]
                    pred = 0
                    for wi, ind in zip(ws, indices):
                        pred += wi * src[ind]
                    predictY.append(pred/sum(ws))
                    observeY.append(src[node_i])
                assert len(predictY) == len(observeY)
                p, _ = pearsonr(np.array(predictY), np.array(observeY))
                p = abs(p)
                if p > results[0]['coef']:
                    res_data = [d[0] for d in combs]
                    res_lag = [d[1] for d in combs]
                    results[0] = dict(coef=p, data=res_data, lag=res_lag)
                results.sort(key=lambda x: x['coef'])
            return results

        dataset = [y1, y2, y3, y4]
        results = {}
        for i, data in enumerate(dataset):
            ref = dataset[:]
            ref.pop(i)
            print('src: ', i)
            results[i] = analyize(data, ref)
        with open('../static/resultT1.json', 'w') as f:
            json.dump(results, f)


if __name__ == '__main__':
    ty = ToyModel()
    # ty.calculate_causality()
    # ty.embedding_dimension(display=True)
    ty.multiview(lag_T=1, lag_L=6, embed_E=3)

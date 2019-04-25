import numpy as np
import LCS
import time
import copy
import DataPretreatment
import math

UNCLASSIFIED = False
NOISE = 0
data_tmp = None


def dist(a, b):
    """
    输入：向量A, 向量B
    输出：两个向量的欧式距离
    """
    a_new = copy.deepcopy(a)
    b_new = copy.deepcopy(b)
    return LCS.get_lcs_distance(a_new,b_new)

def eps_neighbor(a, b, eps):
    """
    输入：向量A, 向量B
    输出：是否在eps范围内
    """
    return dist(a, b) < eps

def region_query(data, pointId, eps):
    """
    输入：数据集, 查询点id, 半径大小
    输出：在eps范围内的点的id
    """
    nPoints = data.shape[1]
    seeds = []
    for i in range(nPoints):
        if eps_neighbor(data_tmp[pointId], data_tmp[i], eps):
            seeds.append(i)
    return seeds

def expand_cluster(data, clusterResult, pointId, clusterId, eps, minPts):
    """
    输入：数据集, 分类结果, 待分类点id, 簇id, 半径大小, 最小点个数
    输出：能否成功分类
    """
    seeds = region_query(data, pointId, eps)
    if len(seeds) < minPts: # 不满足minPts条件的为噪声点
        clusterResult[pointId] = NOISE
        return False
    else:
        clusterResult[pointId] = clusterId # 划分到该簇
        for seedId in seeds:
            clusterResult[seedId] = clusterId

        while len(seeds) > 0: # 持续扩张
            currentPoint = seeds[0]
            queryResults = region_query(data, currentPoint, eps)
            if len(queryResults) >= minPts:
                for i in range(len(queryResults)):
                    resultPoint = queryResults[i]
                    if clusterResult[resultPoint] == UNCLASSIFIED:
                        seeds.append(resultPoint)
                        clusterResult[resultPoint] = clusterId
                    elif clusterResult[resultPoint] == NOISE:
                        clusterResult[resultPoint] = clusterId
            seeds = seeds[1:]
        return True

def dbscan(data, eps):
    """
    输入：数据集, 半径大小, 最小点个数
    输出：分类簇id
    """
    global data_tmp
    clusterId = 1
    nPoints = len(data)
    clusterResult = [UNCLASSIFIED] * nPoints

    MinPtsCandidate = []
    for i in range(len(data)):
        MinPtsCandidate.append(data[i].pop())
    # print(MinPtsCandidate)

    original_minpts = MinPtsCandidate[0]

    data_tmp = copy.deepcopy(data)

    data = np.mat(data).transpose()
    for pointId in range(nPoints):
        point = data[:, pointId]
        if pointId == 0 :
            minPts = original_minpts
        else:
            minPts = math.sqrt(MinPtsCandidate[pointId]/original_minpts) * minPts
            # print(minPts)
        if clusterResult[pointId] == UNCLASSIFIED:
            if expand_cluster(data, clusterResult, pointId, clusterId, eps, minPts):
                clusterId = clusterId + 1
    return clusterResult, clusterId - 1


def main():
    dataSet = DataPretreatment.D1
    eps = DataPretreatment.EpsCandidate
    # print(dataSet)
    ClusterNumberList = []
    for i in range(len(eps)):
        clustering, clusterNum = dbscan(dataSet[i], eps[i])
        ClusterNumberList.append(clusterNum)
    print(clusterNum)
    # print("cluster Numbers = ", clusterNum)
    # print(clusters)
    # result = [[] for i in range(clusterNum + 2)]
    # print(result)
    # for i in range(len(clustering)):
    #     if clustering[i] == -1:
    #         result[clusterNum + 1].append(dataSet[5][i])
    #     else:
    #         result[clustering[i]].append(dataSet[5][i])
    #
    # for i in range(len(result)):
    #     for j in range(len(result[i])):
    #         result[i][j].pop()
    #         while result[i][j][-1] == -1 or result[i][j][-1] == 10 or result[i][j][-1] == 13 or result[i][j][-1] == 9:
    #             result[i][j].pop()
    #
    # for i in range(len(result)):
    #     for j in range(len(result[i])):
    #         print(bytes(result[i][j]))
    #     print("")

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print('finish all in %s' % str(end - start))
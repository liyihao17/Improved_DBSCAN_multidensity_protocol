import numpy as np
import LCS
import time
import copy
import DataPretreatment
import math
import pickle
import operator

final_result = None
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
    if operator.eq(a_new,b_new) == True:
        return 0
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


def CalculateSilhouetteCoefficient(result):
    """
    计算聚类结果的轮廓系数
    :param result: 聚类结果
    :return: 轮廓系数
    """
    S = 0
    num_global = 0
    if len(result) == 1:
        return -1
    for i in range(len(result)):
        if len(result[i]) == 1:
            S = S + 0
            num_global = num_global + 1
        else:
            for j in range(len(result[i])):
                a = 0
                b_list = []
                num_global = num_global + 1
                for k in range(len(result[i])):
                    if j == k:
                        continue
                    a = a + LCS.get_lcs_distance(result[i][j],result[i][k])
                a = a/(len(result[i])-1)
                for i_tmp in range(len(result)):
                    if i == i_tmp:
                        continue
                    for j_tmp in range(len(result[i_tmp])):
                        b_list.append(LCS.get_lcs_distance(result[i][j],result[i_tmp][j_tmp]))
                if len(b_list) == 0:
                    return 0
                b = min(b_list)
                if max(a,b) == 0:
                    break
                S = S + (b - a)/max(a,b)
    S = S/num_global
    return S



def main():
    dataSet = DataPretreatment.D1
    eps = DataPretreatment.EpsCandidate
    # print(dataSet)
    ClusterNumberandIndexList = []
    cluster_result = []
    f = open('result.txt','w')
    for i in range(len(eps)):
        clustering, clusterNum = dbscan(dataSet[i], eps[i])
        result = [[] for i in range(clusterNum + 2)]
        for j in range(len(clustering)):
            if clustering[j] == -1:
                result[clusterNum + 1].append(dataSet[i][j])
            else:
                result[clustering[j]].append(dataSet[i][j])

        for i_1 in range(len(result)):
            for j_1 in range(len(result[i_1])):
                result[i_1][j_1].pop()
                while result[i_1][j_1][-1] == -1 or result[i_1][j_1][-1] == 10 or result[i_1][j_1][-1] == 13 or result[i_1][j_1][-1] == 9:
                    result[i_1][j_1].pop()
        ClusterNumberandIndexList.append((clusterNum,eps[i]))
        print('cluster number is ' + repr(ClusterNumberandIndexList[i][0]))
        # print("SilhouetteCoefficient is " + repr(ClusterNumberandIndexList[i][2]))
        f.write('cluster number is ' + repr(ClusterNumberandIndexList[i][0]+1))
        f.write('\n')
        # print('Silhouette Coefficient is ' + repr(ClusterNumberandIndexList[i][1]))
        f.write("eps is " + repr(ClusterNumberandIndexList[i][1]))
        # f.write('\n')
        # f.write("SilhouetteCoefficient is " + repr(ClusterNumberandIndexList[i][2]))
        f.write('\n')
        f.write("the result of cluster is ")
        f.write('\n')
        for i_1 in range(len(result)):
            f.write("")
            f.write('the number ' + repr(i_1) + ' cluster is \n')
            for j_1 in range(len(result[i_1])):
                # f.write(bytes(result[i_1][j_1]))
                for k_1 in range(len(result[i_1][j_1])):
                    f.write(chr(result[i_1][j_1][k_1]))
                f.write('\n')
            f.write('\n')
        f.write("\n\n")
        cluster_result.append(result)
    f.close()

    global final_result
    for k in range(len(cluster_result)):
        file_name = 'result' + str(k) + '.bin'
        final_result= copy.deepcopy(cluster_result[k])
        final_result_tmp = copy.deepcopy(final_result)
        for i in range(len(final_result_tmp)):
            if len(final_result_tmp[i]) == 0:
                final_result.remove(final_result_tmp[i])
        final_result_tmp = copy.deepcopy(final_result)
        for i in range(len(final_result_tmp)):
            for j in range(len(final_result_tmp[i])):
                final_result[i][j] = bytes(final_result_tmp[i][j])

        # print('final cluster result is ')
        # for i in range(len(final_result)):
        #     for j in range(len(final_result[i])):
        #         print(final_result[i][j])
        #     print('')

        f = open(file_name,'wb')
        pickle.dump(final_result,f)
        f.close()


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
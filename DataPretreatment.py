import PcapReader
import numpy as np
import copy
import LCS
import time

OriginalDistMatrix = []
message_list_original,message_list = PcapReader.ImportMessage()

def TakeLast(elem):
    """
    用于排序函数,获取最后一个元素,在排序的时候可以按最后一个元素进行排序
    :param elem: 列表
    :return: 列表中最后一个元素
    """
    return elem[-1]


def dist(a, b):
    """
    输入：向量A, 向量B
    输出：两个向量的欧式距离
    """
    a_new = copy.deepcopy(a)
    b_new = copy.deepcopy(b)
    return LCS.get_lcs_distance(a_new,b_new)


def returnDk(matrix,k):
    """
    用来计算第K最近的距离集合
    :param matrix: 距离矩阵
    :param k: 第k最近
    :return: 第k最近距离集合
    """
    Dk = []
    for i in range(len(matrix)):
        Dk.append(matrix[i][k])
    return Dk


def returnDkAverage(Dk):
    """
    求第K最近距离集合的平均值
    :param Dk: k-最近距离集合
    :return: Dk的平均值
    """
    sum = 0
    for i in range(len(Dk)):
        sum = sum + Dk[i]
    return sum/len(Dk)


def CalculateDistMatrix(dataset):
    """
    计算距离矩阵
    :param dataset: 数据集
    :return: 距离矩阵
    """
    start = time.clock()
    print('DistMatrix are being calculated')
    DistMatrix = [[0 for j in range(len(dataset))] for i in range(len(dataset))]
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            DistMatrix[i][j] = dist(dataset[i], dataset[j])
    end = time.clock()
    print('DistMatrix calculating over ' + repr(end - start) + ' seconds')
    return DistMatrix


def returnEpsCandidate(dataSet,threshold):
    """
    返回Eps候选列表
    :param dataSet: 数据集
    :param threshold: 阈值
    :return: Eps侯选高于阈值后不再进行计算
    """
    global OriginalDistMatrix
    DistMatrix = CalculateDistMatrix(dataSet)
    OriginalDistMatrix = DistMatrix     #将距离矩阵存到全局变量OriginalDistMatrix中去
    tmp_matrix = copy.deepcopy(DistMatrix)
    for i in range(len(tmp_matrix)):
        tmp_matrix[i].sort()
    EpsCandidate = []
    for k in range(1,len(dataSet)):
        Dk = returnDk(tmp_matrix,k)
        DkAverage = returnDkAverage(Dk)
        if DkAverage >= threshold:
            break
        EpsCandidate.append(DkAverage)
    return EpsCandidate


def returnD1(EpsCandidate):
    """
    返回各Eps候选的排序数据集
    :param dataSet: 初始数据集
    :param EpsCandidate: Eps候选集合
    :return: 各Eps候选的排序数据集
    """
    global OriginalDistMatrix
    global message_list
    D1 = []
    DistMatrixTmp = copy.deepcopy(OriginalDistMatrix)
    for k in range(len(EpsCandidate)):
        eps = EpsCandidate[k]
        message_list_tmp = copy.deepcopy(message_list)
        for i in range(len(DistMatrixTmp)):
            count = 0
            for j in range(len(DistMatrixTmp[i])):
                if DistMatrixTmp[i][j] <= eps:
                    count = count + 1
            message_list_tmp[i].append(count)
        message_list_tmp.sort(key=TakeLast,reverse=True)
        D1.append(message_list_tmp)
    return D1


EpsCandidate = returnEpsCandidate(message_list,0.75) #Eps参数候选列表,全局变量
D1 = returnD1(EpsCandidate) #后面接Eps内点数的预处理后的数据集,全局变量


if __name__ == '__main__':
    EpsCandidate = returnEpsCandidate(message_list,0.5)
    # print(EpsCandidate)
    D1 = returnD1(EpsCandidate)
    for i in range(len(D1)):
        print("\n\n\n\n\n")
        for j in range(len(D1[i])):
            print(D1[i][j])
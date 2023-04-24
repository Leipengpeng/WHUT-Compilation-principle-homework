'''
11.11开始书写       软件sy2001班 雷裕庭
本项目用于实现从NFA到DFA的转化
目标 在11.11之前完成最基础的实现
'''
import copy
import queue

import numpy as np



# 从dict文件中获得Null的连通图
def matrixN(input):

    #首先得知最大的状态数
    maxNum=0
    for i in range(len(input)):
        maxNum=max(max(maxNum,input[i]['start']),max(maxNum,input[i]['next']))

    #基于最大状态数 创建空矩阵
    maxNum+=1
    matrix = [[0] * maxNum for _ in range(maxNum)]

    #填写矩阵
    for i in range(len(input)):
        if input[i]['c']=='~':
            matrix[input[i]['start']][input[i]['next']] = 1

    return matrix

# 从dict文件中获得A相关的连通图
def matrixA(input):

    #首先得知最大的状态数
    maxNum=0
    for i in range(len(input)):
        maxNum=max(max(maxNum,input[i]['start']),max(maxNum,input[i]['next']))

    #基于最大状态数 创建空矩阵
    maxNum+=1
    matrix = [[0] * maxNum for _ in range(maxNum)]

    #填写矩阵
    for i in range(len(input)):
        if input[i]['c']=='a':
            matrix[input[i]['start']][input[i]['next']] = 1

    return matrix

# 从dict文件中获得B相关的连通图
def matrixB(input):

    #首先得知最大的状态数
    maxNum=0
    for i in range(len(input)):
        maxNum=max(max(maxNum,input[i]['start']),max(maxNum,input[i]['next']))

    #基于最大状态数 创建空矩阵
    maxNum+=1
    matrix = [[0] * maxNum for _ in range(maxNum)]

    #填写矩阵
    for i in range(len(input)):
        if input[i]['c']=='b' :
            matrix[input[i]['start']][input[i]['next']] = 1

    return matrix

# 实现矩阵乘
def matrixPlus(matrix1, matrix2):
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    out = np.dot(matrix1, matrix2)
    return list(out)

# 将两个矩阵进行逻辑上的加法
def matrixCon(matrix1,matrix2):
    out = copy.deepcopy(matrix1)
    lenth=len(matrix1)

    for j in range (lenth):
        for k in range(lenth):
            if matrix2[j][k]!=0:
                out[j][k] = 1
    return out

'''
DFS:深度遍历
得到n在matrix中可达的全部元素的set
注:在本项目中主要用于计算 空 的 可达情况
'''
def DFS(matrix,n):
    out=set()
    stack=queue.Queue(maxsize=100)
    lenth=len(matrix)
    out.add(n)
    stack.put(n)

    #初始化栈
    while stack.qsize()>0:
        m=stack.get()
        for j in range(lenth):
            if matrix[m][j] == 1:
                if out.__contains__(j)!=True:
                    out.add(j)
                    stack.put(j)
    return  out


'''
contain:自定义的contain函数 用于判断list集内是否存在对应的set
'''
def contain(hashMap,condition):
    for i in range(len(hashMap)):
        if hashMap[i]==condition:
            return True
    print("不存在状态"+str(condition))
    return False

'''
closureA:计算set 的 Ia closure集合 并输出为set
计算逻辑
1.算出一个元素和其空集的可达集合1
2.算出该可达集合距离a的可达集合2
3.计算可达集合2+可达集合2+空的可达集
4.输出
'''

def closureA(input:set,matrixA:list,matrixN:list):
    lenth= len(matrixA)
    temp=copy.deepcopy(input)       #原始集合  为避免浅拷贝数据污染
    temp1=copy.deepcopy(input)      #可达集合1

    #1.算出一个元素和其空集的可达集合1
    while temp:
        tempInt=temp.pop()
        temp1.update(DFS(matrixN,tempInt))
    print('#1.算出一个元素和其空集的可达集合1'+str(temp1))

    # 2.算出该可达集合距离a的可达集合2
    temp2 = set()
    while temp1:
        tempInt = temp1.pop()
        for i in range(lenth):
            if matrixA[tempInt][i]==1:
                temp2.add(i)
    print('#2.算出该可达集合距离a的可达集合2'+str(temp2))

    #3.计算可达集合2 + 可达集合2 + 空的可达集
    out = copy.deepcopy(temp2)
    while temp2:
        tempInt=temp2.pop()
        out.update(DFS(matrixN,tempInt))
    print('#3.计算可达集合2 + 可达集合2 + 空的可达集'+str(out))

    return out

'''
closureB:计算set 的 Ib closure集合 并输出为set
'''
def closureB(input:set,matrixB:list,matrixN:list):
    lenth = len(matrixB)
    temp = copy.deepcopy(input)  # 原始集合  为避免浅拷贝数据污染
    temp1 = copy.deepcopy(input)  # 可达集合1

    # 1.算出一个元素和其空集的可达集合1
    while temp:
        tempInt = temp.pop()
        temp1.update(DFS(matrixN, tempInt))

    # 2.算出该可达集合距离a的可达集合2
    temp2 = set()
    while temp1:
        tempInt = temp1.pop()
        for i in range(lenth):
            if matrixB[tempInt][i] == 1:
                temp2.add(i)

    # 3.计算可达集合2 + 可达集合2 + 空的可达集
    out = copy.deepcopy(temp2)
    while temp2:
        tempInt = temp2.pop()
        out.update(DFS(matrixN, tempInt))

    return out

'''
matrixLink:主函数
算法逻辑：    状态以set的方法进行储存
            一个hash表，不断的接受和处理新的状态情况
            一个list栈，储存还未计算closure的状态集
            一个储存dict集的list，储存变化后的状态(I Ia Ib)
'''
def matrixLink(input):
    #初始化矩阵
    mN = matrixN(input)
    mA = matrixA(input)
    mB = matrixB(input)
    print("matrixA" + str(mA))
    print("matrixB" + str(mB))
    print("matrixN" + str(mN))
    #初始化三个主要的数据结构
    hashMap=list()          #储存已知的状态
    unfinished=list()       #储存还未处理 已知的状态
    path=list()

    #下面开始不断的计算closure集
    #首先初始化
    hashMap.append(DFS(mN,0))
    unfinished.append(DFS(mN, 0))
    while len(unfinished)>0:
        temp = copy.deepcopy(unfinished.pop())
        tempA = copy.deepcopy(closureA(temp, mA, mN))
        tempB = copy.deepcopy(closureB(temp, mB, mN))
        path.append({"I":temp,"Ia":tempA,"Ib":tempB})
        while contain(hashMap,tempA)==False:
            hashMap.append(tempA)
            unfinished.append(tempA)
        while contain(hashMap,tempB)==False:
            hashMap.append(tempB)
            unfinished.append(tempB)

    return path

if __name__ == '__main__':
    input = [
        {'start': 0, 'next': 4, 'c': '~'},
        {'start': 1, 'next': 2, 'c': 'a'},
        {'start': 2, 'next': 3, 'c': 'b'},
        {'start': 3, 'next': 5, 'c': 'b'},
        {'start': 4, 'next': 1, 'c': '~'},
        {'start': 4, 'next': 4, 'c': 'a'},
        {'start': 4, 'next': 4, 'c': 'b'},
    ]
    path=matrixLink(input)
    for i in range(len(path)):
        print(path[i])


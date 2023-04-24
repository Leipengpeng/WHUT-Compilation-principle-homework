'''
11.12开始 此项目用于将dfs装换为最简dfs
目标：在11.12结束前完成
'''

'''
思路:其实有两种不同的思考方法：
1.合并全部的离散的状态 通过一种拼接方法 使得最多的状态被组合 同时满足 Ia Ib 可规约的要求
2.切割 以切割的组的数量最小为目标进行处理

下面主要是依据第一种思路进行处理
逻辑方法如下
1.首先验证一点:是否有可迭代性？
'''
import copy
import queue

'''
下面是复用自实验二的部分函数 功能和实现方法不再做赘述
'''
# 从dict文件中获得A相关的连通图
def matrixA(input):
    maxNum=0
    for i in range(len(input)):
        maxNum=max(max(maxNum,input[i]['start']),max(maxNum,input[i]['next']))
    maxNum+=1
    matrix = [[0] * maxNum for _ in range(maxNum)]
    for i in range(len(input)):
        if input[i]['c']=='a':
            matrix[input[i]['start']][input[i]['next']] = 1
    return matrix

# 从dict文件中获得B相关的连通图
def matrixB(input):
    maxNum=0
    for i in range(len(input)):
        maxNum=max(max(maxNum,input[i]['start']),max(maxNum,input[i]['next']))
    maxNum+=1
    matrix = [[0] * maxNum for _ in range(maxNum)]
    for i in range(len(input)):
        if input[i]['c']=='b' :
            matrix[input[i]['start']][input[i]['next']] = 1
    return matrix

#实现DFS
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
因为不再存在空字符 对closure的计算自然有略微的修改
'''
#closureA:计算set 的 Ia closure集合 并输出为set
def closureA(input:set,matrixA:list):
    lenth= len(matrixA)
    temp=copy.deepcopy(input)       #原始集合  为避免浅拷贝数据污染
    out=set()
    while temp:
        tempInt = temp.pop()
        for i in range(lenth):
            if matrixA[tempInt][i]==1:
                out.add(i)
    return out

#closureB:计算set 的 Ib closure集合 并输出为set
def closureB(input:set,matrixB:list,):
    lenth = len(matrixB)
    temp = copy.deepcopy(input)  # 原始集合  为避免浅拷贝数据污染
    out = set()
    while temp:
        tempInt = temp.pop()
        for i in range(lenth):
            if matrixB[tempInt][i] == 1:
                out.add(i)
    return out

def getMax(input):
    maxNum=0
    for i in range(len(input)):
        maxNum=max(max(maxNum,input['start']),max(maxNum,input['next']))
    return maxNum

def isIn(inputSet,setList):
    lenth=len(setList)
    for i in range(lenth):
        if set(setList[i]["element"]).issubset(set(inputSet)):
            return True
    return False

'''
通过一个A*算法实现      通过分割集合尽可能的增加finishedNum集合
解树:广度遍历获得  例:对于4元组 4*3 (层数:n//2)
A*的激励函数      best:两子集均可被finish
                middle:一个可finish 一个不可finish
                worst:均不可finish
输出:dict数据结构的子集 out1 out2        一个代表分割情况的Int参数 1 0 -1
其他要求:过程隔离，避免数据污染，不修改输入数据
'''
def separate(mA,mB,setList,temp):                   #输入 matrixA matrixB 当前集合情况
    orignalList=copy.deepcopy(temp["element"])
    layerNum=len(orignalList)//2
    possible=list()


    return 0



'''
SplitSimplify 主逻辑计算函数
算法设计如下:
        1.首先区分出终结符集 T 和 非终结符集 U 两个集合均通过dict的方法储存在一个list中
                数据结构 [ {"class":'T',"cuttable":True,"element":[1,2,3]}*N  etc ]
        2.接下来就不断的访问cuttable的dict的element，通过已有的closureB函数判断其是否要继续切割
        3.直到全部的函数均为uncattable(设立变量)
'''

def SplitSimplify(input):
    # 初始化矩阵
    mA = matrixA(input)
    mB = matrixB(input)
    print("matrixA" + str(mA))
    print("matrixB" + str(mB))
    setNum=2                                    #集合数量
    finishedNum=0                               #不可分集合数量
    setList=list()                              #用于储存全部状态的集合  允许对被分割的集合实施删除操作

    #预处理 区分为 T 和 N
    temp1 = {"class": 'T', "cuttable": True, "element": [4]}
    temp2 = {"class": 'T', "cuttable": True, "element": [0,1,2,3]}
    if len(temp1['element'])==1:
        finishedNum+=1
        temp1['cuttable']=False

    if len(temp2['element'])==1:
        finishedNum+=1
        temp1['cuttable']=False

    setList.append(temp1)
    setList.append(temp2)

    #开始计算
    while setNum>finishedNum:
        print(setList)
        print(setNum,"    ",finishedNum)
        #勉为其难的用list实现了一下一下queue的操作 实在不喜欢使用太多引申类型
        temp=copy.deepcopy(setList[0])
        setNum-=1
        del setList[0]
        if temp['cuttable']==True:
            temp1 = closureA(temp["element"],mA)
            temp2 = closureB(temp["element"],mB)
            if isIn(temp1,setList)==False or isIn(temp2,setList)==False:
                print(1)
                setNum+=3
                finishedNum+=3
                temp1 = {"class": 'T', "cuttable": False, "element": [0]}
                temp2 = {"class": 'T', "cuttable": False, "element": [2]}
                temp3 = {"class": 'T', "cuttable": False, "element": [1,3]}
                setList.append(copy.deepcopy(temp1))
                setList.append(copy.deepcopy(temp2))
                setList.append(copy.deepcopy(temp3))

            else :
                print(3)
                temp['cuttable']=False
                finishedNum+=1
                setList.append(copy.deepcopy(temp))
                setNum+=1
        else:
            setList.append(copy.deepcopy(temp))
            setNum += 1
    return setList


if __name__ == '__main__':

    #注:为方便计算 已经将XY转换为数字 全部的原数字位做+1处理
    input1 = [
        {'start': 0, 'next': 1, 'c': 'a'},
        {'start': 0, 'next': 2, 'c': 'b'},
        {'start': 4, 'next': 1, 'c': 'a'},
        {'start': 4, 'next': 2, 'c': 'b'},
        {'start': 1, 'next': 1, 'c': 'a'},
        {'start': 1, 'next': 3, 'c': 'b'},
        {'start': 2, 'next': 1, 'c': 'a'},
        {'start': 2, 'next': 2, 'c': 'b'},
        {'start': 3, 'next': 1, 'c': 'a'},
        {'start': 3, 'next': 4, 'c': 'b'}
    ]

    input2=[
        {'I': {0, 1, 4}, 'Ia': {1, 2, 4}, 'Ib': {1, 4}},
        {'I': {1, 4}, 'Ia': {1, 2, 4}, 'Ib': {1, 4}},
        {'I': {1, 2, 4}, 'Ia': {1, 2, 4}, 'Ib': {1, 3, 4}},
        {'I': {1, 3, 4}, 'Ia': {1, 2, 4}, 'Ib': {1, 4, 5}},
        {'I': {1, 4, 5}, 'Ia': {1, 2, 4}, 'Ib': {1, 4}},
    ]
    temp=SplitSimplify(input1)
    print(temp)

'''
11.12创建文档       软件sy2001雷裕庭
目标 在11.13前完成该文档
以下项目主要是通过 最简的DFA 实现对于语法的辨别
输入: DFA 字符窜
输出: 通过 或者是 不通过 编译
'''


'''
下面是复用自实验三的部分函数 功能和实现方法不再做赘述
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

'''
lexAnalys:函数直接实现对于语法的解析
输出结果为 True or False
'''
def lexAnalys(input,inputStr:str):
    #初始化连通矩阵
    mA = matrixA(input)
    mB = matrixB(input)
    print(mA)
    print(mB)
    size= len(mB)
    lenth= len(inputStr)
    tempSate=0                #用于记录当前状态
    stateList=list()          #用于记录每一步的状态

    #start       由于已为最简DFA了，状态转化是确定的不存在歧义(亦不需要树状结构处理)
    print("当前状态为X")
    stateList.append('X')
    for i in range (lenth):
        isIn = False
        temp=inputStr[i]
        if temp=='a':
            for j in range(size):
                if mA[tempSate][j]==1:
                    isIn=True
                    tempSate=j
                    stateList.append(j)
                    print("1字符串第" + str(i + 1) + "位输入为:" + temp)
                    print("输入合法，下一状态为"+str(j))
                    break
            if isIn==False:
                print("2字符串第" + str(i + 1) + "位输入为:" + temp)
                print("输入不合法，退出分析程序")
                return stateList, False
        elif temp=='b':
            for k in range(size):
                if mB[tempSate][k]==1:
                    isIn=True
                    tempSate=k
                    stateList.append(k)
                    print("3字符串第" + str(i + 1) + "位输入为:" + temp)
                    print("输入合法，下一状态为"+str(k))
                    break
            if isIn==False:
                print("4字符串第" + str(i + 1) + "位输入为:" + temp)
                print("输入不合法，退出分析程序")
                return stateList, False
        else:
            print("5字符串第"+str(i+1)+"位输入为:"+temp)
            print("输入不合法，退出分析程序")
            return stateList,False

    if tempSate==4:
        return stateList, True
    else:
        print("未到达终点，输入不合法")
        return stateList, False



if __name__ == '__main__':

    #注:为方便计算 已经将XY转换为数字 全部的原数字位做+1处理
    input = [
        {'start': 0, 'next': 1, 'c': 'a'},
        {'start': 0, 'next': 0, 'c': 'b'},
        {'start': 4, 'next': 1, 'c': 'a'},
        {'start': 4, 'next': 0, 'c': 'b'},
        {'start': 1, 'next': 1, 'c': 'a'},
        {'start': 1, 'next': 3, 'c': 'b'},
        {'start': 3, 'next': 1, 'c': 'a'},
        {'start': 3, 'next': 4, 'c': 'b'}
    ]

    inputStr1 = "abb"
    inputStr2 = "ba"
    inputStr3 = "abb;ba"

    out1,out2=lexAnalys(input,inputStr1)
    print(out1)
    print(out2)
    out1, out2 = lexAnalys(input, inputStr2)
    print(out1)
    print(out2)
    out1, out2 = lexAnalys(input, inputStr3)
    print(out1)
    print(out2)

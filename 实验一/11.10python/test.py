'''
11.10开始 软件sy2001班雷裕庭编写
以下程序用于将正则表达式装换为NFA  input:(a|b)*abb
更新日志：11.11继续编写 开始书写path逻辑变化
'''
import string
import copy

'''
graghMake:基于当前串的变化 动态的改变节点
图的状态不进行实体的记录 只记录图的节点的变化
每个图的初始有len+2个节点 len+1个path
算法设计如下:有两个path逻辑
path1用于记录真实的,有意义的,完全的(包括了已经不使用路径)的路径集
path2用于记录每一个节点(字符)前后对应的状态号
无论path12 起始状态号startStep=0 结束的状态号nextStep=lenth(原始的)
'''
def graghMake(input):
    path1 = list()                          # 字符路径的集合
    path2 = list()                          # 字符前后节点集合
    lenth=len(input)
    num=0                                   #num当前的状态数量

    #初始化path1  相当于已将全部zz情况处理完成
    start = {'useState': True,'startStep': num, 'nextStep': num+1, 'path': input[0]} #是否有效 起始状态 下一状态 路径方法
    path1.append(start)
    for i in range(lenth-1):
        num += 1
        temp = {'useState': True, 'startStep':num, 'nextStep': num+1, 'path': input[i+1]}
        path1.append(temp)

    # 初始化path2  相当于已将全部zz情况处理完成
    num=0
    start = {'startStep': num, 'nextStep': num + 1, 'path': input[0]}  # 起始点 终点 字符
    path2.append(start)
    for i in range(lenth-1):
        num += 1
        temp = {'startStep': num, 'nextStep': num + 1, 'path': input[i+1]}
        path2.append(temp)

    #打印path1检测
    print("打印path1检测")
    for i in range(len(path1)):
        print(path1[i])

    # 打印path2检测
    print("打印path2检测")
    for i in range(len(path2)):
        print(path2[i])

    #下面移交至delBrackets函数 判断括号 输出子串 改变path12
    delBrackets(input,path1,path2)

    return path1


'''
delBrackets：函数用于去除括号
输出去除了括号的字符串给予recognize来识别
同时储存不同的z规约串的相关信息
'''
def delBrackets(input,path1,path2):
    cList =""                           # 用于读取的字符栈结构
    i = 0                               # 尾部当前移动到的位置
    j = list()                          # 最后一个"("出现的位置

    lenth = len(input)
    while i < lenth:
        cList += input[i]
        if input[i] == ")":
            tempL = j.pop()
            temp = cList[tempL+1:len(cList)-1]
            cList = cList[0:tempL] + "z"

            #修改path2表 添加规约项 和对应的前后状态
            temppath=path2[tempL+1:len(cList)+len(temp)]
            path2.insert(tempL, {'startStep': path2[tempL]['startStep'], 'nextStep': path2[len(cList)+len(temp)]['nextStep'], 'path': 'z'})
            for n in range(len(temp)+2):
                del path2[tempL+1]

            #由recognize函数判断无括号子串的内容 基于path2(注:对于下一级的path2 而不是上一级的path2)的内容修改path1
            recognize(temp,path1,path2[tempL]['startStep'],path2[tempL]['nextStep'],temppath)
        elif input[i] == "(":
            j.append(i)
        i += 1
        print("当前的栈是" + cList)
    recognize(cList,path1,0,lenth,path2)


'''
graghSort:函数用来去除多余的path 并出现对状态进行编号
'''
def graghSort(path):
    return path

'''
graghSort:函数打印path 输出结果
'''
def graghPrint(path):
    print(path)

'''
recognize:函数用来处理不存在括号的子串
字符串的子集在三种情况下会转换为一个状态
优先级从前到后如下 R=A* R=A|B R=AB
'''
def recognize(input,path1,startP,endP,path2): #输入:无括号子串 集合地址 起始 终点
    print("识别无括号子串:"+input+"   当前子串前后节点:"+str(startP)+"  "+str(endP))
    print(path2)
    lenth = len(input)

    #为了便于寻找子串 下面建立一个全部为z的规则化子串temp
    temp=list()
    for i in range(lenth):
        if input[i]>='a' and input[i]<='z':
            temp.append('z')
        elif input[i]!="(" and input[i]!=")":
            temp.append(input[i])
    tempStr = "".join(temp)

    # 优先处理z*情况
    while tempStr.count('z*'):
        tempInt=tempStr.find('z*')

        # 调用state函数处理
        state1(input[tempInt:tempInt + 2], path1, path2[tempInt], path2[tempInt+1])

        # 修改input串和temp串
        tempStr=tempStr[0:tempInt]+"z"+tempStr[tempInt+2:len(tempStr)]
        input = tempStr[0:tempInt] + "z" + tempStr[tempInt + 2:len(tempStr)]

        #修改path2串
        path2.insert(tempInt,{'startStep': path2[tempInt]['startStep'], 'nextStep': path2[tempInt+1]['nextStep'],'path': 'z'})
        for n in range(2):
            del path2[tempInt+1]



    # 次优先处理z|z情况
    while tempStr.count('z|z'):
        tempInt=tempStr.find('z|z')

        # 调用state函数处理
        state2(input[tempInt:tempInt + 3], path1, path2[tempInt], path2[tempInt+2])

        #修改input串和temp串
        tempStr = tempStr[0:tempInt]+"z"+tempStr[tempInt + 3:len(tempStr)]
        input = tempStr[0:tempInt] + "z" + tempStr[tempInt + 3:len(tempStr)]

        # 修改path2串
        path2.insert(tempInt, {'startStep': path2[tempInt]['startStep'], 'nextStep': path2[tempInt + 2]['nextStep'],'path': 'z'})
        for n in range(3):
            del path2[tempInt + 1]



    #剩下的自然而然全部是zz形式的子串，直接串起即可 串的次数为len-1(不考虑前后的情况下)
    #不进行任何处理

'''
makeGragh系列:函数用来将对应的字母生成图和数据
'''

#R=A*
def state1(input,path1,start,end):
    print("R=A*识别中:"+input)
    a=input[0]
    print(start)
    print(end)
    if a=='z':
        temp = len(path1)
        tempPath = {'useState': True, 'startStep': start['nextStep'], 'nextStep': start['startStep'], 'path': '~'}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['nextStep'], 'path': '~'}
        path1.append(tempPath)
    else:
        temp=len(path1)
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': temp, 'path': '~'}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': temp, 'nextStep': temp, 'path': a}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': temp, 'nextStep': end['nextStep'], 'path': '~'}
        path1.append(tempPath)




#R=A|B
def state2(input,path1,start,end):
    print("R=A|B识别中:"+input)
    a1=input[0]
    a2=input[2]
    if a1 == 'z' and a2 != 'z':
        tempPath = {'useState': True, 'startStep': start['nextStep'], 'nextStep': end['nextStep'], 'path': '~'}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['nextStep'], 'path': a2}
        path1.append(tempPath)
    elif a1 != 'z' and a2 == 'z':
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['startStep'], 'path': '~'}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['nextStep'], 'path': a1}
        path1.append(tempPath)
    elif a1 == 'z' and a2 == 'z':
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['startStep'], 'path': '~'}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': start['nextStep'], 'nextStep': end['nextStep'], 'path': '~'}
        path1.append(tempPath)
    else:
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['nextStep'], 'path': a1}
        path1.append(tempPath)
        tempPath = {'useState': True, 'startStep': start['startStep'], 'nextStep': end['nextStep'], 'path': a2}
        path1.append(tempPath)


#R=AB  因为算法的设计，该部分已经在初始化的时候被取代 无需再进行处理
def state3(input):
    print("do nothing")
    print("R=AB识别中:"+input)


'''
main函数
'''
if __name__ == '__main__':
    input = "(a|b)*abb"
    path=graghMake(input)
    print("路径如下")
    for i in range(len(path)):
        print(path[i])






'''
11.10开始 软件sy2001班雷裕庭编写
以下程序用于将正则表达式装换为NFA      测试用例:     input:(a|b)*abb

更新日志:    11.11继续编写 开始书写path逻辑变化
           11.13开始修改 开始使用新的算法流程
           参考文献:    https://blog.csdn.net/qq_42256538/article
           逻辑:
                        1.先将中缀表达式转换为后缀表达式
                        2.将后缀表达式转换为NFA
                        3.all in all 以下代码按照这一逻辑书写
目标:在11.13前彻底完成
'''

'''
isChar:判断输入为字符还是符号
'''
def isChar(input):
    if input>="a" and input<="z":
        return True
    else:
        return False

'''
isChar:返回对应符号的权重 栈内只能存在一单向递增权重的数列
'''
def signWeight(input):
    if input=='|':
        return 2
    elif input=='&':
        return 3
    elif input=='*':
        return 4
    elif input=='(':
        return 1
    elif input==')':
        return 0
    return -1

'''
addElement:为str添加&  输出为list()
'''
def addElement(input:str):
    out=list(input)
    i=0
    while i <(len(out)-1):
        if (isChar(out[i])and isChar(out[i+1]))or(signWeight(out[i])==4and isChar(out[i+1])):
            out.insert(i+1,"&")
            i+=1
        i+=1
    return out

'''
infixToSuffix:中缀转换为后缀
'''
def infixToSuffix(input:list):
    lenth= len(input)
    cList=list()            #字符串
    eList=list()            #符号串
    eList.append('#')

    for i in range(lenth):
        #对list进行出栈操作
        tempC=input[0]
        del input[0]
        #字符情况
        if isChar(tempC):
            cList.append(tempC)
        #非")"符号情况
        elif signWeight(tempC)>0:
            cValue = signWeight(tempC)
            tempValue = signWeight(eList[len(eList) - 1])
            while cValue <= tempValue:
                cList.append(eList.pop())
                tempValue = signWeight(eList[len(eList) - 1])
            eList.append(tempC)

        # ")"符号情况
        elif signWeight(tempC)==0:
            tempE=eList.pop()
            while tempE!="(":
                cList.append(tempE)
                tempE = eList.pop()
    while eList:
        cList.append(eList.pop())
    del cList[len(cList)-1]
    return cList

'''
suffixToNFA:后缀转换为NFA
'''
def suffixToNFA(input:list):
    Num=0               #当前状态数量
    NFAlist=list()           #NFA栈
    path=list()         #用于输出的最终路径
    lenth= len(input)

    '''
    对dict数据结构说明 "start" "next" "c" "single"}
    前一个状态 后一个状态 状态装换条件 原子性
    '''

    for i in range(lenth):
        temp=input[i]
        if isChar(temp):
            tempDict={"start":Num,"next":Num+1,"c":temp,"single":True}
            NFAlist.append(tempDict)
            Num+=1
        elif temp=='|':
            temp1=NFAlist.pop()
            temp2=NFAlist.pop()
            #四条空边
            tempDict= {"start": Num, "next": temp1["start"], "c": 'Null',"single":True}
            path.append(tempDict)
            tempDict = {"start": Num, "next": temp2["start"], "c": 'Null', "single": True}
            path.append(tempDict)
            tempDict = {"start": temp1["next"], "next": Num+1, "c": 'Null', "single": True}
            path.append(tempDict)
            tempDict = {"start": temp2["next"], "next": Num+1, "c": 'Null', "single": True}
            path.append(tempDict)
            Num+=2
            path.append(temp1)
            path.append(temp2)
            #等价边入栈
            tempDict = {"start": Num, "next": Num + 1, "c": 'Null', "single": False}
            NFAlist.append(tempDict)
        elif temp=='*':
            temp = NFAlist.pop()
            #将两端状态无向连接的两条边
            tempDict = {"start": temp["start"], "next": temp["next"], "c": 'Null', "single": True}
            path.append(tempDict)
            tempDict = {"start": temp["next"], "next": temp["start"], "c": 'Null', "single": True}
            path.append(tempDict)
            #等价边入栈
            tempDict = {"start": temp["start"], "next": temp["next"], "c": 'Null', "single": True}
            NFAlist.append(tempDict)
        elif temp == '&':
            # 首尾相连
            tempDict = {"start": temp2["next"], "next": temp1["start"], "c": 'Null', "single": True}
            path.append(tempDict)
            path.append(temp1)
            path.append(temp2)
            # 将两端节点提出
            tempDict = {"start": temp2["start"], "next": temp1["next"], "c": 'Null', "single": False}
            NFAlist.append(tempDict)
    for i in range(len(NFAlist)):
        if NFAlist[i]["single"]==True:
            path.append(NFAlist[i])

    lenth= len(path)
    i=0
    while i <lenth:
        if path[i]["single"]==False:
            del path[i]
            i-=1
            lenth-=1
        i+=1
    return path
'''
toNFA:主程序
'''
def toNFA(input):

    tempList=addElement(input)
    print("添加间隔符")
    print(tempList)
    suffixList=infixToSuffix(tempList)
    print("中缀表达式转换为后缀表达式")
    print(suffixList)
    path=suffixToNFA(suffixList)
    print("后缀表达式转换为NFA")
    for i in range(len(path)):
        print(path[i])

    return path

'''
main函数
'''
if __name__ == '__main__':
    input = "(a|b)*abb"
    toNFA(input)

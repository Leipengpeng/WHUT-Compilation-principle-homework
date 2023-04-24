'''
实验五 11.21 软件sy2001 雷裕庭开始编写
11.24编写完成
'''

'''
isChar 判断是否为字符
'''
def isChar(input):
    input=str(input)
    if (input<="Z"and input>="A")or(input<="z"and input>="a"):
        return True
    return False

'''
isNum 判断是否为数字
'''
def isNum(input):
    input=str(input)
    if input<="9"and input>="0":
        return True
    return False

'''
stateChange 用于基于 输入状态 下一个字符的类型 返回下一个状态
'''
def stateChange(nowState:int,input:str,stateList:list,tempStr:str):
    # 多层处理
    print(' ')
    print('nowState    input    tempStr')
    print(nowState,'    ',input,'    ',tempStr)
    if nowState==1 and input=='':
        nextState=1
    elif nowState == 1 and input == ' ':
        nextState = 1
    elif nowState == 1 and input is None:
        nextState = 1
    elif nowState==1 and isChar(input):
        tempStr+=input
        nextState=2
    elif nowState==1 and isNum(input):
        tempStr += input
        nextState=4
    elif nowState==1 and input=="<":
        nextState=8
    elif nowState==1 and input==">":
        nextState=11

    #单一符号处理
    elif nowState==1 and input=="-":
        stateList.append('MINU')
        nextState=1
    elif nowState==1 and input=="*":
        stateList.append('MULT')
        nextState=1
    elif nowState==1 and input=="/":
        stateList.append('DIV')
        nextState=1
    elif nowState==1 and input=="=":
        stateList.append('ASSIGN')
        nextState=1
    elif nowState==1 and input==";":
        stateList.append('SEMICN')
        nextState=1
    elif nowState==1 and input==",":
        stateList.append('COMMA')
        nextState=1
    elif nowState==1 and input=="(":
        stateList.append('LPARENT')
        nextState=1
    elif nowState==1 and input==")":
        stateList.append('RPARENT')
        nextState=1
    elif nowState==1 and input=="[":
        stateList.append('LBRACK')
        nextState=1
    elif nowState==1 and input=="]":
        stateList.append('RBRACK')
        nextState=1
        '''
    elif nowState==1 and input=="\"":
        stateList.append('PHASE')
        nextState=1
        '''
    elif nowState==1 and input==":":
        stateList.append('COLON')
        nextState=1


    # 第二层的计算 非终结
    elif nowState==2 and (isChar(input)or isNum(input)):
        tempStr += input
        nextState=2
    elif nowState==4 and isNum(input):
        tempStr += input
        nextState=4
    elif nowState == 1 and input == "\"":
        stateList.append('PHASE')
        nextState = 6

    # 第二层计算终结
    elif nowState==2 and (isChar(input)==False and isNum(input)==False):
        stateList.append('CHARCON')
        stateList.append(tempStr)
        tempStr=''
        nowState=1
        nextState,tempStr=stateChange(nowState,input,stateList,tempStr)
    elif nowState==4 and isNum(input)==False:
        stateList.append('INTCON')
        stateList.append(int(tempStr))
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    elif nowState==8 and input=="=":
        stateList.append('LTOE')
        nextState=1
    elif nowState==8 and input!="=":
        stateList.append('LSS')
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    elif nowState==11 and input=="=":
        stateList.append('GTOE')
        nextState=1
    elif nowState==11 and input!="=":
        stateList.append('GRE')
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    elif nowState==6 and input=="\"":
        stateList.append('STRCON')
        stateList.append(tempStr)
        stateList.append('PHASE')
        tempStr=''
        nextState=1
    elif nowState==6 and input!="\"":
        tempStr+=input
        nextState=6
    else:
        print('unable to match')
        print(input)
        nextState = 1
    # 其他情况的处理           设定为不处理
    '''
    else :
        print('unable to match')
        print(input)
        stateList.append(input)
        nextState=1
    '''


    return nextState,tempStr

'''
strMatch
'''
def strMatch(input:str):
    stateList=list()
    nowState=1
    tempStr=''
    for i in range(len(input)):
        inputC=input[i]
        nowState,tempStr=stateChange(nowState, str(inputC), stateList, tempStr)
    return stateList

'''
strClean 该函数处理以下问题
{'name': '标识符' , 'class': 'IDENFR'},
{'name': '字符常量', 'class': 'CHARCON'},
{'name': '字符串', 'class': 'STRCON'},
1.将STRCON从CHARCON中分出来
2.将IDENFR从CHARCON中分出来
'''
def strClean(input:list):
    input.append('')
    input.append('')

    for i in range(len(input)-2):
        if input[i]=='CHARCON':
            if input[i+1]=='const':
                input[i] == 'IDENFR'
                input[i+1]='CONSTTK'
                i-=1
            if input[i+1]=='int':
                input[i] == 'IDENFR'
                input[i+1]='INTTK'
                i-=1
            if input[i+1]=='if':
                input[i] == 'IDENFR'
                input[i+1]='IFTK'
                i-=1
            if input[i+1]=='else':
                input[i] == 'IDENFR'
                input[i+1]='ELSETK'
                i-=1
            if input[i+1]=='do':
                input[i] == 'IDENFR'
                input[i+1]='DOTK'
                i-=1
            if input[i+1]=='while':
                input[i] == 'IDENFR'
                input[i+1]='WHILETK'
                i-=1
            if input[i+1]=='for':
                input[i] == 'IDENFR'
                input[i+1]='FORTK'
                i-=1
            if input[i+1]=='scanf':
                input[i] == 'IDENFR'
                input[i+1]='SCANFTK'
                i-=1

    del input[len(input) - 1]
    del input[len(input) - 1]

    return input

'''
readFile 读取文件 以str list的形式输出
'''
def readFile(address=r"C:\Users\leilu\Desktop\input.txt"):
    with open(address, encoding='utf-8') as file:
        data = file.readlines()
        print(data)

    file.close()

    for i in range(len(data)):
        print(data[i])
    return data

'''
writeFile 书写文件 以str list的形式输出
'''
def writeFile(data:list,address=r"C:\Users\leilu\Desktop\output.txt"):
    with open(address, "w") as file:
        for i in range(len(data)):
            file.write(data[i])
            file.write('\r\n')
            print(data[i])

    file.close()

'''
handle 将以上的函数整合为可用
'''
def handle():
    data=readFile()
    output=list()
    for i in range(len(data)):
        tempStr=data[i]
        tempOut=strMatch(tempStr)
        tempOut=strClean(tempOut)
        tempSave=''
        for j in range(len(tempOut)):
            tempSave+=('['+str(tempOut[j])+']')
        output.append(str(tempSave))
    writeFile(output)


if __name__ == '__main__':
    matchList=[
        #抽象类型
        {'name':'标识符','class':'IDENFR'},
        {'name': '整型常量', 'class': 'INTCON'},
        {'name': '字符常量', 'class': 'CHARCON'},
        {'name': '字符串', 'class': 'STRCON'},

        # 字符常量转标识符
        {'name': 'const', 'class': 'CONSTTK'},
        {'name': 'int', 'class': 'INTTK'},
        {'name': 'if', 'class': 'IFTK'},
        {'name': 'else', 'class': 'ELSETK'},
        {'name': 'do', 'class': 'DOTK'},
        {'name': 'while', 'class': 'WHILETK'},
        {'name': 'for', 'class': 'FORTK'},
        {'name': 'scanf', 'class': 'SCANFTK'},

        # 单符号
        {'name': '-', 'class': 'MINU'},
        {'name': '* ', 'class': 'MULT'},
        {'name': '/ ', 'class': 'DIV'},
        {'name': '<', 'class': 'LSS'},
        {'name': '>', 'class': 'GRE'},
        {'name': '=', 'class': 'ASSIGN'},
        {'name': ';', 'class': 'SEMICN'},
        {'name': ',', 'class': 'COMMA'},
        {'name': '(', 'class': 'LPARENT'},
        {'name': ')', 'class': 'RPARENT'},
        {'name': '[', 'class': 'LBRACK'},

        #双符号
        {'name': '<=', 'class': 'LEQ'},
    ]
    handle()
'''
实验五 11.21 软件sy2001 雷裕庭开始编写
11.24编写完成
'''

'''
isChar 判断是否为字符
'''


def isChar(input):
    input = str(input)
    if ("Z" >= input >= "A") or ("z" >= input >= "a"):
        return True
    return False


'''
isNum 判断是否为数字
'''


def isNum(input):
    input = str(input)
    if "9" >= input >= "0":
        return True
    return False


'''
stateChange 用于基于 输入状态 下一个字符的类型 返回下一个状态
'''


def stateChange(nowState: int, input: str, stateList: list, tempStr: str):
    # 多层处理
    print('nowState    input    tempStr')
    print(nowState, '          ', input, '         ', tempStr)
    if nowState == 1 and input == '':
        nextState = 1
    elif nowState == 1 and input == ' ':
        nextState = 1
    elif nowState == 1 and input == '\n':
        nextState = 1
    elif nowState == 1 and input is None:
        nextState = 1
    elif nowState == 1 and isChar(input):
        tempStr += input
        nextState = 2
    elif nowState == 1 and isNum(input):
        tempStr += input
        nextState = 4
    elif nowState == 1 and input == "<":
        nextState = 8
    elif nowState == 1 and input == ">":
        nextState = 11
    elif nowState == 1 and input == "!":
        nextState = 20
    elif nowState == 1 and input == "=":
        nextState = 21

    # 单一符号处理
    elif nowState == 1 and input == "-":
        stateList.append('MINU')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "+":
        stateList.append('PLUS')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "*":
        stateList.append('MULT')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "/":
        stateList.append('DIV')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == ";":
        stateList.append('SEMICN')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == ",":
        stateList.append('COMMA')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "(":
        stateList.append('LPARENT')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == ")":
        stateList.append('RPARENT')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "[":
        stateList.append('LBRACK')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "]":
        stateList.append('RBRACK')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "{":
        stateList.append('LBRACK')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == "}":
        stateList.append('RBRACK')
        stateList.append(input)
        nextState = 1
    elif nowState == 1 and input == ":":
        stateList.append('COLON')
        stateList.append(input)
        nextState = 1

    # 第二层的计算 非终结
    elif nowState == 2 and (isChar(input) or isNum(input)):
        tempStr += input
        nextState = 2
    elif nowState == 4 and isNum(input):
        tempStr += input
        nextState = 4
    elif nowState == 1 and input == "\"":
        nextState = 6
    elif nowState == 1 and input == "'":
        nextState = 30

    # 第二层计算终结
    elif nowState == 2 and (isChar(input) == False and isNum(input) == False):
        stateList.append('IDENFR')
        stateList.append(tempStr)
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    elif nowState == 4 and isNum(input) == False:
        stateList.append('INTCON')
        stateList.append(int(tempStr))
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
        '''
                "<":nextState=8
                ">":nextState=11
                "!":nextState=20
                "=":nextState=21
                 " :nextState=6
                 ' :nextState=30
        '''
    elif nowState == 8 and input == "=":
        stateList.append('LEQ')
        stateList.append('<=')
        nextState = 1
    elif nowState == 8 and input != "=":
        stateList.append('LSS')
        stateList.append('<')
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    elif nowState == 11 and input == "=":
        stateList.append('GTOE')
        stateList.append('>=')
        nextState = 1
    elif nowState == 11 and input != "=":
        stateList.append('GRE')
        stateList.append('>')
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    elif nowState == 6 and input == "\"":
        stateList.append('STRCON')
        stateList.append(tempStr)
        tempStr = ''
        nextState = 1
    elif nowState == 6 and input != "\"":
        tempStr += input
        nextState = 6

    elif nowState == 30 and input == "'":
        nextState = 1
    elif nowState == 30 and input != "'":
        stateList.append('CHARCON')
        stateList.append(input)
        nextState = 30

    elif nowState == 21 and input == "=":
        stateList.append('EQL')
        stateList.append('==')
        nextState = 1
    elif nowState == 21 and input != "=":
        stateList.append('ASSIGN')
        stateList.append('=')
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)

    elif nowState == 20 and input == "=":
        stateList.append('NEQ')
        stateList.append('!=')
        nextState = 1
    elif nowState == 20 and input != "=":
        stateList.append('WRONG')
        stateList.append('!')
        tempStr = ''
        nowState = 1
        nextState, tempStr = stateChange(nowState, input, stateList, tempStr)
    # 编译不能识别处理
    else:
        print('unable to match')
        print(input)
        stateList.append('WRONG')
        stateList.append(input)
        nextState = 1
    # 另一种处理方法       不处理
    '''
    else :
        print('unable to match')
        print(input)
        stateList.append(input)
        nextState=1
    '''
    return nextState, tempStr


'''
strMatch
'''


def strMatch(input: str):
    print('开始识别     按行识别')
    stateList = list()
    nowState = 1
    tempStr = ''
    for i in range(len(input)):
        inputC = input[i]
        nowState, tempStr = stateChange(nowState, str(inputC), stateList, tempStr)
    return stateList


'''
strClean 该函数处理以下问题
{'name': '标识符' , 'class': 'IDENFR'},
{'name': '字符常量', 'class': 'IDENFR'},
{'name': '字符串', 'class': 'STRCON'},
1.将STRCON从IDENFR中分出来
2.将IDENFR从IDENFR中分出来
'''


def strClean(input: list):
    print('清理IDENFR')
    input.append('')
    input.append('')
    for i in range(len(input) - 2):
        if input[i] == 'IDENFR':
            print(input[i + 1])
            if input[i + 1] == 'const':
                input[i] = 'CONSTTK'
                i -= 1
            if input[i + 1] == 'int':
                input[i] = 'INTTK'
                i -= 1
            if input[i + 1] == 'char':
                input[i] = 'CHARTK'
                i -= 1
            if input[i + 1] == 'void':
                input[i] = 'VOIDTK'
                i -= 1
            if input[i + 1] == 'main':
                input[i] = 'MAINTK'
                i -= 1
            if input[i + 1] == 'if':
                input[i] = 'IFTK'
                i -= 1
            if input[i + 1] == 'else':
                input[i] = 'ELSETK'
                i -= 1
            if input[i + 1] == 'do':
                input[i] = 'DOTK'
                i -= 1
            if input[i + 1] == 'while':
                input[i] = 'WHILETK'
                i -= 1
            if input[i + 1] == 'for':
                input[i] = 'FORTK'
                i -= 1
            if input[i + 1] == 'scanf':
                input[i] = 'SCANFTK'
                i -= 1
            if input[i + 1] == 'printf':
                input[i] = 'PRINTFTK'
                i -= 1
            if input[i + 1] == 'return':
                input[i] = 'RETURNTK'
                i -= 1

    del input[len(input) - 1]
    del input[len(input) - 1]

    return input


'''
readFile 读取文件 以str list的形式输出
'''


def readFile(address=r"C:\Users\leilu\Desktop\testfile.txt"):
    print("读取文件")
    with open(address, encoding='utf-8') as file:
        data = file.readlines()
    file.close()

    for i in range(len(data)):
        print(data[i])

    return data


'''
writeFile 书写文件 以str list的形式输出
'''


def writeFile(data: list, address=r"C:\Users\leilu\Desktop\output.txt"):
    print("写入文件")
    with open(address, "w") as file:
        for i in range(len(data)):
            for j in range(len(data[i]) // 2):
                file.write(str(data[i][j * 2] + " " + data[i][j * 2 + 1]))
                file.write('\n')
                print(str(data[i][j * 2] + " " + data[i][j * 2 + 1]))
    file.close()


'''
handle 将以上的函数整合为可用
'''


def handle():
    data = readFile()
    output = list()
    for i in range(len(data)):
        tempStr = data[i]
        tempOut = strMatch(tempStr)
        tempOut = strClean(tempOut)
        tempSave = list()
        for j in range(len(tempOut)):
            tempSave.append(str(tempOut[j]))
        output.append(tempSave)
    writeFile(output)


def compare(address1=r"C:\Users\leilu\Desktop\output.txt", address2=r"C:\Users\leilu\Desktop\outExample.txt"):
    print("下面运行检验程序")
    aList = readFile(address1)
    bList = readFile(address2)

    #逐行检验
    print(len(aList),len(bList))
    for i in range(min(len(aList),len(bList))):
        print(aList[i],bList[i],aList[i]==bList[i])
    if (aList == bList):
        print("经过检验，编译结果准确无误")
    else:
        print("经过检验，编译结果有误")
    return aList == bList


if __name__ == '__main__':
    handle()
    compare()

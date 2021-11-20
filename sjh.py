import sys
import os
from time import *
import copy
# 미로찾기 알고리즘
# 배열용 문제
class C_THESEUS:
    x = 0
    y = 0
    hX = 0
    hY = 0

def clear():
    os.system('cls')

def printMaze(lst):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            print(lst[i][j],end=' ')
        print()

def setMap(lst):
    temp = list(lst)
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == '1':
                temp[i][j] = ('■')
            elif lst[i][j] == '0':
                temp[i][j] = (' ')
            elif lst[i][j] == '3':
                temp[i][j] = ('♥')
            elif lst[i][j] == '2':
                temp[i][j] = 'Ω'
    return temp

def findTheseus(lst):
    #함수로 빼기
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == 'Ω':
                C_THESEUS.x = i
                C_THESEUS.y = j
            if lst[i][j] == '♥':
                C_THESEUS.hX = i
                C_THESEUS.hY = j
    return C_THESEUS

def isNeedPOP(lst):
    nCount = 0
    dir = [0,0,0,0]
    if lst[C_THESEUS.x][C_THESEUS.y+1] == '1' or lst[C_THESEUS.x][C_THESEUS.y+1] == '5':
        nCount+=1
        dir[0] = 1
    if lst[C_THESEUS.x+1][C_THESEUS.y] == '1' or lst[C_THESEUS.x+1][C_THESEUS.y] == '5' :
        nCount+=1
        dir[1] = 1
    if lst[C_THESEUS.x][C_THESEUS.y-1] == '1' or lst[C_THESEUS.x][C_THESEUS.y-1] == '5':
        nCount+=1
        dir[2] = 1
    if lst[C_THESEUS.x-1][C_THESEUS.y] == '1' or lst[C_THESEUS.x-1][C_THESEUS.y] == '5':
        nCount+=1
        dir[3] = 1
    if nCount < 3:
        if lst[C_THESEUS.x][C_THESEUS.y+1] == '4':
            nCount+=1
            dir[0] = 0
        if lst[C_THESEUS.x+1][C_THESEUS.y] == '4':
            nCount+=1
            dir[1] = 0
        if lst[C_THESEUS.x][C_THESEUS.y-1] == '4':
            nCount+=1
            dir[2] = 0
        if lst[C_THESEUS.x-1][C_THESEUS.y] == '4':
            nCount+=1
            dir[3] = 0
    nReturnIndex = 0
    try:
        nReturnIndex = dir.index(0)
    except:
        pass

    if nCount >= 3:
        return True,nReturnIndex
    return False,nReturnIndex

def POP(lst,printMap,nIndex):
    if nIndex == 0 :
        printMap[C_THESEUS.x][C_THESEUS.y] = ' '
        lst[C_THESEUS.x][C_THESEUS.y] = '5'
        C_THESEUS.y += 1
        printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'
    elif nIndex == 1:
        printMap[C_THESEUS.x][C_THESEUS.y] = ' '
        lst[C_THESEUS.x][C_THESEUS.y] = '5'
        C_THESEUS.x +=1
        printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'
    elif nIndex == 2:
        printMap[C_THESEUS.x][C_THESEUS.y] = ' '
        lst[C_THESEUS.x][C_THESEUS.y] = '5'
        C_THESEUS.y -= 1
        printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'

    elif nIndex == 3:
        printMap[C_THESEUS.x][C_THESEUS.y] = ' '
        lst[C_THESEUS.x][C_THESEUS.y] = '5'
        C_THESEUS.x -= 1
        printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'

def findPath(printMap,lst):
    isEscape = False
    Theseus = 2
    C_THESEUS.x = 0
    C_THESEUS.y = 0
    changeDir = 1
    nRecentDirection = 0
    while(not isEscape):
        
        if lst[C_THESEUS.x][C_THESEUS.y] == '3':
            break
        if C_THESEUS.x == 0 and C_THESEUS.y == 0:
            findTheseus(printMap)
        #동작코드
        if lst[C_THESEUS.x][C_THESEUS.y + 1] == '0':
            printMap[C_THESEUS.x][C_THESEUS.y] = ' '
            lst[C_THESEUS.x][C_THESEUS.y] = '4'
            C_THESEUS.y += 1
            printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'
        
        elif lst[C_THESEUS.x + 1][C_THESEUS.y] == '0':
            printMap[C_THESEUS.x][C_THESEUS.y] = ' '
            lst[C_THESEUS.x][C_THESEUS.y] = '4'
            C_THESEUS.x +=1
            printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'
        
        elif lst[C_THESEUS.x][C_THESEUS.y - 1] == '0':
            printMap[C_THESEUS.x][C_THESEUS.y] = ' '
            lst[C_THESEUS.x][C_THESEUS.y] = '4'
            C_THESEUS.y -= 1
            printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'

        elif lst[C_THESEUS.x - 1][C_THESEUS.y] == '0':
            printMap[C_THESEUS.x][C_THESEUS.y] = ' '
            lst[C_THESEUS.x][C_THESEUS.y] = '4'
            C_THESEUS.x -= 1
            printMap[C_THESEUS.x][C_THESEUS.y] = 'Ω'

        else:
            isPOP = isNeedPOP(lst)
            if isPOP[0]:
                POP(lst,printMap,isPOP[1])
        printMaze(printMap)
        sleep(0.3)
        clear()    

def main():
    lst = [[0 for _ in range(10)] for i in range(10)]
    lst[0] = [1,1,1,1,1,1,1,1,1,1]
    lst[1] = [1,0,0,0,0,0,0,0,3,1]
    lst[2] = [1,0,1,1,1,1,1,1,1,1]
    lst[3] = [1,0,1,0,0,0,0,0,0,1]
    lst[4] = [1,0,1,0,1,0,1,1,1,1]
    lst[5] = [1,0,0,0,1,0,0,0,0,1]
    lst[6] = [1,1,1,1,1,1,1,1,0,1]
    lst[7] = [1,0,0,0,0,0,1,1,0,1]
    lst[8] = [1,2,1,0,1,0,0,0,0,1]
    lst[9] = [1,1,1,1,1,1,1,1,1,1]

    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j] = str(lst[i][j])
    
    printMap = copy.deepcopy(lst)
    
    printMap = setMap(printMap)

    printMaze(printMap)
    findPath(printMap,lst)

    print("미로찾기 완료!")

main()
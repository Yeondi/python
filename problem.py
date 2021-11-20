import random
import math
from setup import *

class Problem(Setup): #상속
    def __init__(self) -> None:
        super().__init__() # call superClass
        self._solution = []
        self._value = 0
        self._numEval = 0
        self._pFileName = 0 # file name
        self._bestSolutionData = 0 # bestSolution data through many experimental
        self._objData = 0 # its objective Value
        self._avgMinObjValue = 0.0 # average Number of Experience Data
        self._limitEval = 0 # average iteration when the best solution appears
        self._expNumEval = 0
        self._sumExpNumEval = 0
        self._tempAvg = 0.0
    
    def getNumEval(self):
        return self._numEval
    
    def getSolution(self):
        return self._solution
    
    def getValue(self):
        return self._value

    def setNumEval(self, cnt=0):
        self._numEval += cnt

    def getExpNameData(self):         # 혹시모를 get을 사용할 경우를 위한 get
        return self._pFileName

    def getBestSolutionData(self):
        return self._bestSolutionData

    def getObjData(self):
        return self._objData

    def getAvgMinObjValue(self):
        return self._avgMinObjValue

    def getExpNumEval(self):
        return self._expNumEval

    def getSumExpNumEval(self):
        return self._sumExpNumEval

    def storeResult(self,solution,value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Average objective value: {0:.3f}".format(self._avgMinObjValue))
        print("Average number of evalutations: {0:,}".format(self._expNumEval))
        print()
        print("Best solution found:")
        print("({0:.3f}, {1:.3f}, {2:.3f}, {3:.3f})".format(self._bestSolutionData[0],self._bestSolutionData[1],self._bestSolutionData[2],self._bestSolutionData[3]))
        # print("Best value: {0:.3f}".format(self._))
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))

    def setVariables(self,parameters):
        self._pFileName = parameters['pFileName']
        self._limitEval = parameters['limitEval']
        


class Numeric(Problem):
    def __init__(self) -> None:
        super().__init__()
        self._delta= self.getDeltaInSetup() # 기존 superClass call로 이렇게
        self._domain=[]
        self._expression = ''
    #   gradient descent
        self._dx=0.01
        self._alpha = self.getAlphaInSetup() # 위와 같음
    def getDx(self):
        return self._dx
    def getAlpha(self):
        return self._alpha

    def takeStep(self,x,y):
        grad = self.gradient(x,y)
        xCopy = x[:]
        for i in range(len(xCopy)):
            xCopy[i] = xCopy[i] - self._alpha - grad[i]
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x

    def gradient(self,x,y):
        grad = []
        for i in range(len(x)):
            xCopyH = x[:]
            xCopyH[i] += self._dx
            g = (self.evaluate(xCopyH) - y) / self._dx
            grad.append(g)
        return grad

    def isLegal(self,xCopy): #값을 벗어나는가?
        for i in range(len(xCopy)):
            if self._dx > xCopy[i]:
                return False
        return True

    def getDelta(self):
        return self._delta

    def setDelta(self,delta):
        self._delta = delta

    def setVariables(self,parameters):
        # import os
        # dataFile = input('Enter the file name of a function: ')
        # fileDir = 'C:/Users/atlan/source/repos/PythonApplication1/PythonApplication1/HW06/problem'
        # filePath = os.path.join(fileDir,dataFile)

        Problem.setVariables(self,parameters)
        infile = open(self._pFileName,'r')
        # self._expression = infile.readline()

        varNames = []
        low = []
        up = []

        #여기 수정
        for idx,line in enumerate(infile):
            if idx == 0:
                self._expression = line.strip()
                # self._expression = self._expression.strip()
            else:    
                data = line.strip().split(',')
                varNames.append(data[0])
                low.append(int(data[1]))
                up.append(int(data[2]))

        self._domain = [varNames,low,up]

    def randomInit(self): # Return a random initial point as a list
        ###
        # type이 list인 init에 최하~최대값을 랜덤으로 설정?
        domain = self._domain
        low,up = domain[1],domain[2]

        init=[]

        for i in range(0,len(low)):
            init.append(random.uniform(low[i],up[i])) # 그걸 리스트에 꽂아줌
    

        ###

        return init    # list of values

    def evaluate(self,current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        # global NumEval
    
        self._numEval += 1
        expr = self._expression     # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain: [varNames, low, up]
        for i in range(len(varNames)):
            for j in range(len(varNames[i])):
                assignment = varNames[i] + '=' + str(current[j])
            # assignment.append(varNames[i])
            # assignment.append(str(current[i]))
                exec(assignment)
        return eval(expr)

    def mutate(self,current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain       # [VarNames, low, up]
        l = domain[1][i]     # Lower bound of i-th
        u = domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def describe(self):
        self.describeProblem(self)
        

    def describeProblem(self,p):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        varNames = self._domain[0] # p[1] is domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 

    def displayResult(self,solution, minimum):
        print()
        print("Solution found:")
        print(self.coordinate(solution))  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(minimum))
        print()
        print("Total number of evaluations: {0:,}".format(self.getNumEval()))

    def coordinate(self,solution):
        c = [round(value, 3) for value in solution]
        return tuple(c)  # Convert the list to a tuple

    def randomMutant(self,current):
        ###
        i = random.randrange(0,len(self._domain[0])) # numeric.py에 쓰인 리스트 길이 재는방식 사용 / 0부터 i번째의 랜덤값
        bDeltaRandom = random.randrange(0,2) # 0~1이 나오고 0이면 음수 1이면 양수
        DELTA = self.getDelta()
        if bDeltaRandom == 0:
            d = -DELTA
        elif bDeltaRandom == 1:
            d = DELTA

        return self.mutate(current, i, d)

    def mutants(self,current):
        ###
        d = self.getDelta()
        neighbors = []
        loop = len(self._domain) - 1
        num = 0
        for i in range(loop):
            for j in range(loop):
                neighbors.append(self.mutate(current,num,d))
                d *= -1
            num+=1
        return neighbors
    
    def storeExpResult(self,results):
        # results = 
            # bestSolution = self._bestSolutionData,
            # bestMinimum = self._objData,
            # avgMinimum = self._avgMinObjValue,
            # avgNumEval = self._expNumEval,
            # sumOfNumEval = self._sumExpNumEval,
            # avgWhen = self._limitEval
        self._bestSolutionData = results[0]
        self._objData = results[1]
        self._avgMinObjValue = results[2]
        self._expNumEval = results[3]
        self._sumExpNumEval = results[4]
        # self._limitEval = results[5]


class Tsp(Problem):
    def __init__(self) -> None:
        super().__init__()
        self._numCities = 0
        self._locations=[]
        self._table=[]

    def getNumCities(self):
        return self._numCities
    
    #   gradient descent
    def setVariables(self):
        import os
        dataFile = input('Enter the file name of a TSP: ')
        fileDir = 'C:/Users/atlan/source/repos/PythonApplication1/PythonApplication1/HW06/problem'
        filePath = os.path.join(fileDir,dataFile)
        
        infile = open(filePath, 'r')
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self._locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        self._numCities = self._locations[0]
        self._locations.remove(self._numCities)
        self._table = self.calcDistanceTable(self._numCities, self._locations)


        return self._numCities, self._locations, self._table

    def calcDistanceTable(self,numCities, locations):
        ###
        #Euclidian distance number of cities / locations (coordinate)
        # sqrt((x2-x1)^2 + (y2-y1)^2)
        table = [[0 for column in range(numCities)] for row in range(numCities)] # table 2차원 배열을 city의 개수에 따라서 0으로 초기화
        for i in range(numCities): # i번지를 잡고 j번지들과 비교하기위함
            x1 = locations[i][0] # (x1,y1) , (x2,y2)의 비교라서
            y1 = locations[i][1]
            for j in range(numCities):
                x2 = locations[j][0]
                y2 = locations[j][1]
                table[i][j] = round(math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2)),1) #유클리디안 거리 공식은 sqrt((x2-x1)^2 + (y2-y1)^2)이고
                                                                                #제곱을 위해 math.pow , 소수점 한자리로 끊어주기위해 round사용
        ###
        return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self,current):
        # print('current : ',current)
        self._numEval+=1
        departure = current[0] # 첫 시작인덱스
        cost = 0 # cost 초기화
        for j in range(1,len(current)): # 예 2-0-1-3이면 -에 해당하는 edge의 코스트를 감안해서 계산해야함.
            
            cost += self._table[departure][current[j]] # inputFile에 대한 정보가 담겨있음. i.e.) tsp50.txt
            departure = current[j] # 위 예를 빌리자면, 2를 한 후 다음은 0번지에서 시작해야함
    
        return cost

    def inversion(self,current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def describeProblem(self,p):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def displayResult(self,solution, minimum):
        print()
        print("Best order of visits:")
        self.tenPerRow(solution)       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(minimum)))
        print()
        print("Total number of evaluations: {0:,}".format(self.getNumEval()))

    def tenPerRow(self,solution):
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

    def mutants(self,current): # Inversion only
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def randomMutant(self,current): # Inversion only
        while True:
            i, j = sorted([random.randrange(self.getNumCities()) for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
            break
        try:
            return curCopy
        except(UnboundLocalError):
            curCopy = self.inversion(current, i, j)
            return curCopy

    def mutate(self,current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain       # [VarNames, low, up]
        l = domain[1][i]     # Lower bound of i-th
        u = domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy
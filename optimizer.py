# steepest : run / bestOf 
# fc : displaySetting / run
# gd : =same
from setup import * 
import random
import math
from plot import *

class Optimizer(Setup): # 새로운 superClass
    def __init__(self):
        super().__init__()
        self._pType = 0
        self._numExp = 0
        self._loopCount = 0
        self._numRestart = 0

    def setLoopCount(self):
        self._loopCount+=1

    def setNumExp(self,numExp):
        self._numExp = numExp
    
    def getNumExp(self):
        return self._numExp

    def displaySetting(self):
        print("common information") # 오버라이딩용
        #limitStuck

    def run(self,p): # 상속용
        pass

    def getWhenBestFound(self):
        pass

    def setVariables(self,parameters):
        super().setVariables(parameters)
        self._pType = parameters['pType'] #값 세팅
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']
        self._limitStuck = parameters['limitStuck']
        self._limitNumEval = parameters['limitEval']

    def displayNumExp(self):
        print()
        print("Number of experiments: {0:}".format(self._numExp))
        

class HillClimbing(Optimizer):
    def __init__(self):
        super().__init__() # superclass initializing
        # Optimizer.__init__(self) # superClass가 두개라서 두번째 부모는 직접 저렇게 접근해야함
        self._delta = self.getDelta() #상속받은 값
        self._alpha = self.getAlpha()
        self._limitStuck = 0
        self._numRestart = 0


    def setVariables(self,parameters):
        Optimizer.setVariables(self,parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

        
    def displaySetting(self):
        if self._numRestart == 1:
            print("Number of random restarts:",self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2<= self._aType <= 3:
            print("Max evaluations with no improvement: {0:,}".format(self._limitStuck))
        #limitStuck
    
    def getAType(self):
        return self._aType 
    
    def getNumExp(self):
        return self._numExp



    def randomRestart(self,p):
        i = 1
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()
        while i < self._numRestart:
            self.run(p)
            newSolution = p.getSolution()
            newMinimum = p.getValue()
            numEval = p.getNumEval()
            if newMinimum < bestMinimum:
                bestSolution = newSolution
                bestMinimum = newMinimum
            i+=1
        p.storeResult(bestSolution,bestMinimum)

    def run(self,p):
        pass

class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        print()
        print("Number of random restarts: {0:}".format(self._loopCount))
        print()
        print("Mutation step size:", self._delta) # 상속받은 delta값
        print("Max evaluations with no improvement: {0:} iterations".format(self._limitStuck))
    
    def run(self,p): 
        # p == problem # 기존 setVariables
        current = p.randomInit()   # 'current' is a list of city ids 
        valueC = p.evaluate(current)
        f=open('steepest.txt','w')
        
        while True: 
            neighbors = p.mutants(current)
            (successor, valueS) = self.bestOf(neighbors,p)
            f.write(str(round(valueC,1))+'\n')
            if valueS > valueC: # valueC가 더 작거나 같아야함
                break
            else:#아닐경우
                if successor != 0:
                    current = successor
                valueC = valueS
            p.storeResult(current,valueC)
            f.close()
            return current, valueC

    def bestOf(self,neighbors, p):
    ###
        loop = len(neighbors)
        eval1 = []
        for i in range(loop):
            eval1.append(p.evaluate(neighbors[i]))
    
        best = 0
        min = eval1[0]
        bestValue = 0.0
        for i in range(1,loop):
            if min > eval1[i]:
                min = eval1[i]
                best = neighbors[i]
                bestValue = eval1[i]
        return best, bestValue  

class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        print()
        print("Number of random restarts: {0:}".format(None))
        print()
        print("Mutation step size:", self._delta)
        print("Max evaluations with no improvement: {0:} iterations".format(self._limitStuck))
    
    def run(self,p):
        current = p.randomInit()   # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < LIMIT_STUCK:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
        p.storeResult(current,valueC)


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        print()
        print("Number of random restarts: {0:}".format(None))
        print()
        print("Mutation step size:", self._delta)
        print("Max evaluations with no improvement: {0:} iterations".format(self._limitStuck))
    
    def run(self,p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)

        nextP = p.takeStep(current,self._alpha) # derivative, alpha
        nextN = p.evaluate(nextP)

        p.storeResult(nextP,nextN) # 새로만들기 problem.py

class Stochastic(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self,p): 
        # p == problem # 기존 setVariables
        current = p.randomInit()   # 'current' is a list of city ids 
        valueC = p.evaluate(current)

        i=0

        while i< self._limitStuck:
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors,p)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i=0
            else:
                i+=1

        p.storeResult(current,valueC)

    def stochasticBest(self, neighbors, p):
        # Smaller valuse are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

class MetaHeuristics(Optimizer): # limitEval관련 값
    def __init__(self):
        super().__init__()
        self._limitEval = 0
        self._whenBestFound = 0

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self._whenBestFound

    def run(self, p):
        pass

    def displaySetting(self):
        super().displaySetting()
        print("Number of evaluations until termination: {0:,}".format(self._limitEval))

class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        super().__init__()
        self._numSample = 100
    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing")
        print()
        super().displaySetting()

    def run(self,p):
        current = p.randomInit()   # 'current' is a list of values
        valueC = p.evaluate(current)
        best,valueBest = current,valueC
        i=0
        whenBestFound = i-1
        t = self.initTemp(p)
        while True:
            t = self.tSchedule(t)
            if t==0 or i == self._limitEval:
                break
            neighbor = p.randomMutant(current)
            valueN = p.evaluate(neighbor)
            i+= 1
        p.storeResult(current,valueC)

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numRestart):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numRestart  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

    def getWhenBestFound(self):
        return self._whenBestFound

class GA(MetaHeuristics):
    def __init__(self):
        super().__init__()
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation
        self._resolution = 0
        

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        self._resolution = parameters['resolution']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        super().displaySetting()
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)

    def run(self,p):
        popSize = self._popSize
        pop = p.initializePop(popSize)
        # print('pop',pop)
        best = self.evalAndFindBest(pop,p)
        p.setValue(best[0])
        par1,par2 = self.selectParents(pop)

        newPop = []
        i=00
        while i < self._popSize:
            # print(i)
            par1,par2 = self.selectParents(pop)
            ch1,ch2 = p.crossover(par1,par2,self._pC)
            p.randomMutant(p.randomInit())
            newPop.extend([ch1,ch2])
            i+=2
            # print('newPop',newPop)
        

    def evalAndFindBest(self,pop,p):
        best = pop[0]
        p.evalInd(best)
        bestValue = best[0]
        ##
        self._whenBestFound+=1
        # print('best',best,'bestValue',bestValue)
        return best # 가장 작은 값 return?

    def selectParents(self,pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.binaryTournament(ind1,ind2)
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.binaryTournament(ind1,ind2)
        return par1,par2

    def selectTwo(self,pop):
        popCopy = pop[:]
        random.shuffle(popCopy)
        return popCopy[0],popCopy[1]

    def binaryTournament(self,ind1,ind2):
        if ind1[0] < ind2[0]:
            return ind1
        else:
            return ind2
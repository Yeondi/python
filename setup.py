# parent of Problem.py and Hillclimbing.py
LIMIT_STUCK = 100
class Setup: # 공통된 데이터
    def __init__(self):
        self._delta = 0.01
        self._alpha = 0.01
    def getDeltaInSetup(self):
        return self._delta
    def getAlphaInSetup(self):
        return self._alpha

        #솔직히 겹치는 부분이 생각보다 꽤 있는데, 그러면 Problem자체를 덮어도 될 정도라 이정도로 유지했습니다.

    # def evaluate(self,current):
    #     ## Evaluate the expression of 'p' after assigning
    #     ## the values of 'current' to the variables
    #     # global NumEval
    
    #     self._numEval += 1
    #     expr = self._expression     # p[0] is function expression
    #     varNames = self._domain[0]  # p[1] is domain: [varNames, low, up]
    #     for i in range(len(varNames)):
    #         for j in range(len(varNames[i])):
    #             assignment = varNames[i] + '=' + str(current[j])
    #         # assignment.append(varNames[i])
    #         # assignment.append(str(current[i]))
    #             exec(assignment)
    #     return eval(expr)

    # def evaluate(self,current):
    #     # print('current : ',current)
    #     self._numEval+=1
    #     departure = current[0] # 첫 시작인덱스
    #     cost = 0 # cost 초기화
    #     for j in range(1,len(current)): # 예 2-0-1-3이면 -에 해당하는 edge의 코스트를 감안해서 계산해야함.
            
    #         cost += self._table[departure][current[j]] # inputFile에 대한 정보가 담겨있음. i.e.) tsp50.txt
    #         departure = current[j] # 위 예를 빌리자면, 2를 한 후 다음은 0번지에서 시작해야함
    
    #     return cost
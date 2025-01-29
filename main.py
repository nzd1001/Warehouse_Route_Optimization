from algorithms.greedy import Greedy_Solver
from algorithms.aco import ACO_Solver
from algorithms.LS_SA import LS_LA_Solver
from algorithms.cp import CP_Solver
from algorithms.ip import IP_Solver
from algorithms.bb import BB_Solver
import random,math,json,time
from data.load_data import load_data_from_input,load_data_from_json,load_data_from_json2
class Ultimate_Solver:
    def __init__(self,data):
        self.data=data
    def solve(self):
        print('Choose your solver: ')
        print('\t 1. Branch and Bound')
        print('\t 2. CP ')
        print('\t 3. IP ')
        print('\t 4. Greedy ')
        print('\t 5. Local Search - Simulated Annealing ')
        print('\t 6. Ant Colony')
        choice= int(input())
        match choice:
            case 1:
                solver=BB_Solver(self.data)
            case 2:
                solver=CP_Solver(self.data)
            case 3:
                solver=IP_Solver(self.data)
            case 4:
                solver=Greedy_Solver(self.data)
            case 5:
                solver=LS_LA_Solver(self.data)
            case 6:
                solver=ACO_Solver(self.data)
            case _:
                return (None,None)
        ans,value=solver.solve()
        return (ans,value)
def main():
    #testcase=load_data_from_input() 
    testcase=load_data_from_json()
    solver=Ultimate_Solver(testcase)
    start=time.time()
    ans,value=solver.solve()
    end=time.time()
    if ans and value:
        print(ans)
        print(value)
        print('Time taken: ',end-start)
    else:
        print('Goodbye!')
if __name__=="__main__":
    main()
import math,random,json
from algorithms.greedy import Greedy_Solver
class LS_LA_Solver:
    def __init__(self,data,alpha=0.99,T=100,threshold=None):
        self.name='LS_SA'
        self.data=data
        self.alpha=alpha
        self.T=100
        if threshold!=None:
            self.threshold=threshold
        else: self.threshold=max(1000,int(2*10**6/self.data['shelf_num']))
    def initialization(self):#create initial solution by greedy
        solver=Greedy_Solver(self.data)
        ans=solver.solve()
        return (ans[0],ans[1])
    def calc_cost(self,path):#calculate the cost of a solution
        cost=0
        cost+=self.data['distance'][0][path[0]]
        for i in range(len(path)-1):
            cost+=self.data['distance'][path[i]][path[i+1]]
        cost+=self.data['distance'][path[-1]][0]
        return cost
    def is_valid(self,path):#check if a solution is valid or not(satisfy kpi or not)
        if not path:
            return False
        for p in range(len(self.data['kpi'])):
            total=sum([self.data['storage'][p][shelf] for shelf in path])
            if total-self.data['kpi'][p]<0:
                return False
        return True
    def make_neighbor(self,path,l):#make a neighbour of current solution
        other_shelf=list(set([i for i in range(1,self.data['shelf_num']+1)])-set(path))        
        neighbours=[]
        k=random.random()
        def replace():
            i=random.choice(other_shelf)
            index=random.choice([i for i in range(len(path))])
            path[index]=i
        def add_and_replace():
            new_s=random.choice(other_shelf)
            other_shelf.remove(new_s)
            path.append(new_s)
            i=random.choice(other_shelf)
            index=random.choice([i for i in range(len(path)-1)])
            path[index]=i
        def remove():
            index=random.choice([i for i in range(len(path))])
            path.pop(index)
        def three_opt():
            indexes=random.sample([i for i in range(len(path))],3)
            indexes.sort()
            i,j,k=tuple(indexes)
            new_path = path[:i] + path[j:k] + path[i:j] + path[k:]
            return new_path
        if len(path)<=1.25*l:
            if k<=0.25 and other_shelf:
                replace()
            elif k<=0.5 and len(other_shelf)>=2:
                add_and_replace()
            elif k<=0.75:
                remove()
            else:
                return three_opt()
            return path
        else:
            remove()
        return path
    """def three_opt_local_search(self,path):
        current_path=path[:]
        current_cost=self.calc_cost(path)
        better=True
        while better:
            better=False
            for i in range(0, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    for k in range(j + 1, len(path)):
                        # Create a new path by removing three edges and reconnecting
                        new_path = current_path[:i] + current_path[j:k] + current_path[i+1:j] + current_path[k+1:] + current_path[i:i+1] + current_path[k:k+1]
                        # Calculate the cost of the new path
                        new_cost = self.calc_cost(new_path)
                        # If the new path is better, update the best path
                        if new_cost < current_cost:
                            current_cost=new_cost
                            current_path=new_path[:]
                            better=True
              
        return current_path"""
    def two_opt_local_search(self,path):#2-opt local search
        def two_opt():
            current_path=path[:]
            better=True
            while better:
                better = False
                for i in range(0, len(path) - 2):
                    for j in range(i + 1, len(path)):
                        next_j=0 if j==len(current_path)-1 else current_path[j+1]
                        next_i=current_path[i+1]
                        delta_cost= - self.data['distance'][current_path[i]][next_i] - self.data['distance'][current_path[j]][next_j] + self.data['distance'][next_i][next_j] + self.data['distance'][current_path[i]][current_path[j]]
                        if delta_cost< 0:
                            two_opt_swap(current_path, i, j)
                            better = True
            return current_path
        def two_opt_swap(path, i, j):
            path[i+1:j+1] = reversed(path[i+1:j+1])  # Reverse the sub-tour between i and j
        local_optimum=two_opt()
        return local_optimum
    def solve(self):#main function to solve
        current_path,greedy_cost=self.initialization()#initalization
        l=len(current_path)
        iteration=0
        T=self.T
        #convergence_test=[]
        #convergence_test.append(greedy_cost)
        current_path=self.two_opt_local_search(current_path) #apply local search to initial solution
        current_cost=self.calc_cost(current_path)
        #convergence_test.append(current_cost)
        u=0 #this variable is for reheating
        best_path=current_path[:]
        best_cost=current_cost
        while iteration<self.threshold:
            new_path = self.make_neighbor(current_path[:],l)#create neighbour
            while not self.is_valid(new_path):#check if the neighbour is valid or not, if not continue creating neighbour until valid
                new_path = self.make_neighbor(current_path[:],l)
            new_path = self.two_opt_local_search(new_path)
            new_cost = self.calc_cost(new_path)
            delta_E = new_cost - current_cost
            if delta_E <= 0:  # New solution is better or equal
                current_path = new_path[:]
                current_cost = new_cost
                if delta_E<0:
                    u=0 #if find a better solution than the current one, reset u=0
                if new_cost < best_cost:
                    best_path = new_path[:]
                    best_cost = new_cost   
            else:  # New path is worse 
                p = math.exp(-delta_E/T)
                if random.random() < p:
                    current_path = new_path[:]
                    current_cost = new_cost
            T*=self.alpha
            iteration+=1
            #convergence_test.append(current_cost)
            u+=1
            if u==200: #increase T if cant find a better solution in 200 iter
                T*=20
                u=0
        return (best_path,best_cost)

import random
import math,json
class ACO_Solver:
    def __init__(self,data,alpha=1,beta=3,evar_p=0.3,Q=10,threshold=None):
        self.name='ACO'
        self.data=data
        self.node_num=self.data['shelf_num']+1 #shelf 0(the door) is also a node
        if threshold!=None:
            self.threshold=threshold
        else: self.threshold=int(200000/self.data['shelf_num'])
        self.alpha=alpha
        self.beta=beta
        self.evar_p=evar_p
        self.Q=Q
    def generate_ant(self):#create a number of ants
        ants=[i for i in (1,int(0.1*self.data['shelf_num'])+1,)]
        return ants
    def initialization(self):#initialize P and R
        P,R=dict(),dict()
        for i in range(self.node_num):
            for j in range(1,self.node_num):
                    if i!=j:
                        P[(i,j)]=self.heuristic(i,j)
                        R[(i,j)]=self.heuristic(i,j)
                    else:
                        P[(i,j)]=0
        return (P,R)
    def choose_next(self,current_shelf,prob,visited):#choose next shelf based on probability P
        pick_from=[]
        corresponding_p=[]
        for a in range(1,self.node_num):
            if not visited[a]:
                pick_from.append(a)
                corresponding_p.append(prob[(current_shelf,a)])
        chosen=random.choices(pick_from,weights=corresponding_p)[0]
        return chosen
    def heuristic(self,i,j):#the heuristic information
        if self.data['distance'][i][j]==0:
            return 0
        return 1/(self.data['distance'][i][j])
    def update_P(self,i,P,R,visited):#update probability
        denum=0
        for s in range(1,self.node_num):
            if not visited[s]:
                denum+=R[(i,s)]**self.alpha*self.heuristic(i,s)**self.beta
        for j in range(1,self.node_num):
            if not visited[j]:
                """ if denum==0:
                    P[(i,j)]=self.heuristic(i,j)
                else: """
                nume=R[(i,j)]**self.alpha*self.heuristic(i,j)**self.beta
                P[(i,j)]=nume/denum
            else:
                P[(i,j)]=0
    def solve(self):
        P,R=self.initialization()
        ants=self.generate_ant()
        best_path=None
        ultimate_min_cost=float('inf') #this is the best cost in all iteration
        ultimate_best_path=[] #this is the best path in all iteration
        convergence_test=[]
        for iteration in range(self.threshold):
            delta_R={(i,j):0 for j in range(1,self.node_num) for i in range(self.node_num)}
            for ant in ants:
                #delta_r={(i,j):0 for j in range(1,self.node_num) for i in range(1,self.node_num)}
                kpi=self.data['kpi'][:]
                visited=[False for _ in range(self.node_num)]
                visited_edge=[]
                path=[]
                visited[0]=True
                current_shelf=0                
                cost=0
                min_cost=float('inf') #this is the best cost in this iteration only
                best_path=[] #this is the best path in this iteration only
                while True:
                    if current_shelf==0 and iteration<20: #in the fisrt 20 iterations, go from 0 to other shelves with equal probability to increase exploration
                        for j in range(1,self.node_num):
                            P[(0,j)]=1/(self.node_num-1)
                    else:
                        self.update_P(current_shelf,P,R,visited) #update the P 
                    next_shelf=self.choose_next(current_shelf,P,visited) #choose next shelf based on P
                    visited_edge.append((current_shelf,next_shelf))
                    cost+=self.data['distance'][current_shelf][next_shelf]
                    current_shelf=next_shelf
                    path.append(current_shelf)
                    visited[current_shelf]=True
                    for product in range(len(kpi)):
                        kpi[product]-=min(kpi[product],self.data['storage'][product][current_shelf])
                    if all(a==0 for a in kpi):#reached goal
                        cost+=self.data['distance'][path[-1]][0]
                        if cost<min_cost:
                            min_cost=cost
                            best_path=path[:]
                            if min_cost<ultimate_min_cost:
                                ultimate_min_cost=min_cost
                                ultimate_best_path=best_path
                        break
                #update delta pheromonon on each visited egde of an ant
                for (i,j) in visited_edge:
                    delta_R[(i,j)]+=self.Q/cost
                    """ if i!=0:
                        delta_R[(j,i)]+=self.Q/cost
                    else:
                        delta_R[(0,path[-1])]+=self.Q/cost """
            #update the total pheromonon after the iteration
            for i in range(self.node_num):
                for j in range(1,self.node_num):
                    if i!=j:
                        R[(i,j)]=(1-self.evar_p)*R[(i,j)]+delta_R[(i,j)] 
                        if (i,j) in zip([0]+best_path[:-1],best_path):
                            R[(i,j)]+=0.5*self.Q/min_cost #update the pheromenon of the best path found in this iteration by EAS 
                            """ if i!=0:
                                R[(j,i)]+=0.5*self.Q/min_cost
                            else:
                                R[(0,best_path[-1])]+=0.5*self.Q/min_cost """
            #convergence_test.append(ultimate_min_cost)
        return (ultimate_best_path,ultimate_min_cost)
from ortools.linear_solver import pywraplp
import json
#Convention : the door is shelf 0
class IP_Solver():
    def __init__(self,data):
        self.data=data
        self.name='IP'
    def connected_edge(self,y,i): #this func return number of edges to i(predecessor) and number of edges from i(decessor)
        predecessor=0
        decessor=0
        for j in range(self.data['shelf_num']+1):
            decessor+=y[(i,j)]
            predecessor+=y[(j,i)]
        return (decessor,predecessor)
    def construct_path(self,y): #this function is to output the path given visited edge
        nextt={}
        for (i,j) in y:
            if y[(i,j)].solution_value()==1:
                nextt[i]=j
        current=0
        path=[]
        for _ in range(len(nextt)-1):
            path.append(nextt[current])
            current=nextt[current]
        return path
    def solve(self):
        model=pywraplp.Solver.CreateSolver('SAT')
        m=self.data['product_num']
        n=self.data['shelf_num']+1
        #define variables
        x={} #the amount of p picked in shelf s
        for p in range(m):
            for s in range(1,n):
                x[(p,s)]=model.IntVar(0,self.data['storage'][p][s],f'x({p},{s})')
        """for i in range(1,n):
            x[i]=model.NewIntVar(0,1,f'x[{i}]')"""
        y={} #the edge is visited or not
        for i in range(n):
            for j in range(n):
                if i!=j:
                    y[(i,j)]=model.IntVar(0,1,f'y({i},{j})')
                else:
                    y[(i,j)]=model.IntVar(0,0,f'y({i},{j})')
        u=[None]*n #variable for Miller Tucker subtour elimination
        for i in range(1,n):
            u[i]=model.IntVar(2,n,f'u[{i}]')
        #define the objective
        model.Minimize(sum([self.data['distance'][i][j]*y[(i,j)] for (i,j) in y]))
        #define the constraints
        #1.Total pickup is larger or equal to kpi
        for p in range(m):
            model.Add(sum([x[(p,s)] for s in range(1,n)])>=self.data['kpi'][p])
        #2.If a shelf is visited,we pick up all the amount of product.Otherwise,no pickup allowed
        for j in range(1,n):
            for p in range(m):
                model.Add(x[(p,j)]==self.data['storage'][p][j]*self.connected_edge(y,j)[1])
        #3.Ensure the path is connected,closed and each shelf is only visited once , and 0 is the start point
        #ensure that there must be one edge to 0 and one edge from 0
        decessor,predecessor=self.connected_edge(y,0)
        model.Add(decessor==1) 
        model.Add(predecessor==1)
        for i in range(1,n):
            #ensure that decessor+predecessor ==0 or ==2
            decessor,predecessor=self.connected_edge(y,i)
            model.Add(decessor<=1)
            model.Add(predecessor<=1)
            model.Add(decessor==predecessor)
        # Only one cycle ensure(E.g: 0-2-0 U 1-3-5-1 is not valid ) by Miller-Tucker-Zemlin subtour elimination
        for i in range(1,n):
            for j in range(1,n):
                model.Add(u[i]-u[j]+1<=(n-1)*(1-y[(i,j)]))
        status = model.Solve()
        if status==pywraplp.Solver.OPTIMAL:
            path=self.construct_path(y)
            return path,model.Objective().Value()
            


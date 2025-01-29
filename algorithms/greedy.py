import math,json
def heuristic1(data,current_shelf,visited): #choose the nearest shelf from the current shelf
        minn=float('inf')
        next_shelf=0
        for shelf,distance in enumerate(data['distance'][current_shelf]):
            if distance<minn and not visited[shelf]:
                next_shelf=shelf
                minn=distance
        return next_shelf
"""def storage_distance(data,shelf):
    a=sum([(min(data['storage'][p][shelf-1],data['kpi'][p])-data['kpi'][p])**2 for p in range(len(data['kpi']))])
    a=math.sqrt(a)
    return a
def heuristic2(data,current_shelf,visited):
    minn=float('inf')
    next_shelf=0
    for shelf in range(1,len(data['distance'][current_shelf])):
        sd=storage_distance(data,shelf)
        if sd<minn and not visited[shelf]:
            next_shelf=shelf
            minn=sd
    return next_shelf   """
class Greedy_Solver:
    #Convention: door is shelf 0
    def __init__(self,data,heuristic=heuristic1):
        self.name='Greedy'
        self.data=data
        self.heuristic=heuristic 
    def is_goal(self,kpi):
        return all(a==0 for a in kpi)
    def solve(self):
        visited=[False for _ in range(self.data['shelf_num']+1)]
        visited[0]=True #start from shelf 0
        route=[]
        value=0
        current_shelf=0
        kpi=self.data['kpi'][:]
        while True:
            next_s=self.heuristic(self.data,current_shelf,visited) #choose the next shelf
            value+=self.data['distance'][current_shelf][next_s] #update the value
            current_shelf=next_s #update current shelf
            route.append(current_shelf) #update the route
            for product in range(len(self.data['kpi'])):
                kpi[product]-=min(kpi[product],self.data['storage'][product][current_shelf]) 
            visited[current_shelf]=True #mark the current shelf as visited
            if self.is_goal(kpi):
                value+=self.data['distance'][current_shelf][0] 
                break 
        return (route,value)
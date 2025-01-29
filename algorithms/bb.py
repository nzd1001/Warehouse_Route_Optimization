import math
import json
maxsize = float('inf')

class BB_Solver:

    def __init__(self, data):
        self.name='Branch and bound'
        self.data = data
        self.final_res = maxsize  # Stores the final minimum weight of shortest route.
        self.final_path = []  # Stores the final route
        self.Cmin = maxsize # Stores the minimum weight in the distance matrix

    def is_goal(self, kpi):
        return all(a <= 0 for a in kpi)

    def solve(self):
        # Initialize current path, visited array, order, current weight and Cmin
        N = len(self.data['distance'])
        for i in range(N):
            for j in range(N):
                if i != j and self.Cmin > self.data['distance'][i][j]:
                    self.Cmin = self.data['distance'][i][j]
        kpi = self.data['kpi']
        curr_bound = 0
        curr_weight = 0
        curr_path = [-1] * (N + 1)
        visited = [False] * N
        # We start at level 1 so the first node in curr_path[] is 0 which is marked as visited
        visited[0] = True
        curr_path[0] = 0
        self.BB(curr_bound, 1, curr_weight, curr_path, visited, kpi)
        return self.final_path, self.final_res

    # function takes arguments:
    # curr_bound -> lower bound of the root node
    # curr_weight-> stores the weight of the path so far
    # level-> current level while moving in the search space tree
    # curr_path[] -> where the solution is being stored which would later be copied to final_path[]
    # visited -> check list of what shelf has been visited
    # kpi -> stores products

    # Recursive function to explore the solution space
    def BB(self, curr_bound, level, curr_weight, curr_path, visited, kpi):
        N = len(self.data['distance'])
        # base case is when we have picked up enough products
        if self.is_goal(kpi):
            curr_res = curr_weight + self.data['distance'][curr_path[level - 1]][curr_path[0]]
            # Update final path if a better solution is found
            if curr_res < self.final_res:
                self.final_path.clear()
                for i in curr_path[1:]:
                    if i != -1 and i != 0:
                        self.final_path.append(i)
                self.final_res = curr_res
            return
        # Explore the solution space recursively
        for i in range(N):
            # Consider next node if it is not same
            # (diagonal entry in adjacency matrix and not visited already)
            if self.data['distance'][curr_path[level - 1]][i] != 0 and visited[i] == False:
                tp_kpi = kpi[:]
                curr_weight += self.data['distance'][curr_path[level - 1]][i]
                # if a feasible solution is found, change how to calculate the bound
                if self.final_path:
                    curr_bound = curr_weight + self.Cmin*abs(len(self.final_path)-level)
                else:
                    curr_bound = curr_weight + self.Cmin*(N-level)
                # if current bound is smaller than the best current weight then continue to go down that node 
                if curr_bound <= self.final_res:
                    curr_path[level] = i
                    visited[i] = True
                    for product in range(len(kpi)):
                        kpi[product] -= self.data['storage'][product][i]
                        # call BB for the next level
                    self.BB(curr_bound, level + 1, curr_weight, curr_path, visited, kpi)
                # Else we have to prune the node by resetting all changes to curr_weight, curr_bound and kpi
                kpi = tp_kpi
                curr_weight -= self.data['distance'][curr_path[level - 1]][i]
                curr_bound = 0
                # Also reset the visited array and curr_path
                visited = [False] * len(visited)
                for j in range(level):
                    if curr_path[j] != -1:
                        visited[curr_path[j]] = True
                for j in range(N-1, level-1, -1):
                    curr_path[j] = -1


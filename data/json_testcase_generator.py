import random
import json
n=int(input('Num of shelves: '))
m=int(input('Num of products: '))
print(m,n)
storage=[]
for p in range(m):
    storage.append([])
    for s in range(n):
        storage[p].append(random.randint(1,30))
d=[]
for i in range(n+1):
    d.append([])
    for j in range(n+1):
        if i==j:
            d[i].append(0)
        elif j>i:
            d[i].append(random.randint(10,100))
        else:
            d[i].append(d[j][i])
       
kpi=[random.randint(n,sum([storage[p][s] for s in range(n)])//2) for p in range(m)]
testcases={}
testcases['testcase']={}
testcases['testcase']['shelf_num']=n
testcases['testcase']['product_num']=m
testcases['testcase']['storage']=storage
testcases['testcase']['distance']=d
testcases['testcase']['kpi']=kpi
with open('data/testcase.json','w') as file:
    #json.dump(testcases,file,separators=(",", ":"))
    json.dump(testcases,file,indent=4)


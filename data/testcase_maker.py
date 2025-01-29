import random
n=int(input('Num of shelves: '))
m=int(input('Num of products: '))
print(m,n)
storage={}
for p in range(m):
    for s in range(n):
        storage[(p,s)]=random.randint(1,30)
        print(storage[(p,s)],end=' ')
    print('')
d={}
for i in range(n+1):
    for j in range(n+1):
        if i==j:
            d[(i,j)]=0
        elif j>i:
            d[(i,j)]=random.randint(5,100)
        else:
            d[(i,j)]=d[(j,i)]
        print(d[(i,j)],end=' ')
    print('')
kpi=[random.randint(n,sum([storage[(p,s)] for s in range(n)])//2) for p in range(m)]
print(' '.join(str(i) for i in kpi))
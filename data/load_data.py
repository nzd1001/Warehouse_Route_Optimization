import json
def load_data_from_json(): #this is to load data from file testcase.json
    with open('data/testcase.json', 'r') as file:
        testcases = json.load(file)
    for i in testcases['testcase']['storage']:
        i.insert(0, 0)
    return testcases['testcase']
def load_data_from_json2(): #this is to load data fron file testcases.json
    with open('data/testcases.json','r') as file:
        testcases=json.load(file)
    for name in testcases:
        for i in testcases[name]['storage']:
            i.insert(0,0)
    return testcases
def load_data_from_input(): #this is to load data from user input
    data = {}
    data['product_num'], data['shelf_num'] = tuple(map(int, input().split()))
    data['storage'] = []
    for i in range(data['product_num']):
        x = [0]
        x.extend([int(j) for j in input().split()])
        data['storage'].append(x)
    data['distance'] = []
    for i in range(data['shelf_num'] + 1):
        x = [int(j) for j in input().split()]
        data['distance'].append(x)
    data['kpi'] = [int(i) for i in input().split()]
    return data
data=load_data_from_json()
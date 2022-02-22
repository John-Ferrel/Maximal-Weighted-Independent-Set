from operator import itemgetter, attrgetter
import scipy.io as scio
import time


#  1_1.改进DtOne查找,将删去点权重改为0
class Node:
    def __init__(self, index, weight, adjVec = []):
        self.index = index
        self.weight = weight
        self.adjVec = adjVec
        self.adjNum = 1
        self.adjIndex = []
        self.adjWei = self.weight
        for i,v in enumerate(adjVec):
            if v == 1:
                self.adjNum += 1
                self.adjWei += weightList[i]
                self.adjIndex.append(i)
        self.weightPerNumPlusOne = float(weight)/float(self.adjNum)
        self.adjWeiRate = float(self.weight)/float(self.adjWei)

    def getAdjNode(self):
        temp = []
        for index,value in enumerate(self.adjVec):
            if value == 1:
                temp.append(index)
        temp.append(self.index)
        return temp

    def updateAdjNode(self, delNode=[]):
        for i in delNode:
            self.adjVec[i] = 0
        self.adjNum = 1
        self.adjWei = self.weight
        self.adjIndex = []
        for i,v in enumerate(self.adjVec):
            if v == 1:
                self.adjNum += 1
                self.adjWei += weightList[i]
                self.adjIndex.append(i)
        self.weightPerNumPlusOne = float(self.weight) / float(self.adjNum)
        self.adjWeiRate = float(self.weight)/float(self.adjWei)


def cutoff1(graphList):
    temp = []
    for node in graphList:
        if node.adjWeiRate >= 0.5:
            if node not in temp:
                temp.append(node)
    return temp

def repeat_cutoff1(graphList, MWIS):
    global totalWeight
    while 1:
        cut1 = cutoff1(graphList)
        if not cut1:
            break
        for node in cut1:
            MWIS.append(node.index)
            totalWeight += node.weight
            graphList.remove(node)
            weightList[node.index] = 0
            for i in node.adjIndex:
                for j in graphList:
                    if i == j.index:
                        graphList.remove(j)
                        weightList[j.index] = 0
        for j in graphList:
            j.updateAdjNode()

def cutoff2(graphList):
    temp = []
    res = []
    for node in graphList:
        if 0.5 > node.adjWeiRate >= 0.33:
            temp.append(node)
    for i in range(len(temp)):
        for j in range(i + 1,len(temp)):
            resWeight = 0
            for k in graphList[i].adjIndex:
                if k in graphList[j].adjIndex:
                    resWeight += weightList[k]
            if resWeight:
                sumWeight = graphList[i].weight + graphList[j].weight
                sumAdjWeight = graphList[i].adjWei + graphList[j].adjWei - resWeight
                if float(sumWeight)/float(sumAdjWeight) > 0.5:
                    if graphList[i] not in res:
                        res.append(graphList[i])
                    if graphList[j] not in res:
                        res.append(graphList[j])
    return res

def repeat_cutoff2(graphList,MWIS):
    global totalWeight
    while 1:
        cut2 = cutoff2(graphList)
        if not cut2:
            break
        for node in cut2:
            MWIS.append(node.index)
            totalWeight += node.weight
            graphList.remove(node)
            weightList[node.index] = 0
            for i in node.getAdjNode():
                for j in graphList:
                    if i == j.index:
                        graphList.remove(j)
                        weightList[j.index] = 0
        for j in graphList:
            j.updateAdjNode()

#####################################################################################
T1 = time.time()
weightList = [] 
graphList = []
MWIS = []

file = open('GD98_c_test.txt', 'r')    #you can modify testfile here
# file = scio.loadmat('Sandi_authors.mat')
# print(type(file['Problem']))


for i,line in enumerate(file):
    if i == 1:
        for plot in line.split():
            weightList.append( float(plot))
    elif i > 1:
        graphList.append( Node( i-2, weightList[i-2], list( map( float, line.split()))))
file.close()
for i in graphList:
    print(i.index, i.weight, i.adjVec, i.adjNum, i.adjWeiRate)

totalWeight = 0
repeat_cutoff1(graphList,MWIS)
repeat_cutoff2(graphList,MWIS)

graphList.sort(key = attrgetter('index'), reverse = True)
graphList.sort(key = attrgetter('adjWeiRate'))
graphList.reverse()

while len(graphList) > 0:
    repeat_cutoff1(graphList,MWIS)
    if not graphList:
        continue
    repeat_cutoff2(graphList,MWIS)
    if not graphList:
        continue
    for j in graphList:
        j.updateAdjNode()
    MWIS.append(graphList[0].index)
    totalWeight += graphList[0].weight
    for j in graphList:
        if j.index != graphList[0].index:
            j.updateAdjNode(graphList[0].getAdjNode())
    for i in graphList[0].getAdjNode():
        for j in graphList:
            if i == j.index:
                graphList.remove(j)
    graphList.sort(key = attrgetter('index'), reverse = True)
    graphList.sort(key = attrgetter('adjWeiRate'))
    graphList.reverse()

MWIS.sort()
print(MWIS)
print(totalWeight)
print(weightList)
#for i in graphList:
 #   print(i.index ,i.weight , i.adjVec, i.adjNum, i.weightPerNumPlusOne)
T2 = time.time()
print("process time:", (T2-T1)*1000, 'ms')




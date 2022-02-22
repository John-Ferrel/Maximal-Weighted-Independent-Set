from operator import itemgetter, attrgetter
import scipy.io as scio
import time
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
            temp.append(node)
    return temp

def cutoff2(graphList):
    temp = []
    res = []
    for node in graphList:
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
            weightList.append( int(plot))
    elif i > 1:
        graphList.append( Node( i-2, weightList[i-2], list( map( int, line.split()))))
file.close()
for i in graphList:
    print(i.index, i.weight , i.adjVec, i.adjNum, i.weightPerNumPlusOne)

totalWeight = 0
cut1 = cutoff1(graphList)
for node in cut1:
    MWIS.append(node.index)
    totalWeight += node.weight
    # print(node.index,'\t',node.adjIndex)
    graphList.remove(node)
    for i in node.adjIndex:
        for j in graphList:
            if i == j.index:
                graphList.remove(j)
for j in graphList:
    j.updateAdjNode()

cut2 = cutoff2(graphList)
for node in cut2:
    MWIS.append(node.index)
    totalWeight += node.weight
    graphList.remove(node)
    for i in node.getAdjNode():
        for j in graphList:
            if i == j.index:
                graphList.remove(j)
for j in graphList:
    j.updateAdjNode()

graphList.sort(key = attrgetter('index'), reverse = True)
graphList.sort(key = attrgetter('weightPerNumPlusOne'))
graphList.reverse()



while len(graphList) > 0:
    cut1 = cutoff1(graphList)
    for node in cut1:
        MWIS.append(node.index)
        totalWeight += node.weight
        graphList.remove(node)
        for i in node.getAdjNode():
            for j in graphList:
                if i == j.index:
                    graphList.remove(j)
    for j in graphList:
        j.updateAdjNode()
    cut2 = cutoff2(graphList)
    for node in cut2:
        MWIS.append(node.index)
        totalWeight += node.weight
        graphList.remove(node)
        for i in node.getAdjNode():
            for j in graphList:
                if i == j.index:
                    graphList.remove(j)
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
    graphList.sort(key = attrgetter('weightPerNumPlusOne'))
    graphList.reverse()

MWIS.sort()
print(MWIS)
print(totalWeight)
#for i in graphList:
 #   print(i.index ,i.weight , i.adjVec, i.adjNum, i.weightPerNumPlusOne)
T2 = time.time()
print("process time:", (T2-T1)*1000, 'ms')




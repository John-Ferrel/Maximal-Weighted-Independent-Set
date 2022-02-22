from operator import itemgetter, attrgetter
# import scipy.io as scio
import time


#  1_1.改进DtOne查找,将删去点权重改为0
#  1_2.调整cutoff
#  1_5.整合比较
#  1_6.添加注释，调整process循环顺序，检查DtTwo邻接
#  1_7.尝试不循环剪枝
#  1_8.尝试使用newRate
class Node:
    def __init__(self, index, weight, adjVec = [],weightList=[]):
        self.index = index
        self.weight = weight
        self.adjVec = adjVec
        self.adjNum = 1                                                       # 避免度为0时更新错误
        self.adjIndex = []
        self.adjWei = self.weight                                             # 避免度为零更新错误
        for i,v in enumerate(adjVec):
            if v == 1:
                self.adjNum += 1
                self.adjWei += weightList[i]
                self.adjIndex.append(i)
        self.weightPerNumPlusOne = float(weight)/float(self.adjNum)
        self.adjWeiRate = float(self.weight)/float(self.adjWei)               # 属于（0，1], 仅当无邻居为1
        self.newRate = 2 * self.adjWeiRate * self.weightPerNumPlusOne         # 系数调整后的权度比
    def getAdjNode(self):
        temp = []
        for index,value in enumerate(self.adjVec):
            if value == 1:
                temp.append(index)
        temp.append(self.index)
        return temp

    def updateAdjNode(self,weightList=[], delNode=[]):                        # 更新邻接点极其邻接点
        for i in delNode:
            weightList[i] = 0                                                 # 删点，将其权重调为0
        self.adjNum = 1
        self.adjWei = self.weight
        for i,v in enumerate(self.adjVec):
            if v == 1:
                if weightList[i]:
                    self.adjNum += 1
                self.adjWei += weightList[i]
        self.weightPerNumPlusOne = float(self.weight) / float(self.adjNum)
        self.adjWeiRate = float(self.weight)/float(self.adjWei)
        self.newRate = 2 * self.adjWeiRate * self.weightPerNumPlusOne


def cutoff1(graphList):                                                       # DtOne 剪枝
    temp = []
    for node in graphList:
        if node.adjWeiRate > 0.5:
            temp.append(node)
            # print(node.index)
    return temp


def repeat_cutoff1(graphList, MWIS,weightList,totalCutoff1=[]):               # 重复剪枝过程
    global totalWeight
    while 1:
        cut1 = cutoff1(graphList)
        if not cut1:
            break
        for node in cut1:
            MWIS.append(node.index)
            totalCutoff1.append(node.index)
            totalWeight += node.weight
            graphList.remove(node)
            weightList[node.index] = 0
            for i in node.adjIndex:
                for j in graphList:
                    if i == j.index:
                        graphList.remove(j)
                        weightList[j.index] = 0                               # 调整邻居节点权重为0
        for j in graphList:                                                   # 删一批节点后更新，减少时间损耗
            j.updateAdjNode(weightList)


def single_cutoff1(graphList,MWIS,weightList,totalCutoff1=[]):                # 单次剪枝，测试用
    global totalWeight
    cut1 = cutoff1(graphList)
    for node in cut1:
        MWIS.append(node.index)
        totalCutoff1.append(node.index)
        totalWeight += node.weight
        graphList.remove(node)
        weightList[node.index] = 0
        for i in node.adjIndex:
            for j in graphList:
                if i == j.index:
                    graphList.remove(j)
                    weightList[j.index] = 0
                    j.updateAdjNode(weightList,node.getAdjNode())


def cutoff2(graphList,weightList):                                            # DtTwo剪枝
    temp = []
    res = []
    for node in graphList:
        if node.adjWeiRate >= 0.33:
            temp.append(node)
    for i in range(len(temp)):
        for j in range(i + 1,len(temp)):
            resWeight = 0
            if graphList[j].index in graphList[i].adjIndex:                   # 邻接检查
                continue
            for k in graphList[i].adjIndex:
                if k in graphList[j].adjIndex:
                    resWeight += weightList[k]
            if resWeight:
                sumWeight = graphList[i].weight + graphList[j].weight
                sumAdjWeight = graphList[i].adjWei + graphList[j].adjWei - resWeight
                if float(sumWeight)/float(sumAdjWeight) >= 0.5:               # DtTwo检验
                    if graphList[i] not in res:
                        res.append(graphList[i])
                    if graphList[j] not in res:
                        res.append(graphList[j])
    return res


def repeat_cutoff2(graphList, MWIS, weightList, totalCutoff2):                # 重复剪枝过程
    global totalWeight
    while 1:
        cut2 = cutoff2(graphList,weightList)
        if not cut2:
            break
        for node in cut2:
            # print(node.index)
            MWIS.append(node.index)
            totalCutoff2.append(node.index)
            totalWeight += node.weight
            graphList.remove(node)
            weightList[node.index] = 0
            for i in node.getAdjNode():
                for j in graphList:
                    if i == j.index:
                        weightList[j.index] = 0
                        graphList.remove(j)
        for j in graphList:
            j.updateAdjNode(weightList)                                       # 删一批节点后更新，减少时间损耗
        for j in graphList:
            j.updateAdjNode(weightList)


def single_cutoff2(graphList, MWIS, weightList, totalCutoff1=[]):             # 单次剪枝，测试用
    global totalWeight
    cut2 = cutoff2(graphList,weightList)
    for node in cut2:
        MWIS.append(node.index)
        totalCutoff1.append(node.index)
        totalWeight += node.weight
        graphList.remove(node)
        weightList[node.index] = 0
        for i in node.adjIndex:
            for j in graphList:
                if i == j.index:
                    graphList.remove(j)
                    weightList[j.index] = 0
                    j.updateAdjNode(weightList, node.getAdjNode())


#####################################################################################
def process(filename,greedyFeature,pruning=False):
    T1 = time.time()
    totalCutoff1 = []                                                         # DtOne 剪去节点
    totalCutoff2 = []                                                         # DtTwo 剪去节点
    weightList = []
    graphList = []
    MWIS = []

    file = open(filename, 'r')    #you can modify testfile here
    # file = scio.loadmat('Sandi_authors.mat')
    # print(type(file['Problem']))

    for i, line in enumerate(file):                                           # 初始化节点
        if i == 1:
            for plot in line.split():
                weightList.append( float(plot))
                # print(line)
        elif i > 1:
            graphList.append( Node( i-2, weightList[i-2], list( map( float, line.split())),weightList))
    file.close()
    # for i in graphList:
    #     print(i.index, i.weight, i.adjVec, i.adjNum, i.adjWeiRate)
    global totalWeight
    totalWeight = 0
    if pruning:                                                               # 第一次剪枝
        # single_cutoff1(graphList,MWIS,weightList,totalCutoff1)
        # single_cutoff2(graphList,MWIS,weightList,totalCutoff2)
        repeat_cutoff1(graphList,MWIS,weightList,totalCutoff1)
        repeat_cutoff2(graphList, MWIS, weightList, totalCutoff2)

    graphList.sort(key = attrgetter('index'), reverse = True)                 # 排序，便于检查校验，也可用于找到贪心特征最大节点
    graphList.sort(key = attrgetter(greedyFeature))
    graphList.reverse()

    while len(graphList) > 0:
        if pruning:                                                           # 剪枝
            # single_cutoff1(graphList,MWIS,weightList,totalCutoff1)
            repeat_cutoff1(graphList,MWIS,weightList,totalCutoff1)
            if not graphList:
                continue
            # single_cutoff2(graphList,MWIS,weightList,totalCutoff2)
            repeat_cutoff2(graphList, MWIS, weightList, totalCutoff2)
            if not graphList:
                continue
            for j in graphList:
                j.updateAdjNode(weightList)
        graphList.sort(key = attrgetter('index'), reverse = True)
        graphList.sort(key = attrgetter(greedyFeature))
        graphList.reverse()
        MWIS.append(graphList[0].index)                                       # 贪心查找
        totalWeight += graphList[0].weight
        weightList[graphList[0].index] = 0
        for j in graphList:
            if j.index != graphList[0].index:
                j.updateAdjNode(weightList,graphList[0].getAdjNode())
        for i in graphList[0].getAdjNode():
            for j in graphList:
                if i == j.index:
                    graphList.remove(j)

    MWIS.sort()                                                               # 独立集索引排序
    print('-----------------------------------------------------------------------------------------')
    print('greedyFeature=',greedyFeature,',pruning=',pruning,':')
    if sum(weightList):                                                       # 若!=0, 则说明有点被遗漏
        print('Error!!!')
        print(weightList)
    print('MWIS:',MWIS)
    print('totalWeight:',totalWeight)
    #for i in graphList:
     #   print(i.index ,i.weight , i.adjVec, i.adjNum, i.weightPerNumPlusOne)
    T2 = time.time()
    if pruning:
        print('cutoff1_index_set:',totalCutoff1)
        print('cutoff2_index_set:',totalCutoff2)
    print("process time:", (T2-T1)*1000, 'ms')


#####################################################################################
totalWeight = 0
filename = 'GD98_c_test.txt'
print('Testset\'s name:',filename)
process(filename=filename,greedyFeature='weightPerNumPlusOne',pruning=False)
process(filename=filename,greedyFeature='adjWeiRate',pruning=False)
process(filename=filename,greedyFeature='newRate',pruning=False)
process(filename=filename,greedyFeature='weightPerNumPlusOne',pruning=True)
process(filename=filename,greedyFeature='adjWeiRate',pruning=True)
process(filename=filename,greedyFeature='newRate',pruning=True)
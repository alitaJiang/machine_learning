import numpy
import random
import math

class User:

    # 一次计算周期的耗能为e(mJ)
    e = 5e-6
    # 当处理一个数据元素时，需要yita个数据周期
    yita = 100
    # 一个数据单元所含的位数
    s = 8

    # 路径损耗指数初值
    beta = 2.5
    # 参考距离d0(m)
    d0 = 200
    # 自由空间路径损耗减弱常数，基站已知 波长 = 3e+8/2.4GHz(m)
    G = 0.5  # (0.125/(4*3.14159*d0))**2
    # noise spectral dencity
    N0 = 1e-6

    # 传输数据的时间(ms)
    T = 20



    def __init__(self, offloadType, d, beta = 2.5, m = 60):

        # 每个用户设备有L个数据块
        self.L = 10
        # 每个用户、每个数据块的数据单元数量
        self.m = m
        # 更改beta
        User.beta = beta
        # 每个用户需要处理的数据
        self.data = self.m * self.L * User.s

        # 用户的带宽(MHz)
        self.B = Server.BW/50

        self.alpha = None
        # offload权重初值
        if offloadType == "SL":
            self.alpha = random.random()
        elif offloadType == "SF":
            self.alpha = random.randint(0,1)
        else: raise Exception("offloadType must be SL or SF")

        # 用户离服务器的距离d(m)，在半径为800的圆内的均匀分布
        self.d = d

        # 用户完全自己处理的耗能
        self.energyUserFullyProcessed = self.L*User.e*User.yita*complexity(self.m)
        # 用户设备自己处理的耗能
        self.energyUserProcessed = (1 - self.alpha)*self.energyUserFullyProcessed
        # 完全转给服务器处理的耗能
        self.energyFullyOffload = (2 ** (self.data / (self.B * 1000 * User.T)) - 1) / User.G * (self.d / User.d0) ** User.beta * User.N0 * self.B * User.T * 1000
        # 转给服务器处理的耗能
        self.energyOffload = (2**(self.alpha*self.data/(self.B * 1000 * User.T)) - 1)/User.G * (self.d/User.d0)**User.beta * User.N0 * self.B * User.T * 1000
        # 用户总耗能
        self.energySum = self.energyUserProcessed + self.energyOffload

        # 服务器处理用户部分的计算次数
        self.cUser2Serv = Server.yita * complexity(self.m)


    # 迭代使用的权重
    def getAlpha(self):
        return self.alpha

    # 返回数据量
    def getM(self):
        return self.m




class Server:

    # 当处理一个数据元素时，需要yita个数据周期
    yita = 1

    # 服务器的处理时间(ms)
    Tpr = 1

    # 服务器单位时间的处理次数(MHz)
    Cs = 200

    # 在指定时间里服务器的最大计算周期数
    Csmax = Cs * Tpr * 1e+3

    # 给服务器的计算总量
    Csum = 0

    # 总带宽(MHz)
    BW = 10


    # 连接服务器的用户List
    def linkUsers(self, usersList):
        for user in usersList:
            Server.Csum += user.L * user.getAlpha() * user.cUser2Serv

    def updateUsers(self, usersList):
        Server.Csum = 0
        for user in usersList:
            Server.Csum += user.L * user.getAlpha() * user.cUser2Serv



# the linear complexity function, with m data elements
def complexity(m):
    return m

# 更新alpha，相应的能量值也重算
def updateAlpha(userList, alphaList):
    for i in range(len(userList)):
        userList[i].alpha = alphaList[i]
        userList[i].energyUserProcessed = (1 - userList[i].alpha)*userList[i].energyUserFullyProcessed
        userList[i].energyOffload = (2 ** (userList[i].alpha * userList[i].data / (userList[i].B * 1000 * User.T)) - 1) / User.G * (userList[i].d / User.d0) ** User.beta * User.N0 * userList[i].B * User.T * 1000
        userList[i].energySum = userList[i].energyUserProcessed + userList[i].energyOffload
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math, random
from optimization.kkt import KKT
from optimization.evolution import Evolution

# 初始化出图用的beta和m
betaList = [2 + 0.1*i for i in range(21)]
mList = [20 + 20*i for i in range(15)]

# 确定移动设备的位置
dList = [math.sqrt(random.random())*800 for i in range(50)]

# 一些因变量 均为服务器满负荷的情况
miu_beta_SL = []
Esum_beta_0 = []
Esum_beta_1 = []
Esum_beta_alpha_SL = []
miu_M_SL = []
Esum_m_0 = []
Esum_m_1 = []
Esum_m_alpha_SL = []

# methodClass取KKT或者Evolution
def presentation(methodClass):
    for beta in betaList:

        # 自动开始KKT或者Evolution计算，得到alpha
        method = methodClass(dList, beta)

        alpha_sum = 0
        Esum_0 = 0
        Esum_1 = 0
        Esum_alpha = 0

        # 取数据
        for user in method.userList:
            alpha_sum += user.alpha
            Esum_0 += user.energyUserFullyProcessed
            Esum_1 += user.energyFullyOffload
            Esum_alpha += user.energySum

        miu = alpha_sum/50

        miu_beta_SL.append(miu)
        Esum_beta_0.append(Esum_0)
        Esum_beta_1.append(Esum_1)
        Esum_beta_alpha_SL.append(Esum_alpha)

    for m in mList:
        # 自动开始KKT或者Evolution计算，得到alpha
        method = methodClass(dList, 2.5, m)

        alpha_sum = 0
        Esum_0 = 0
        Esum_1 = 0
        Esum_alpha = 0

        # 取数据
        for user in method.userList:
            alpha_sum += user.alpha
            Esum_0 += user.energyUserFullyProcessed
            Esum_1 += user.energyFullyOffload
            Esum_alpha += user.energySum

        miu = alpha_sum / 50

        miu_M_SL.append(miu)
        Esum_m_0.append(Esum_0)
        Esum_m_1.append(Esum_1)
        Esum_m_alpha_SL.append(Esum_alpha)

# 画图







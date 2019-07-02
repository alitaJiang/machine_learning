from optimization.edgeCloudOffloading import *
import math


class KKT:

    def __init__(self, dList, beta=2.5, m=60):
        # 初始化
        N = 50
        self.userList = []
        server = Server()

        for i in range(N):
            self.userList.append(User("SL", dList[i], beta, m))

        server.linkUsers(self.userList)

        # 为user赋予kkt相关属性
        for user in self.userList:
            user.r = user.data / (user.B * 1000 * user.T)
            user.K = math.log(2) * (user.d / User.d0)**User.beta * User.N0 * user.data / User.G

        # 自动运行
        self.iterate_alpha_v_full_load()



    def iterate_alpha_v_full_load(self, offloadingType = "SL"):

        # 初始化拉格朗日常数v
        # 如果v>0，意味着服务器在满负荷运行，如果v=0，服务器没有满负荷运行
        v = 0.0025  # 假设一种情况：服务器满负荷运行

        # flours = []
        # ceilings = []
        # for user in userList:
        #     flours.append((user.energyUserFullyProcessed - user.K * 2**user.r)/user.cUser2Serv)
        #     ceilings.append((user.energyUserFullyProcessed - user.K)/user.cUser2Serv)
        #
        # flour = max(max(flours), 0)
        # ceiling = min(ceilings)
        #
        # # theorem 2
        # if v < flour:
        #     v1 = flour
        # if v > ceiling:
        #     v1 = ceiling

        cnt = 0

        alphas1 = []
        for user in self.userList:
            alphas1.append(user.alpha)
        alphas2 = []

        while cnt < 1000:
            # 计算最优解alpha
            v_new = 0
            weightAll = 0

            for user in self.userList:
                _alpha = 1 / user.r * math.log2(1 / user.K * (user.energyUserFullyProcessed - v * user.cUser2Serv))
                # print(_alpha)
                if _alpha < 0:
                    user.alpha = 0
                    weightPerUser = math.exp(_alpha)
                elif _alpha > 1:
                    user.alpha = 1
                    weightPerUser = math.exp(1 - _alpha)
                else:
                    if offloadingType == "SF":
                        if _alpha > 0.5:
                            user.alpha = 1
                        else:
                            user.alpha = 0
                    else:
                        user.alpha = _alpha
                    weightPerUser = 1
                alphas2.append(user.alpha)

                # 根据更新的alpha反算v，因为v可能不同
                _v = (user.energyUserFullyProcessed - user.K * 2**(user.alpha * user.r)) / user.cUser2Serv
                if _v < 0:
                    _v = 0
                v_new += _v * weightPerUser
                weightAll += weightPerUser

            print(str(cnt + 1) + "次迭代结果是" + str(alphas2))
            cnt += 1

            diff = norm2(alphas2, alphas1)
            print("本次迭代最优解之间的差距为：" + str(diff))
            if diff < 0.001:
                break

            # 前进一步
            alphas1 = alphas2
            alphas2 = []

            # 更新v
            v = v_new / weightAll
            print("本次迭代更新的v是: " + str(v))
            print("\n")

        updateAlpha(self.userList, alphas2)
        return alphas2


    # 假设没有全负载，默认10%
    def iterate_alpha_v_under_load(self, offloadingType = "SL", loadPersantage = 0.1):

        alphas = []

        for user in self.userList:
            _alpha = 1 / user.r * math.log2(1 / user.K * (user.energyUserFullyProcessed))
            if _alpha < 0:
                user.alpha = 0

            elif _alpha > 1:
                user.alpha = 1

            else:
                if offloadingType == "SF":
                    if _alpha > 0.5:
                        user.alpha = 1
                    else:
                        user.alpha = 0
                else:
                    user.alpha = _alpha

            alphas.append(user.alpha)

        updateAlpha(self.userList, alphas)
        return alphas



def norm2(arrayList1, arrayList2):
    if len(arrayList1) != len(arrayList2):
        raise Exception("two arrays must be of same length!")
    s = 0
    for i in range(len(arrayList1)):
        s += (arrayList1[i] - arrayList2[i])**2
    return math.sqrt(s)





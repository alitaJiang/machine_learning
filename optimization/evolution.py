from optimization.edgeCloudOffloading import *


## 进化算法
class Evolution:

    server = Server()

    def __init__(self, dList, beta=2.5, m=60):
        # 引入50个user
        self.userList = []
        for i in range(50):
            self.userList.append(User("SL", dList[i], beta, m))
        Evolution.server.linkUsers(self.userList)

        self.evolve()

    def evolve(self):
        # 初始化alpha种群, 含有10000个alpha随机值数组，数组长度50
        population = []
        for j in range(10000):
            alphas = []
            for k in range(50):
                alphas.append(random.random())
            population.append(alphas)

        # 编码（数组无需编码）

        # 对种群进行评价和淘汰
        for cnt in range(5):
            _population = []
            # 淘汰在可行域外面的alpha数组
            for arr in population:
                updateAlpha(self.userList, arr)
                Evolution.server.updateUsers(self.userList)

                if Server.Csum <= Server.Csmax:
                    _population.append(arr)

            population = _population
            # print(len(population))
            # 淘汰总能量不在底部20%的alpha数组
            totalEnergyList = []
            for arr in population:
                updateAlpha(self.userList, arr)
                Evolution.server.updateUsers(self.userList)
                totalEnergy = 0
                for user in self.userList:
                    totalEnergy += user.energySum
                totalEnergyList.append(totalEnergy)

            _totalEnergyList = [totalEnergyList[i] for i in range(len(totalEnergyList))]
            _totalEnergyList.sort()

            totalEnergyMin = _totalEnergyList[0]
            totalEnergyMax = _totalEnergyList[-1]

            # 找到下20%的边界
            totalEnergyBoundary = totalEnergyMin + 0.2 * (totalEnergyMax - totalEnergyMin)

            _population = []
            for totalEnergy in totalEnergyList:
                if totalEnergy <= totalEnergyBoundary:
                    _population.append(population[totalEnergyList.index(totalEnergy)])

            population = _population
            # print(len(population))

            # 繁衍后代
            new_population = [] + population

            # if (len(population) % 2 == 1):
            #     population.pop()

            for i in range(len(population) - 1):
                # 随便挑选两个个体，让其中的alpha发生一个小幅度抖动，然后再产生2个个体，规则是两个个体中每个alpha都是之前两个个体的线性插值
                parent1 = population[i]
                parent2 = population[i + 1]

                for alpha in parent1:
                    alpha += 0.005 * random.random() - 0.0025
                for alpha in parent2:
                    alpha += 0.005 * random.random() - 0.0025

                child1 = []
                child2 = []

                for i in range(len(parent1)):
                    child1.append(2/3 * parent1[i] + 1/3 * parent2[i])
                    child2.append(1/3 * parent1[i] + 2/3 * parent2[i])

                new_population.append(child1)
                new_population.append(child2)

            population = new_population
            print("第" + str(cnt + 1) + "轮变异之后的种群还剩" + str(len(population)) + "个个体")

        # 对最后的选择结果做均值
        resultAlphas = []
        for i in range(50):
            _alpha = 0
            for arr in population:
                _alpha += arr[1]
            resultAlphas.append(_alpha / len(population))

        updateAlpha(self.userList, resultAlphas)
        Evolution.server.updateUsers(self.userList)



# 出图看效果
# x = []
# y = []
#
# for arr in population:
#     x.append(arr[0])
#     y.append(arr[1])
#
# plt.plot(x, y, "ob")




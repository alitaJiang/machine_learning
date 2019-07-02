

def quafun(a,b,c,start = 1, recur = 0):
    recur+=1
    if recur >= 30:
        return '方程无解'
    solution1 = start
    solution2 = -c/(a*solution1+b)
    if abs(solution1-solution2) <= 0.00001:
        return solution2
    else:
        solution1 = solution2
        solution2 = quafun(a,b,c,solution1, recur)
    return solution2


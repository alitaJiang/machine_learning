from multiprocessing import Pool
import time


def sha(fn):
    def wrap(*args, **kwargs):
        print('start to process')
        print(fn(*args, **kwargs))
        print('finished')

    return wrap

# sumAll = sha(sumAll)

@sha
def sumAll(*args, **kwargs):
    a = 0
    for i in args:
        a+=i
    return a

def dec1(func):
    print("1111")
    def one():
        print("2222")
        func()
        print("3333")
    print('傻逼拉')
    return one

def dec2(func):
    print("aaaa")
    def two():
        print("bbbb")
        func()
        print("cccc")
    print('汤老师')
    return two

@dec1
@dec2
def test():
    print("test test")

print("finished")




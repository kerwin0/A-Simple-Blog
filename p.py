import time


def timer(func):
    def inner(*args, **kwargs):
        start = time.time()
        re = func(*args, **kwargs)
        print(time.time() - start)
        return re

    return inner


@timer  # ==> func2 = timer(func2)
def func2(a):
    print('in func2 and get a:%s' % (a))
    return 'fun2 over'


func2('aaaaaa')
print(func2('aaaaaa'))

import time
import random
def count1(num):
    counter =0
    while num:
        if (num&1):
            counter+=1
        num=num>>1
    return counter

def count2(num):
    ans=len(str(bin(num)).replace("0",""))-1
    return ans
print(count2(11))
limit = 100000

t1=time.time()
fastest  = [count1(random.randint(100000000000000000000000,10000000000000000000000000)) for _ in range(limit)]
t1=time.time()-t1

t2=time.time()
fastest2 = [count2(random.randint(100000000000000000000000,10000000000000000000000000)) for _ in range(limit)]
t2=time.time()-t2

print('fastest',t1)
print('fastest2',t2,)

#
# data=""
#
#
#
#
#
#
#
#

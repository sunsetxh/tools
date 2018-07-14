# coding=utf-8
import getopt

import numpy as np
import time

import sys


def usage():
    print("""usage:
             -s:开始序号
             -e:结束序号
             -n:序号数量
             -h:帮助
    """)


start = 1
end = 82725
num = 15000

opts, args = getopt.getopt(sys.argv[1:], "hs:e:n:")

for op, value in opts:
    if op == "-s":
        start = int(value)
    elif op == "-e":
        end = int(value)
    elif op == "-n":
        num = int(value)
    elif op == "-h":
        usage()
        sys.exit()

indexs = np.random.randint(start, end, int(float(num) * (float(num) / float(end) - 0.04 + 1)))  # 会有重复，所以多生成一些
print(len(indexs))
indexs = list(set(indexs))  # 去重
print(len(indexs))
while len(indexs) >= num:  # 随机删除多余的
    indexs.pop(np.random.randint(0, len(indexs), 1))
# print(len(indexs))
indexs.sort()  # 排序

#print(indexs[0:100])

nowtime = time.strftime("%m%d%H%M%S")

f = open('index-{}-{}.txt'.format(num, nowtime), 'w')

for index in indexs:
    f.write('{} '.format(index))
f.close()

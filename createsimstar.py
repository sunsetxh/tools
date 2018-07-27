# python2.7
# coding:utf-8
# 将star文件读取到内存中
import operator

import sys

import os


def readstarfile(filename):
    f_star = open(filename, 'r')
    lines = f_star.readlines()
    headlen = 0
    headdict = {}
    for line in lines:
        headlen += 1
        if len(line.split()) <= 1:
            continue
        elif len(line.split()) > 2:
            break
        strlist = line.split()
        # 将文件头信息存储到字典中
        headdict.update({strlist[0][4:]: int(strlist[1].strip('#')) - 1})
    data = []
    for i in range(headlen - 1, len(lines)):
        if len(lines[i].split()) < 3:
            continue
        data.append(lines[i])
    f_star.close()
    return headdict, data


# 存储star文件，支持原数据存储和简洁数据存储
def savestar(filename, headdict, data):
    file = open(filename, 'w')
    file.write('\ndata_\n\nloop_\n')
    head = sorted(headdict.items(), key=operator.itemgetter(1))
    for name, value in head:
        file.write('_rln{} #{}\n'.format(name, value + 1))
    for item in data:
        file.write(item)
    file.close()


inputdir = sys.argv[0]
datagroup = []
headgroup = []
headdict = {}
os.system('mkdir {0}/Image/'.format(inputdir))
for i in range(1, 6):
    os.system('cp {0}/{1}/preprocessed.mrcs ../Image/group{2}.mrcs'.format(inputdir, i, i))
    headdict, data = readstarfile('{0}/{1}/s_group1-1.star'.format(inputdir, i))
    for line in data:
        line.replace('preprocessed.mrcs', 'Image/group{0}.mrcs'.format(i))
    print(data)
    datagroup.append(data)
    headgroup.append(headdict)

savestar('total.star', headdict, datagroup)

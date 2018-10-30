import numpy as np
import sys
import os

# 类别总数，主要用于求平均值
clsnum = 2
clsname = 'glob_dis4+127_0_160.mrcs'


def mergefiles():
    outputfiles = []
    files = os.listdir(os.getcwd())

    files.sort()
    filelist = []
    # delete the files which we not need
    for f in files:
        if len(f) == 20:
            filelist.append(f)

    del files
    group = [[] for i in range(10)]

    # files classfication
    for f in filelist:
        file = open(f, 'r')
        for line in file:
            grpnum = int(line.split('\t')[1].split('_')[2])
            if grpnum != 0:
                group[grpnum - 1].append(f)
                break
    # merge the files which have the same group
    for i in range(len(group)):
        if len(group[i]) != 0:
            name = 'diff2_group{}'.format(i + 1)
            outputfiles.append(name)
            output = open(name, 'w')
            for file in group[i]:
                for line in open(file):
                    output.write(line)
            output.close()
    return outputfiles


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


def dealwithdata(infile, outfile, clsnum, clsname):
    file_diff2 = open(infile, 'r')
    i = -1
    # group num 0 1 2 3 4
    diff2 = []
    temp = []

    for line in file_diff2:
        items = line.split('\t')
        if i == int(items[0]):
            temp.append(float(items[3]))  # find the same particle and append
            continue
        elif i != -1:
            min_index = temp.index(min(temp[3:]))
            temp.append(min_index - 3)  # 添加最小值
            diff2_avg = float(np.average(temp[3:3 + clsnum]))
            temp.append(diff2_avg)  # 添加均值
            # for j in temp[2:]):
            #   j -= diff2_min
            # temp.append(float(max(temp[2:]) - min(temp[2:])))
            # 添加差值
            if len(temp) == 7:
                temp.append(temp[3] - temp[4])
            else:
                temp.append(temp[temp[0] + 1] - temp[min_index])
            # 将该行数据添加至列表
            diff2.append(temp)
            if len(items) <= 1:
                break
            else:
                del temp
                temp = []

        if items[1].find('group') != -1:  # support more than 2 classes
            temp.append(int(items[1][items[1].index('group') + 5]))  # temp[0]
            temp.append(int(items[1][0:(items[1].index('@'))]))  # temp[1]
        else:  # only support 2 classes
            temp.append(int(items[0]))  # temp[0]
            if items[1].find(clsname) != -1:
                temp.append(0)  # temp{1]
            else:
                temp.append(1)  # temp[1]
        temp.append(items[1])  # temp[2]
        temp.append(float(items[3]))
        i = int(items[0])

    diff2.sort()
    output = open(outfile, 'w')
    fmt = []
    for item in diff2[0]:
        tpy = type(item)
        # print(item)
        # print(tpy)
        if tpy == int:
            fmt.append('{:6d}\t')
        elif tpy == float:
            fmt.append('{:8.2f}\t')
        elif tpy == str:
            fmt.append('{:6s}\t')
        else:
            fmt.append('{}\t')
    # print(fmt)
    for items in diff2:
        for i in range(len(items)):
            output.write(fmt[i].format(items[i]))
        output.write('\n')
    output.close()
    file_diff2.close()


files = mergefiles()
for f in files:
    dealwithdata(f, '{}.txt'.format(f), clsnum, clsname)

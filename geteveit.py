# coding=utf-8

# 将star文件读取到内存中
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


def getdatastar():
    datas = []
    path = os.listdir(os.getcwd())
    for p in path:
        if p.find('_data.star'):
            datas.append(p)
    datas.sort()
    return datas


data_path = getdatastar()
print(data_path)

fout = open('result.txt', 'w')

for p in data_path:
    head, data = readstarfile(p)
    clsdis = [[0] * 2 for i in range(2)]
    for line in data:
        item = line.split()
        if item[head['ImageName']].find('_200.mrcs') != -1:
            clsdis[int(item[head['ClassNumber']]) - 1][0] += 1
        else:
            clsdis[int(item[head['ClassNumber']]) - 1][1] += 1
    fout.write(
        '{0:6s}\t{1:7d}\t{2:7d}\t{3:7d}\t{4:7d}\n'.format(p.split('_')[1],
                                                          clsdis[0][0], clsdis[0][1],
                                                          clsdis[1][0], clsdis[1][1]))

fout.close()
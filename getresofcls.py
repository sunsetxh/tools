# coding=utf-8


# 将star文件读取到内存中
import sys


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


headdict, data = readstarfile(sys.argv[1])
count = 0
classcnt = [0, 0, 0, 0, 0]

for item in data:
    items = item.split()
    if items[headdict.get('ImageName')].find('group{}'.format(items[headdict.get('ClassNumber')])) != -1:
        count += 1
        classcnt[int(items[headdict.get('ClassNumber')]) - 1] += 1

print('正确率 ＝ {:4f}％'.format(count * 100.0 / len(data)))
for i in range(0,5):
    print('class {} = {:4f}%'.format(i+1,classcnt[i] * 100.0 / 10000))

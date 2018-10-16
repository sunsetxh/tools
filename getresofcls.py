# coding=utf-8
import sys


# 将star文件读取到内存中
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
clscnt = [0, 0, 0, 0, 0]
classrtcnt = [0, 0, 0, 0, 0]
cnt = [[0] * 5 for i in range(5)]

for line in data:
    vars = line.split()
    clsnum = int(vars[headdict['ClassNumber']])
    groupnum = int(vars[headdict['ImageName']][-6])
    cnt[clsnum - 1][groupnum - 1] += 1

print(cnt)

f_det = open('detailedresult.txt', 'w')
for i in range(5):
    for j in range(5):
        f_det.write('{:5d}\t'.format(cnt[i][j]))
    f_det.write('\n')
f_det.close()

for item in data:
    items = item.split()
    clscnt[int(items[headdict.get('ClassNumber')]) - 1] += 1
    if items[headdict.get('ImageName')].find('group{}'.format(items[headdict.get('ClassNumber')])) != -1:
        count += 1
        classrtcnt[int(items[headdict.get('ClassNumber')]) - 1] += 1

print('正确率 ＝ {:4f}％'.format(count * 100.0 / len(data)))
for i in range(0, 5):
    if clscnt[i] == 0:
        print('class {} = {:4f}% number = {}'.format(i + 1, 0.0, clscnt[i]))
    else:
        print('class {} = {:4f}% number = {}'.format(i + 1, classrtcnt[i] * 100.0 / clscnt[i], clscnt[i]))

f = open('result.txt', 'a')
f.write('{}\n'.format(sys.argv[1]))
f.write('{:20s}\t'.format('result'))
for i in range(1, 6):
    f.write('{:>18s} {:1d}\t'.format('class', i))
f.write('{:>20s}\t'.format('total'))
f.write('\n')
f.write('{:20s}\t'.format('Number of particles'))
for i in range(0, 5):
    f.write('{:20d}\t'.format(clscnt[i]))
f.write('{:20d}\t'.format(len(data)))
f.write('\n')
f.write('{:20s}\t'.format('Correct rate'))
for i in range(0, 5):
    if clscnt[i] == 0:
        f.write('{:20f}%\t'.format(0))
    else:
        f.write('{:20f}%\t'.format(classrtcnt[i] * 100.0 / clscnt[i]))
f.write('{:20f}%\t'.format(count * 100.0 / len(data)))
f.write('\n\n\n\n')
f.close()

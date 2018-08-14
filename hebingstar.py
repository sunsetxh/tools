# python2.7
# coding:utf-8
import os
import re

import operator

import time

__author__ = 'WangYuchao'

import sys
import getopt

labels = ['MicrographName', 'CoordinateX', 'CoordinateY', 'ImageName',
          'DefocusU', 'DefocusV', 'DefocusAngle', 'Voltage',
          'SphericalAberration', 'AmplitudeContrast',
          'Magnification', 'DetectorPixelSize', 'CtfFigureOfMerit']


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


# 挑选出star文件中指定类的数据
def getclassdata(filename, k):
    headdict, data = readstarfile(filename)
    newdata = []
    for line in data:
        for classnum in k:
            if int(line.split()[headdict.get('ClassNumber', 0)]) == classnum:
                newdata.append(line)
    return headdict, newdata


# 存储star文件，支持原数据存储和简洁数据存储
def savestar(filename, headdict, data, simple=1):
    file = open(filename, 'w')
    if simple == 1:
        headlabel = []
        labelitems = []
        for label in labels:
            if headdict.get(label) != None:
                headlabel.append(label)
                labelitems.append(headdict.get(label, 0))
        file.write('\ndata_\n\nloop_\n')
        for i in range(len(headlabel)):
            file.write('_rln{} #{}\n'.format(headlabel[i], i + 1))
        for item in data:
            for j in labelitems:
                file.write('{}\t'.format(item.split()[j]))
            file.write('\n')
    else:
        file.write('\ndata_\n\nloop_\n')
        head = sorted(headdict.items(), key=operator.itemgetter(1))
        for name, value in head:
            file.write('_rln{} #{}\n'.format(name, value + 1))
        for item in data:
            file.write(item)
    file.close()


def main():
    files = sys.argv[1:]
    dataall = []
    headdict = {}
    for star in files:
        headdict, data = readstarfile(star)
        dataall.extend(data)

    savestar('all.star', headdict, dataall)


if __name__ == '__main__':
    main()

# coding=utf-8
import os
import time


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


class Job:
    def __init__(self, name):
        self.name = name
        self.resolution = ''
        self.parameter = ''
        self.input = ''
        self.ref = ''
        self.ini_high = ''
        self.healpix_order = ''
        self.averagepmax = ''
        self.number = 0

    def getparameter(self):
        f = open(self.name + '/' + 'run_it000_optimiser.star')
        self.parameter = f.readlines()[1]

        ps = self.parameter.split('--')

        for p in ps:
            if p.find('i ') == 0:
                self.input = p.split()[1]
            if p.find('ref ') != -1:
                self.ref = p.split()[1]
            if p.find('ini_high') != -1:
                self.ini_high = p.split()[1]
            if p.find('healpix_order') != -1 and p.find('auto_local') == -1:
                self.healpix_order = p.split()[1]
        f.close()

    def getmodel(self):
        f = open(self.name + '/' + 'run_model.star')
        lines = f.readlines()
        for line in lines:
            if line.find('_rlnAveragePmax') != -1:
                self.averagepmax = line.split()[1]
            if line.find('_rlnCurrentResolution') != -1:
                self.resolution = line.split()[1]
            if line.find('data_model_classes') != -1:
                break
        f.close()

    def getnum(self):
        headdict, data = readstarfile(self.name + '/' + 'run_data.star')
        self.number = len(data)

    def getresult(self):
        try:
            self.getparameter()
        except IOError, e:
            print(self.name + " is empty")
            return
        try:
            self.getmodel()
            self.getnum()
        except IOError, e:
            print self.name + " don't have result"


names = []

path = os.listdir(os.getcwd())

for p in path:
    if os.path.isdir(p):
        names.append(p)

# print names
names.sort()
# print names

outfile = open('result.txt', 'w')

outfile.write(
    '{:8s} \t{:40s} \t{:20s} \t{:8s} \t{:8s} \t{:8s} \t{:8s}\n'.format('jobname', 'input', 'ref', 'ini_high',
                                                                       'healpix_order',
                                                                       'number', 'resolution'))

for name in names:
    job = Job(name)
    job.getresult()
    outfile.write(
        '{:8s} \t{:40s} \t{:20s} \t{:8s} \t{:8s} \t{:8d} \t{:8s}\t'.format(name, job.input, job.ref, job.ini_high,
                                                                           job.healpix_order,
                                                                           job.number, job.resolution))

    outfile.write('\n')
outfile.close()

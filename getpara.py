# coding=utf-8
import os
import time


class Job:
    def __init__(self, name):
        self.name = name
        self.classes = []
        self.parameter = ''
        self.healpix_order = ''
        self.averagepmax = ''
        self.sigma_ang = ''
        self.offset_range = ''
        self.offset_step = ''

    def getparameter(self):
        try:
            file = open(self.name + '/' + 'run_ct1_it001_optimiser.star')
            self.parameter = file.readlines()[1]

            ps = self.parameter.split('--')

            for p in ps:
                if p.find('healpix_order') != -1:
                    self.healpix_order = p.split()[1]
                if p.find('sigma_ang') != -1:
                    self.sigma_ang = p.split()[1]
                if p.find('offset_range') != -1:
                    self.offset_range = p.split()[1]
                if p.find('offset_step') != -1:
                    self.offset_step = p.split()[1]
            file.close()
        except IOError as e:
            print(self.name + "is empty")

    def getmodel(self):
        try:
            file = open(self.name + '/' + 'run_ct1_it002_model.star')
            lines = file.readlines()
            for line in lines:
                if line.find('_rlnAveragePmax') != -1:
                    self.averagepmax = line.split()[1]
                if line.find('.mrc') != -1:
                    self.classes.append(line.split()[1])
                if line.find('data_model_class_1') != -1:
                    break
            file.close()
        except IOError as e:
            print(self.name + " don't have result")


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
    '{:8s} \t{:13s} \t{:8s} \t{:13s} \t{:13s} \t{:13s} \t{:8s}\n'.format('jobname', 'healpix_order', 'sigma_ang',
                                                                         'offset_range', 'offset_step', 'averagePmax',
                                                                         'classes'))

for name in names:
    job = Job(name)
    job.getparameter()
    job.getmodel()
    clsdis = [[0] * 2 for i in range(len(job.classes))]
    print(clsdis)
    headdict, data = readstarfile(job.name + '/' + 'run_ct1_it002_data.star')
    for line in data:
        item = line.split()
        if item[headdict['ImageName']].find('_a.mrcs') != -1:
            clsdis[int(item[int(headdict['ClassNumber'])]) - 1][0] += 1
        else:
            clsdis[int(item[int(headdict['ClassNumber'])]) - 1][1] += 1
    outfile.write(
        '{:8s} \t{:13s} \t{:8s} \t{:13s} \t{:13s} \t{:13s}\t'.format(name, job.healpix_order,
                                                                     job.sigma_ang, job.offset_range, job.offset_step,
                                                                     job.averagepmax))
    for cls in job.classes:
        outfile.write('{:8s}\t'.format(cls))
    for dis in clsdis:
        outfile.write('{:20d}\t'.format(dis))
    outfile.write('\n')
outfile.close()

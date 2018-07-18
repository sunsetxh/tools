import os
import time


class Job:
    def __init__(self, name):
        self.name = name
        self.classes = []
        self.parameter = ''
        self.input = ''
        self.ref = ''
        self.ini_high = ''
        self.healpix_order = ''
        self.averagepmax = ''
        self.sigma_ang = ''

    def getparameter(self):
        try:
            file = open(self.name + '/' + 'run_it000_optimiser.star')
            self.parameter = file.readlines()[1]

            ps = self.parameter.split('--')

            for p in ps:
                if p.find('i ') == 0:
                    self.input = p.split()[1]
                if p.find('ref') != -1:
                    self.ref = p.split()[1]
                if p.find('ini_high') != -1:
                    self.ini_high = p.split()[1]
                if p.find('healpix_order') != -1:
                    self.healpix_order = p.split()[1]
                if p.find('sigma_ang') != -1:
                    self.sigma_ang = p.split()[1]
            file.close()
        except IOError, e:
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
                    break;
            file.close()
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
    '{:8s} \t{:40s} \t{:20s} \t{:8s} \t{:13s} \t{:8s} \t{:8s} \t{:8s}\n'.format('jobname', 'input', 'ref', 'ini_high',
                                                                                'healpix_order', 'sigma_ang',
                                                                                'averagePmax', 'classes'))

for name in names:
    job = Job(name)
    job.getparameter()
    job.getmodel()
    outfile.write(
        '{:8s} \t{:40s} \t{:20s} \t{:8s} \t{:13s} \t{:8s} \t{:8s}\t'.format(name, job.input, job.ref, job.ini_high,
                                                                            job.healpix_order,
                                                                            job.sigma_ang, job.averagepmax))
    for cls in job.classes:
        outfile.write('{:8s}\t'.format(cls))

    outfile.write('\n')
outfile.close()

import sys

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve

# test = np.hstack((np.zeros(10000), np.ones(10000)))
# print(len(test))
score = []
test = []
weight = []
count = 0

inputname=sys.argv[1]

ADP = open(inputname, 'r')
for line in ADP:
    items = line.split()
    test.append(int(items[1]))
    score.append(float(items[6]))
    # weight.append(10000.0/float(items[5]))
ADP.close()

# ATP=open('diff2_ATP_10000.txt','r')
# for line in ATP:
#     items=line.split()
#     test.append(int(items[1]))
#     score.append(float(items[6]))
# ATP.close()

average_precision = average_precision_score(test, score)
print(average_precision)

precision, recall, _ = precision_recall_curve(test, score)

plt.step(recall, precision, color='b', alpha=0.2,
         where='post')
plt.fill_between(recall, precision, step='post', alpha=0.2,
                 color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
    average_precision))
plt.savefig('{}.png'.format(inputname.split('.')[0]))
#plt.show()


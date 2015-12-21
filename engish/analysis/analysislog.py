# -*- coding: utf-8 -*-
__author__ = 'luocheng'
import re
from collections import defaultdict
validUsers = ('2015011253','2015011319','2015011246','2015011318','2012011880','2015011315')



# calibration -userid ,jobid

calibration = defaultdict(lambda:defaultdict(lambda:[0.0,0.0]))
# calibration -userid ,jobid,docid
estimation = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:-1)))

reading = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:[0.0,0.0])))


etp = re.compile(r'ET=(.*?)\t')
cdp = re.compile(r'CURRENT_DOC=(.*?)\t')
tp = re.compile(r'TIMESTAMP=(.*?)\t')


for line in open('../data/pilot.csv').readlines()[1:]:
    id,studentid,jobid,action,content = line.strip().split(',')
    if studentid in validUsers:
        if action == 'BEGIN_CALIBRATION':
            time = int(tp.search(content+'\t').group(1))
            calibration[studentid][jobid][0] = time
        if action =='END_CALIBRATION':
            time = int(tp.search(content+'\t').group(1))
            calibration[studentid][jobid][1] = time
        if action == 'TIME_ESTIMATION':
            docid = int(cdp.search(content+'\t').group(1).split(' ')[0])
            et = int(etp.search(content+'\t').group(1))
            # print studentid,jobid,docid,et
            estimation[studentid][jobid][docid] = et
        if action == 'BEGIN_READING':
            # newdocid = cdp = re.compile(r'CURRENT_DOC=(.*?)')
            # print content
            docid = int(cdp.search(content+'\t').group(1))
            time = int(tp.search(content+'\t').group(1))
            reading[studentid][jobid][docid][0] = time

        if action == 'END_READING':
            # newdocid = cdp = re.compile(r'CURRENT_DOC=(.*?)')
            docid = int(cdp.search(content+'\t').group(1))
            time = int(tp.search(content+'\t').group(1))
            reading[studentid][jobid][docid][1] = time

fout = open('../data/organized.csv','w')
for studentid in  validUsers:
    items = []
    items.append(studentid)
    for j in ['0','1','2','3','4']:
        items.append(str((calibration[studentid][j][1]-calibration[studentid][j][0])/1000.0))
        for d in [1,2,3,4]:
            items.append(str((reading[studentid][j][d][1]-reading[studentid][j][d][0])/1000.0))
            items.append(str((estimation[studentid][j][d])))
    fout.write(','.join(items))
    fout.write('\n')

fout.close()







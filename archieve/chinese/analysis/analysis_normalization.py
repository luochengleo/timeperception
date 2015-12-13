__author__ = 'franky'
import re
from collections import defaultdict
import numpy as np
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

calibration_time = defaultdict(lambda: defaultdict(lambda: 0.0))
dwell_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
ratio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

for studentid in validUsers:
    for j in ['1', '2', '3', '4']:
        calibration_time[studentid][j] = (calibration[studentid][j][1]-calibration[studentid][j][0])/1000.0
        for d in [1, 2, 3, 4]:
            dwell_time[studentid][j][d] = (reading[studentid][j][d][1]-reading[studentid][j][d][0])/1000.0
            estimated_time[studentid][j][d] = estimation[studentid][j][d]
            ratio[studentid][j][d] = estimated_time[studentid][j][d]/dwell_time[studentid][j][d]


def normalization_by_user_and_job():
    fout = open('../data/normalization_by_user_and_job.csv', 'w')
    for studentid in validUsers:
        items = []
        items.append(studentid)
        for j in ['1', '2', '3', '4']:
            items.append(str(calibration_time[studentid][j]))
            ratios = []
            for d in [1, 2, 3, 4]:
                ratios.append(ratio[studentid][j][d])
            ave = np.mean(ratios)
            stda = np.std(ratios)
            for d in [1, 2, 3, 4]:
                items.append(str((ratio[studentid][j][d]-ave)/stda))
        fout.write(','.join(items))
        fout.write('\n')
    fout.close()


def normalization_by_user():
    fout = open('../data/normalization_by_user.csv', 'w')
    for studentid in validUsers:
        items = []
        items.append(studentid)
        ratios = []
        for j in ['1', '2', '3', '4']:
            for d in [1, 2, 3, 4]:
                ratios.append(ratio[studentid][j][d])
        ave = np.mean(ratios)
        stda = np.std(ratios)
        for j in ['1', '2', '3', '4']:
            items.append(str(calibration_time[studentid][j]))
            for d in [1, 2, 3, 4]:
                items.append(str((ratio[studentid][j][d]-ave)/stda))
        fout.write(','.join(items))
        fout.write('\n')
    fout.close()


def normalization_by_job():
    fout = open('../data/normalization_by_job.csv', 'w')
    ratios = defaultdict(lambda: [])
    for studentid in validUsers:
        for j in ['1', '2', '3', '4']:
            for d in [1, 2, 3, 4]:
                ratios[j].append(ratio[studentid][j][d])
    ratios_ave = {}
    ratios_std = {}
    for j in ['1', '2', '3', '4']:
        ratios_ave[j] = np.mean(ratios[j])
        ratios_std[j] = np.std(ratios[j])
    for studentid in validUsers:
        items = []
        items.append(studentid)
        for j in ['1', '2', '3', '4']:
            items.append(str(calibration_time[studentid][j]))
            for d in [1, 2, 3, 4]:
                items.append(str((ratio[studentid][j][d]-ratios_ave[j])/ratios_std[j]))
        fout.write(','.join(items))
        fout.write('\n')
    fout.close()


normalization_by_user_and_job()
normalization_by_user()
normalization_by_job()

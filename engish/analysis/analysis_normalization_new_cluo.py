# -*- coding: utf-8 -*-
__author__ = 'franky'
import re
from collections import defaultdict
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import random

validUsers = {'2015012620': 1, '2015012618': 2, '2015012674': 3, '2014011319': 4, '2015012625': 5, '2015012676': 6,
              '2015012609': 7, '2015012811': 8, '2015012653': 9, '2015012679': 10, '2015012617': 11, '2015012828': 12,
              '2015012642': 13, '2015012624': 14, '2014012759': 15, '2012012767': 16, '2015012623': 17,
              '2014012772': 18, '2015012610': 19, '2011012756': 20, '2014012780': 21, '2015012622': 22,
              '2015012649': 23, '2015011043': 24}


# 估计的时间
estimation = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1))))
# 估计的relevance
relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
# begin 时间和ending的时间和relevance annotation的时间
reading_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0])))
# range 方法的low和high
range_low = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
range_high = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))

# import settings
job_setting = defaultdict(lambda: defaultdict(lambda: ''))
for line in open('../data/job_settings.csv').readlines()[1:]:
    id, jobid, settingid, taskid, docseq = line.strip().split(',')
    job_setting[int(settingid)][taskid] = docseq

# read logs
cdp = re.compile(r'CURRENT_DOC=(.*?)\t')
tp = re.compile(r'TIMESTAMP=(.*?)\t')
relp = re.compile(r'REL=(.*?)\t')
segp = re.compile(r'Segments=(.*?)\t')
rangep = re.compile(r'Range=(.*?)\t')
relap = re.compile(r'Relative=(.*?)\t')
for line in open('../data/log20151227.csv').readlines()[1:]:
    id = line.strip().split(',')[0]
    studentid = line.strip().split(',')[1]
    jobid = line.strip().split(',')[2]
    action = line.strip().split(',')[3]
    content = line.strip().split(',')[4]
    if studentid in validUsers:
        if action == 'BEGIN_READING':
            doc_rank = int(cdp.search(content + '\t').group(1))
            time = int(tp.search(content + '\t').group(1))
            reading_time[studentid][jobid][doc_rank][0] = time
            # 时刻记得维护一个最新时间戳,避免日志丢失造成大的时间错误
            if doc_rank < 4:
                reading_time[studentid][jobid][doc_rank + 1][0] = time
            if doc_rank > 1 and reading_time[studentid][jobid][doc_rank - 1][1] == 0.0:
                reading_time[studentid][jobid][doc_rank - 1][1] = time
            if doc_rank > 1 and reading_time[studentid][jobid][doc_rank - 1][2] == 0.0:
                reading_time[studentid][jobid][doc_rank - 1][2] = time

        if action == 'END_READING':
            doc_rank = int(cdp.search(content + '\t').group(1))
            time = int(tp.search(content + '\t').group(1))
            reading_time[studentid][jobid][doc_rank][1] = time
            if doc_rank < 4:
                reading_time[studentid][jobid][doc_rank + 1][0] = time
            if doc_rank > 1 and reading_time[studentid][jobid][doc_rank - 1][1] == 0.0:
                reading_time[studentid][jobid][doc_rank - 1][1] = time
            if doc_rank > 1 and reading_time[studentid][jobid][doc_rank - 1][2] == 0.0:
                reading_time[studentid][jobid][doc_rank - 1][2] = time

        if action == 'RELEVANCE_ANNOTATION':
            doc_rank = int(cdp.search(content + '\t').group(1).split(' ')[0])
            time = int(tp.search(content + '\t').group(1))
            reading_time[studentid][jobid][doc_rank][2] = time
            rel = int(relp.search(content + '\t').group(1).split(' ')[0])
            relevance[studentid][jobid][doc_rank] = rel
            if doc_rank < 4:
                reading_time[studentid][jobid][doc_rank + 1][0] = time
            if doc_rank > 1 and reading_time[studentid][jobid][doc_rank - 1][1] == 0.0:
                reading_time[studentid][jobid][doc_rank - 1][1] = time
            if doc_rank > 1 and reading_time[studentid][jobid][doc_rank - 1][2] == 0.0:
                reading_time[studentid][jobid][doc_rank - 1][2] = time

        if action == 'TIME_1':
            seg = segp.search(content + '\t').group(1).split(' ')[0]
            point1, point2, point3, _ = seg.split('_')
            point1 = int(point1)
            point2 = int(point2)
            point3 = int(point3)
            estimation['segments'][studentid][jobid][1] = point1
            estimation['segments'][studentid][jobid][2] = point2 - point1
            estimation['segments'][studentid][jobid][3] = point3 - point2
            estimation['segments'][studentid][jobid][4] = 1000 - point3

        if action == 'TIME2':
            ran = rangep.search(content + '\t').group(1).split(' ')[0]
            _, min1, max1, min2, max2, min3, max3, min4, max4, _ = ran.split('_')
            '''# 几何平均数
            mean1 = np.sqrt(int(min1) * 10 * int(max1) * 10)
            if mean1 == 0.0:
                mean1 = 1.0
            mean2 = np.sqrt(int(min2) * 10 * int(max2) * 10)
            if mean2 == 0.0:
                mean2 = 1.0
            mean3 = np.sqrt(int(min3) * 10 * int(max3) * 10)
            if mean3 == 0.0:
                mean3 = 1.0
            mean4 = np.sqrt(int(min4) * 10 * int(max4) * 10)
            if mean4 == 0.0:
                mean4 = 1.0'''
            # 算术平均数
            mean1 = (int(min1) * 10 + int(max1) * 10) / 2
            mean2 = (int(min2) * 10 + int(max2) * 10) / 2
            mean3 = (int(min3) * 10 + int(max3) * 10) / 2
            mean4 = (int(min4) * 10 + int(max4) * 10) / 2
            range_low[studentid][jobid][1] = int(min1) * 10
            range_low[studentid][jobid][2] = int(min2) * 10
            range_low[studentid][jobid][3] = int(min3) * 10
            range_low[studentid][jobid][4] = int(min4) * 10
            range_high[studentid][jobid][1] = int(max1) * 10
            range_high[studentid][jobid][2] = int(max2) * 10
            range_high[studentid][jobid][3] = int(max3) * 10
            range_high[studentid][jobid][4] = int(max4) * 10
            estimation['range'][studentid][jobid][1] = mean1
            estimation['range'][studentid][jobid][2] = mean2
            estimation['range'][studentid][jobid][3] = mean3
            estimation['range'][studentid][jobid][4] = mean4

        if action == 'TIME3':
            rela = relap.search(content + '\t').group(1).split(' ')[0]
            doc1, doc2, doc3, doc4, _ = rela.split('_')
            estimation['relative'][studentid][jobid][1] = int(doc1)
            estimation['relative'][studentid][jobid][2] = int(doc2)
            estimation['relative'][studentid][jobid][3] = int(doc3)
            estimation['relative'][studentid][jobid][4] = int(doc4)

# task2-task5, dwell_time, estimated_time, perceived_relevance
# dwell_time    student id | jobid  | docid |
dwell_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1))))
perceived_relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
relevance_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            dwell_time[studentid][j][d] = (reading_time[studentid][j][d][1] - reading_time[studentid][j][d][0]) / 1000.0
            perceived_relevance[studentid][j][d] = relevance[studentid][j][d]
            relevance_time[studentid][j][d] = (reading_time[studentid][j][d][2] - reading_time[studentid][j][d][1]) / 1000.0
            for time_method in ['segments', 'range', 'relative']:
                estimated_time[time_method][studentid][j][d] = float(estimation[time_method][studentid][j][d])
# compute average dwell_time and relevance_time
total_dwell_time = 0
total_relevance_time = 0
total_num = 0
for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            total_num += 1
            total_dwell_time += dwell_time[studentid][j][d]
            total_relevance_time += relevance_time[studentid][j][d]
print "average dwell time:", total_dwell_time / total_num, "average relevance time:", total_relevance_time / total_num


# relevance_filling
for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        docseq_ = job_setting[validUsers[studentid]][j]
        for d in [1, 2, 3, 4]:
            docid = int(docseq_.split('-')[d - 1])
            if perceived_relevance[studentid][j][d] == -1:
                if docid > 3:
                    perceived_relevance[studentid][j][d] = 0
                else:
                    perceived_relevance[studentid][j][d] = 3

# relevance agreement
relevance_agreement = defaultdict(lambda: defaultdict(lambda: 0.0))
relevance_agree_num = defaultdict(lambda: defaultdict(lambda: 0))


def output_csv():
    fout = open('../data/output.csv', 'w')
    fout.write("studentid,taskid,docid,docrank,perceived relevance,dwell time,time1,time2_low,time2_high,time3\n")
    for studentid in validUsers:
        for taskid in ['2', '3', '4', '5']:
            for docrank in [1, 2, 3, 4]:
                fout.write(studentid + ',')
                fout.write(taskid + ',')
                docseq_ = job_setting[validUsers[studentid]][taskid]
                docid = int(docseq_.split('-')[docrank-1])
                fout.write(str(docid) + ',' + str(docrank) + ',' + str(perceived_relevance[studentid][taskid][docrank]) + ',' + str(round(dwell_time[studentid][taskid][docrank], 1)) + ',' + str(estimated_time['segments'][studentid][taskid][docrank]) + ',' + str(range_low[studentid][taskid][docrank]) + ',' + str(range_high[studentid][taskid][docrank]) + ',' + str(estimated_time['relative'][studentid][taskid][docrank]) + '\n')

    fout.close()

# output_csv()
# 计算用户的relevance 和我们设定的relevance是不是一致？


def compute_relevance_agreement():
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            for studentid in validUsers:
                docseq_ = job_setting[validUsers[studentid]][j]
                docid = int(docseq_.split('-')[d - 1])
                if (docid < 4 and perceived_relevance[studentid][j][d] > 1) or (
                        docid > 3 and perceived_relevance[studentid][j][d] < 2):
                    relevance_agree_num[j][docid] += 1
        for docid in [1, 2, 4, 5]:
            relevance_agreement[j][docid] = relevance_agree_num[j][docid] / 24.0
            print j, docid, relevance_agreement[j][docid]


# compute_relevance_agreement()

# print dwell time, estimated time, perceived relevance
'''for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            print studentid, j, d, dwell_time[studentid][j][d]
            for time_method in ['segments', 'range', 'relative']:
                print time_method, studentid, j, d, estimated_time[time_method][studentid][j][d]
for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            print studentid, j, d, perceived_relevance[studentid][j][d]'''

# perceived relevant and irrelevant docs
relevant_doc_ranks = defaultdict(lambda: defaultdict(lambda: []))
irrelevant_doc_ranks = defaultdict(lambda: defaultdict(lambda: []))
for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            if perceived_relevance[studentid][j][d] < 2:
                irrelevant_doc_ranks[studentid][j].append(d)
            else:
                relevant_doc_ranks[studentid][j].append(d)
# full sample
# relevant & relevant
rr_de_agree_full_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
rr_de_total_full_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
rr_e1e2_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e3_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e2e3_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e2_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e3_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e2e3_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
# relevant & irrelevant
ri_de_agree_full_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ri_de_total_full_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ri_e1e2_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e3_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e2e3_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e2_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e3_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e2e3_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
# irrelevant & irrelevant
ii_de_agree_full_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ii_de_total_full_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ii_e1e2_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e3_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e2e3_agree_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e2_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e3_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e2e3_total_full_num = defaultdict(lambda: defaultdict(lambda: 0))

# discriminative sample
# relevant & relevant
rr_de_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
rr_de_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
rr_e1e2_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e3_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e2e3_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e2_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e3_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e2e3_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
# relevant & irrelevant
ri_de_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ri_de_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ri_e1e2_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e3_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e2e3_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e2_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e3_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e2e3_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
# irrelevant & irrelevant
ii_de_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ii_de_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ii_e1e2_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e3_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e2e3_agree_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e2_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e3_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e2e3_total_discriminative_num = defaultdict(lambda: defaultdict(lambda: 0))


def analyze_pairwise_agreement():
    for studentid in validUsers:
        for j in ['2', '3', '4', '5']:
            # relevant & relevant
            for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                    doc1 = relevant_doc_ranks[studentid][j][d1]
                    doc2 = relevant_doc_ranks[studentid][j][d2]
                    # dtime & etime(3 methods)
                    for time_method in ['segments', 'range', 'relative']:
                        rr_de_total_full_num[time_method][studentid][j] += 1
                        if (dwell_time[studentid][j][doc1] <= dwell_time[studentid][j][doc2] and
                                    estimated_time[time_method][studentid][j][doc1] <=
                                    estimated_time[time_method][studentid][j][doc2]) or (
                                dwell_time[studentid][j][doc1] >= dwell_time[studentid][j][doc2] and
                                estimated_time[time_method][studentid][j][doc1] >=
                                estimated_time[time_method][studentid][j][doc2]):
                            rr_de_agree_full_num[time_method][studentid][j] += 1
                    # segments & range
                    rr_e1e2_total_full_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                        doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][
                        doc2]) or (
                            estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['range'][studentid][j][doc1] >=
                        estimated_time['range'][studentid][j][doc2]):
                        rr_e1e2_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        rr_e1e2_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][
                            doc2]) or (
                                estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                                doc2] and estimated_time['range'][studentid][j][doc1] >=
                            estimated_time['range'][studentid][j][doc2]):
                            rr_e1e2_agree_discriminative_num[studentid][j] += 1
                    # segments & relative
                    rr_e1e3_total_full_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                        doc2] and estimated_time['relative'][studentid][j][doc1] <=
                        estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                        rr_e1e3_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        rr_e1e3_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] <=
                            estimated_time['relative'][studentid][j][doc2]) or (
                                estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                                doc2] and estimated_time['relative'][studentid][j][doc1] >=
                            estimated_time['relative'][studentid][j][doc2]):
                            rr_e1e3_agree_discriminative_num[studentid][j] += 1
                    # range & relative
                    rr_e2e3_total_full_num[studentid][j] += 1
                    if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and
                                estimated_time['relative'][studentid][j][doc1] <=
                                estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                        rr_e2e3_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        rr_e2e3_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and
                                estimated_time['relative'][studentid][j][doc1] <=
                                estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                            rr_e2e3_agree_discriminative_num[studentid][j] += 1

            # relevant & irrelevant
            for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    doc1 = relevant_doc_ranks[studentid][j][d1]
                    doc2 = irrelevant_doc_ranks[studentid][j][d2]
                    # dtime & etime(3 methods)
                    for time_method in ['segments', 'range', 'relative']:
                        ri_de_total_full_num[time_method][studentid][j] += 1
                        if (dwell_time[studentid][j][doc1] <= dwell_time[studentid][j][doc2] and
                                    estimated_time[time_method][studentid][j][doc1] <=
                                    estimated_time[time_method][studentid][j][doc2]) or (
                                dwell_time[studentid][j][doc1] >= dwell_time[studentid][j][doc2] and
                                estimated_time[time_method][studentid][j][doc1] >=
                                estimated_time[time_method][studentid][j][doc2]):
                            ri_de_agree_full_num[time_method][studentid][j] += 1
                    # segments & range
                    ri_e1e2_total_full_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                        doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][
                        doc2]) or (
                            estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['range'][studentid][j][doc1] >=
                        estimated_time['range'][studentid][j][doc2]):
                        ri_e1e2_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        ri_e1e2_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][
                            doc2]) or (
                                estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                                doc2] and estimated_time['range'][studentid][j][doc1] >=
                            estimated_time['range'][studentid][j][doc2]):
                            ri_e1e2_agree_discriminative_num[studentid][j] += 1
                    # segments & relative
                    ri_e1e3_total_full_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                        doc2] and estimated_time['relative'][studentid][j][doc1] <=
                        estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                        ri_e1e3_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        ri_e1e3_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] <=
                            estimated_time['relative'][studentid][j][doc2]) or (
                                estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                                doc2] and estimated_time['relative'][studentid][j][doc1] >=
                            estimated_time['relative'][studentid][j][doc2]):
                            ri_e1e3_agree_discriminative_num[studentid][j] += 1
                    # range & relative
                    ri_e2e3_total_full_num[studentid][j] += 1
                    if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and
                                estimated_time['relative'][studentid][j][doc1] <=
                                estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                        ri_e2e3_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        ri_e2e3_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and
                                estimated_time['relative'][studentid][j][doc1] <=
                                estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                            ri_e2e3_agree_discriminative_num[studentid][j] += 1

            # irrelevant & irrelevant
            for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                    doc1 = irrelevant_doc_ranks[studentid][j][d1]
                    doc2 = irrelevant_doc_ranks[studentid][j][d2]
                    # dtime & etime(3 methods)
                    for time_method in ['segments', 'range', 'relative']:
                        ii_de_total_full_num[time_method][studentid][j] += 1
                        if (dwell_time[studentid][j][doc1] <= dwell_time[studentid][j][doc2] and
                                    estimated_time[time_method][studentid][j][doc1] <=
                                    estimated_time[time_method][studentid][j][doc2]) or (
                                dwell_time[studentid][j][doc1] >= dwell_time[studentid][j][doc2] and
                                estimated_time[time_method][studentid][j][doc1] >=
                                estimated_time[time_method][studentid][j][doc2]):
                            ii_de_agree_full_num[time_method][studentid][j] += 1
                    # segments & range
                    ii_e1e2_total_full_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                        doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][
                        doc2]) or (
                            estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['range'][studentid][j][doc1] >=
                        estimated_time['range'][studentid][j][doc2]):
                        ii_e1e2_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        ii_e1e2_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][
                            doc2]) or (
                                estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                                doc2] and estimated_time['range'][studentid][j][doc1] >=
                            estimated_time['range'][studentid][j][doc2]):
                            ii_e1e2_agree_discriminative_num[studentid][j] += 1
                    # segments & relative
                    ii_e1e3_total_full_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                        doc2] and estimated_time['relative'][studentid][j][doc1] <=
                        estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                        ii_e1e3_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        ii_e1e3_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] <=
                            estimated_time['relative'][studentid][j][doc2]) or (
                                estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][
                                doc2] and estimated_time['relative'][studentid][j][doc1] >=
                            estimated_time['relative'][studentid][j][doc2]):
                            ii_e1e3_agree_discriminative_num[studentid][j] += 1
                    # range & relative
                    ii_e2e3_total_full_num[studentid][j] += 1
                    if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and
                                estimated_time['relative'][studentid][j][doc1] <=
                                estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                        ii_e2e3_agree_full_num[studentid][j] += 1
                    if abs(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) > min(dwell_time[studentid][j][doc1], dwell_time[studentid][j][doc2]) * 0.2:
                        ii_e2e3_total_discriminative_num[studentid][j] += 1
                        if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and
                                estimated_time['relative'][studentid][j][doc1] <=
                                estimated_time['relative'][studentid][j][doc2]) or (
                            estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][
                            doc2] and estimated_time['relative'][studentid][j][doc1] >=
                        estimated_time['relative'][studentid][j][doc2]):
                            ii_e2e3_agree_discriminative_num[studentid][j] += 1


# analyze_pairwise_agreement()


def compute_pairwise_agreement():
    fout = open('../data/pairwise_agreement.csv', 'w')
    fout.write(
        "studentid,SG|RG,SG|RC,RG|RC,SG|RG,SG|RC,RG|RC")
    fout.write('\n')
    for studentid in validUsers:
        fout.write(studentid + ',')
        e1e2_agree_full_num_all_tasks = 0
        e1e2_total_full_num_all_tasks = 0
        e1e3_agree_full_num_all_tasks = 0
        e1e3_total_full_num_all_tasks = 0
        e2e3_agree_full_num_all_tasks = 0
        e2e3_total_full_num_all_tasks = 0

        e1e2_agree_discriminative_num_all_tasks = 0
        e1e2_total_discriminative_num_all_tasks = 0
        e1e3_agree_discriminative_num_all_tasks = 0
        e1e3_total_discriminative_num_all_tasks = 0
        e2e3_agree_discriminative_num_all_tasks = 0
        e2e3_total_discriminative_num_all_tasks = 0

        for j in ['2', '3', '4', '5']:
            e1e2_agree_full_num_all_tasks += (rr_e1e2_agree_full_num[studentid][j] + ri_e1e2_agree_full_num[studentid][j] + ii_e1e2_agree_full_num[studentid][j])
            e1e2_total_full_num_all_tasks += (rr_e1e2_total_full_num[studentid][j] + ri_e1e2_total_full_num[studentid][j] + ii_e1e2_total_full_num[studentid][j])
            e1e3_agree_full_num_all_tasks += (rr_e1e3_agree_full_num[studentid][j] + ri_e1e3_agree_full_num[studentid][j] + ii_e1e3_agree_full_num[studentid][j])
            e1e3_total_full_num_all_tasks += (rr_e1e3_total_full_num[studentid][j] + ri_e1e3_total_full_num[studentid][j] + ii_e1e3_total_full_num[studentid][j])
            e2e3_agree_full_num_all_tasks += (rr_e2e3_agree_full_num[studentid][j] + ri_e2e3_agree_full_num[studentid][j] + ii_e2e3_agree_full_num[studentid][j])
            e2e3_total_full_num_all_tasks += (rr_e2e3_total_full_num[studentid][j] + ri_e2e3_total_full_num[studentid][j] + ii_e2e3_total_full_num[studentid][j])

            e1e2_agree_discriminative_num_all_tasks += (rr_e1e2_agree_discriminative_num[studentid][j] + ri_e1e2_agree_discriminative_num[studentid][j] + ii_e1e2_agree_discriminative_num[studentid][j])
            e1e2_total_discriminative_num_all_tasks += (rr_e1e2_total_discriminative_num[studentid][j] + ri_e1e2_total_discriminative_num[studentid][j] + ii_e1e2_total_discriminative_num[studentid][j])
            e1e3_agree_discriminative_num_all_tasks += (rr_e1e3_agree_discriminative_num[studentid][j] + ri_e1e3_agree_discriminative_num[studentid][j] + ii_e1e3_agree_discriminative_num[studentid][j])
            e1e3_total_discriminative_num_all_tasks += (rr_e1e3_total_discriminative_num[studentid][j] + ri_e1e3_total_discriminative_num[studentid][j] + ii_e1e3_total_discriminative_num[studentid][j])
            e2e3_agree_discriminative_num_all_tasks += (rr_e2e3_agree_discriminative_num[studentid][j] + ri_e2e3_agree_discriminative_num[studentid][j] + ii_e2e3_agree_discriminative_num[studentid][j])
            e2e3_total_discriminative_num_all_tasks += (rr_e2e3_total_discriminative_num[studentid][j] + ri_e2e3_total_discriminative_num[studentid][j] + ii_e2e3_total_discriminative_num[studentid][j])

        print "full sample total number", e1e2_total_full_num_all_tasks, e1e3_total_full_num_all_tasks, e2e3_total_full_num_all_tasks
        print "discriminative sample", e1e2_total_discriminative_num_all_tasks, e1e3_total_discriminative_num_all_tasks, e2e3_total_discriminative_num_all_tasks

        items = [
            round(float(e1e2_agree_full_num_all_tasks) / float(e1e2_total_full_num_all_tasks), 3),
            round(float(e1e3_agree_full_num_all_tasks) / float(e1e3_total_full_num_all_tasks), 3),
            round(float(e2e3_agree_full_num_all_tasks) / float(e2e3_total_full_num_all_tasks), 3),
            round(float(e1e2_agree_discriminative_num_all_tasks) / float(e1e2_total_discriminative_num_all_tasks), 3),
            round(float(e1e3_agree_discriminative_num_all_tasks) / float(e1e3_total_discriminative_num_all_tasks), 3),
            round(float(e2e3_agree_discriminative_num_all_tasks) / float(e2e3_total_discriminative_num_all_tasks), 3)
        ]
        fout.write(','.join(str(item) for item in items))
        fout.write('\n')

    fout.close()


# compute_pairwise_agreement()


def compute_kappa():
    predefined = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    fout = open('../data/kappa.csv', 'w')
    k = 0
    for studentid in validUsers:
        perceived = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in ['2', '3', '4', '5']:
            for d in relevant_doc_ranks[studentid][j]:
                docseq_ = job_setting[validUsers[studentid]][j]
                docid = int(docseq_.split('-')[d - 1])
                if docid < 4:
                    perceived[int(j)*4 + docid - 9] = 1
                else:
                    perceived[int(j)*4 + docid - 10] = 1
        yy = 0.0
        yn = 0.0
        ny = 0.0
        nn = 0.0
        for i in range(0, 16):
            if predefined[i] == 1 and perceived[i] == 1:
                yy += 1
            if predefined[i] == 1 and perceived[i] == 0:
                yn += 1
            if predefined[i] == 0 and perceived[i] == 1:
                ny += 1
            if predefined[i] == 0 and perceived[i] == 0:
                nn += 1
        total = 16.0
        po = (yy + nn) / total
        pe = ((yy + yn) / total) * ((yy + ny) / total) + ((nn + yn) / total) * ((nn + ny) / total)
        kappa = (po - pe) / (1 - pe)
        k += 1
        print k, studentid, kappa
        fout.write(str(k) + ',' + str(kappa) + '\n')
    fout.close()

compute_kappa()


# 计算dwell time，比较相关不相关上的差异
def compute_dtime():
    r_dtimes = defaultdict(lambda: [])
    ir_dtimes = defaultdict(lambda: [])
    means_r_dtimes = []
    std_r_dtimes = []
    means_ir_dtimes = []
    std_ir_dtimes = []
    for studentid in validUsers:
        for j in ['2', '3', '4', '5']:
            for d in relevant_doc_ranks[studentid][j]:
                r_dtimes[j].append(dwell_time[studentid][j][d])
            for d in irrelevant_doc_ranks[studentid][j]:
                ir_dtimes[j].append(dwell_time[studentid][j][d])
    for j in ['2', '3', '4', '5']:
        means_r_dtimes.append(np.mean(r_dtimes[j]))
        std_r_dtimes.append(np.std(r_dtimes[j]))
        means_ir_dtimes.append(np.mean(ir_dtimes[j]))
        std_ir_dtimes.append(np.std(ir_dtimes[j]))
        print j, np.mean(r_dtimes[j]), np.std(r_dtimes[j]), np.mean(ir_dtimes[j]), np.std(ir_dtimes[j]), \
        stats.ttest_ind(r_dtimes[j], ir_dtimes[j], equal_var=False)[1]
    '''# plot
    n_groups = 4
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = plt.bar(index, means_r_dtimes, bar_width, alpha=opacity, color='b', yerr=std_r_dtimes,
                     error_kw=error_config, label='R')
    rects2 = plt.bar(index + bar_width, means_ir_dtimes, bar_width, alpha=opacity, color='r', yerr=std_ir_dtimes,
                     error_kw=error_config, label='I')
    plt.xlabel('Task')
    plt.ylabel('Dtime')
    plt.title('')
    plt.xticks(index + bar_width, ('2', '3', '4', '5'))
    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/dwell_time_comparison.png")
    plt.show()'''

#compute_dtime()

# 用perception ratio
rr_perceived_ratios = defaultdict(lambda: [])
ri_perceived_ratios = defaultdict(lambda: [])
ii_perceived_ratios = defaultdict(lambda: [])


def compute_perception_ratio():
    fout = open('../data/log_perception_ratio_significance.csv', 'w')
    for time_method in ['segments', 'range', 'relative']:
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                # relevant & irrelevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ri_perceived_ratios[time_method].append(math.log(perceived_ratio))
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        # 随机调换一下顺序
                        if int(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) % 2 == 0:
                            perceived_ratio = 1 / perceived_ratio
                        rr_perceived_ratios[time_method].append(math.log(perceived_ratio))
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        # 随机调换一下顺序
                        if int(dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]) % 2 == 0:
                            perceived_ratio = 1 / perceived_ratio
                        ii_perceived_ratios[time_method].append(math.log(perceived_ratio))
        fout.write(time_method + ',ri,mean:' + str(round(np.mean(ri_perceived_ratios[time_method]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ri_perceived_ratios[time_method], 0)[1], 3)) + '\n')
        fout.write(time_method + ',rr,mean:' + str(round(np.mean(rr_perceived_ratios[time_method]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(rr_perceived_ratios[time_method], 0)[1], 3)) + '\n')
        fout.write(time_method + ',ii,mean:' + str(round(np.mean(ii_perceived_ratios[time_method]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ii_perceived_ratios[time_method], 0)[1], 3)) + '\n')

        print time_method, "ri", np.mean(ri_perceived_ratios[time_method]), np.std(
                ri_perceived_ratios[time_method]), stats.ttest_1samp(ri_perceived_ratios[time_method], 0)[1]
        print time_method, "rr", np.mean(rr_perceived_ratios[time_method]), np.std(
                    rr_perceived_ratios[time_method]), stats.ttest_1samp(rr_perceived_ratios[time_method], 0)[1]
        print time_method, "ii", np.mean(ii_perceived_ratios[time_method]), np.std(
                ii_perceived_ratios[time_method]), stats.ttest_1samp(ii_perceived_ratios[time_method], 0)[1]
    fout.close()

    # plot
    index = np.arange(3)
    bar_width = 1
    font = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 16,
    }
    # plt.subplot(1, 3, 1)
    data = [ri_perceived_ratios["segments"], ri_perceived_ratios["range"], ri_perceived_ratios["relative"]]
    # print 'data here'
    # print data
    plt.figure(figsize=(6, 6))
    plt.boxplot(data)
    plt.ylabel("p-ratio", fontdict=font)
    plt.ylim(-1.5, 1.5)
    # plt.xticks(index + bar_width, ("SG", "BD", "RC"), fontsize=16)
    plt.xticks(index + bar_width, ("", "", ""), fontsize=16)
    plt.yticks(fontsize=16)
    # plt.title("<R, I>", fontdict=font)
    plt.scatter([1, ], [np.mean(ri_perceived_ratios["segments"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ri_perceived_ratios["segments"]), 2)) + '0*', xy=(0.9, np.mean(ri_perceived_ratios["segments"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=18)
    plt.scatter([2, ], [np.mean(ri_perceived_ratios["range"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ri_perceived_ratios["range"]), 2)) + '0*', xy=(1.9, np.mean(ri_perceived_ratios["range"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=18)
    plt.scatter([3, ], [np.mean(ri_perceived_ratios["relative"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ri_perceived_ratios["relative"]), 2)), xy=(2.9, np.mean(ri_perceived_ratios["relative"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=18)

    texts = [["-3.979","-3.843","-1.454"],["362","362","362"],["0.209","0.202","0.076"]]
    rows = ["t-stat.","df","effect size"]
    from matplotlib.font_manager import FontProperties
    the_table = plt.table(cellText=texts,rowLabels=rows,colLabels=["SG", "BD", "RC"],loc='bottom',fontsize=16)
    plt.subplots_adjust(left=0.2, bottom=0.2)

    the_table.auto_set_font_size(False)
    the_table.set_fontsize(16)
    for _method in ['segments','range','relative']:
        print '-----------------------------'
        print _method
        print 'df', len(ri_perceived_ratios[_method])-1
        print 'effect size', np.mean(ri_perceived_ratios[_method])/np.std(ri_perceived_ratios[_method])
        print 't-statis',stats.ttest_1samp(ri_perceived_ratios[_method], 0)[0]
        print 'p-vale',stats.ttest_1samp(ri_perceived_ratios[_method], 0)[1]




    '''plt.subplot(1, 3, 2)
    data = [rr_perceived_ratios["segments"], rr_perceived_ratios["range"], rr_perceived_ratios["relative"]]
    plt.boxplot(data)
    plt.ticklabel_format(fontdict=font)
    plt.ylim(-1.5, 1.5)
    plt.xticks(index + bar_width, ("SG", "RG", "RC"), fontsize=16)
    plt.yticks([], [])
    plt.title("<R, R>", fontdict=font)
    plt.scatter([1, ], [np.mean(rr_perceived_ratios["segments"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(rr_perceived_ratios["segments"]), 2)), xy=(0.8, np.mean(rr_perceived_ratios["segments"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([2, ], [np.mean(rr_perceived_ratios["range"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(rr_perceived_ratios["range"]), 2)), xy=(1.8, np.mean(rr_perceived_ratios["range"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([3, ], [np.mean(rr_perceived_ratios["relative"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(rr_perceived_ratios["relative"]), 2)), xy=(2.8, np.mean(rr_perceived_ratios["relative"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)

    plt.subplot(1, 3, 3)
    data = [ii_perceived_ratios["segments"], ii_perceived_ratios["range"], ii_perceived_ratios["relative"]]
    plt.boxplot(data)
    plt.ticklabel_format(fontdict=font)
    plt.ylim(-1.5, 1.5)
    plt.xticks(index + bar_width, ("SG", "RG", "RC"), fontsize=16)
    plt.yticks([], [])
    plt.title("<I, I>", fontdict=font)
    plt.scatter([1, ], [np.mean(ii_perceived_ratios["segments"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ii_perceived_ratios["segments"]), 2)), xy=(0.8, np.mean(ii_perceived_ratios["segments"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([2, ], [np.mean(ii_perceived_ratios["range"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ii_perceived_ratios["range"]), 2)), xy=(1.8, np.mean(ii_perceived_ratios["range"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([3, ], [np.mean(ii_perceived_ratios["relative"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ii_perceived_ratios["relative"]), 2)), xy=(2.8, np.mean(ii_perceived_ratios["relative"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)'''

    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/log_perception_ratio.eps")
    plt.show()

compute_perception_ratio()




# 每个user的perception_ratio的分布
rr_user_perceived_ratios = defaultdict(lambda: defaultdict(lambda: []))
ri_user_perceived_ratios = defaultdict(lambda: defaultdict(lambda: []))
ii_user_perceived_ratios = defaultdict(lambda: defaultdict(lambda: []))


def compute_user_perception_ratio():
    fout = open('../data/log_user_perception_ratio_significance.csv', 'w')
    fout2 = open('../data/log_user_perception_ratio_analysis.csv', 'w')
    fout3 = open('../data/log_user_perception_ratio.csv', 'w')
    for time_method in ['segments', 'range', 'relative']:
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                # relevant & irrelevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ri_user_perceived_ratios[time_method][studentid].append(math.log(perceived_ratio))
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        rr_user_perceived_ratios[time_method][studentid].append(math.log(perceived_ratio))
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ii_user_perceived_ratios[time_method][studentid].append(math.log(perceived_ratio))
        for studentid in validUsers:
            print time_method, studentid, "ri", np.mean(ri_user_perceived_ratios[time_method][studentid]), np.std(
                ri_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(ri_user_perceived_ratios[time_method][studentid], 0)[1]
            fout.write(time_method + ',' + studentid + ',ri,mean:' + str(round(np.mean(ri_user_perceived_ratios[time_method][studentid]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ri_user_perceived_ratios[time_method][studentid], 0)[1], 3)) + '\n')
            '''print time_method, studentid, "rr", np.mean(rr_user_perceived_ratios[time_method][studentid]), np.std(
                rr_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(rr_user_perceived_ratios[time_method][studentid], 1)[1]
            print time_method, studentid, "ii", np.mean(ii_user_perceived_ratios[time_method][studentid]), np.std(
                ii_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(ii_user_perceived_ratios[time_method][studentid], 1)[1]'''
    fout.close()

    # fout3
    fout3.write('user')
    for i in range(1, 25):
        fout3.write(',' + str(i))
    fout3.write('\n')
    fout3.write('SG')
    for i in range(1, 25):
        studentid = validUsers.keys()[i-1]
        if stats.ttest_1samp(ri_user_perceived_ratios['segments'][studentid], 0)[1] < 0.05:
            fout3.write(',' + str(round(np.mean(ri_user_perceived_ratios['segments'][studentid]), 2)) + '*')
        else:
            fout3.write(',' + str(round(np.mean(ri_user_perceived_ratios['segments'][studentid]), 2)))
    fout3.write('\n')
    fout3.write('BD')
    for i in range(1, 25):
        studentid = validUsers.keys()[i-1]
        if stats.ttest_1samp(ri_user_perceived_ratios['range'][studentid], 0)[1] < 0.05:
            fout3.write(',' + str(round(np.mean(ri_user_perceived_ratios['range'][studentid]), 2)) + '*')
        else:
            fout3.write(',' + str(round(np.mean(ri_user_perceived_ratios['range'][studentid]), 2)))
    fout3.write('\n')
    fout3.write('RC')
    for i in range(1, 25):
        studentid = validUsers.keys()[i-1]
        if stats.ttest_1samp(ri_user_perceived_ratios['relative'][studentid], 0)[1] < 0.05:
            fout3.write(',' + str(round(np.mean(ri_user_perceived_ratios['relative'][studentid]), 2)) + '*')
        else:
            fout3.write(',' + str(round(np.mean(ri_user_perceived_ratios['relative'][studentid]), 2)))

    fout3.close()

    # plot
    index = np.arange(3)
    bar_width = 1
    font = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 12,
    }
    plt.figure(figsize=(12, 9))
    for i in range(1, 25):
        plt.subplot(4, 6, i)
        studentid = validUsers.keys()[i-1]
        data = [ri_user_perceived_ratios["segments"][studentid], ri_user_perceived_ratios["range"][studentid], ri_user_perceived_ratios["relative"][studentid]]
        plt.boxplot(data)
        if i % 6 == 1:
            plt.ylabel("p-ratio", fontdict=font)
        else:
            plt.yticks([], [])
        plt.ylim(-1.5, 1.5)
        plt.xticks(index + bar_width, ("SG", "BD", "RC"), fontsize=12)
        plt.yticks(fontsize=12)
        plt.title(str(i), fontdict=font)
        plt.scatter([1, ], [np.mean(ri_user_perceived_ratios["segments"][studentid]), ], 10, color='black')
        if stats.ttest_1samp(ri_user_perceived_ratios["segments"][studentid], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["segments"][studentid]), 2)) + '*', xy=(0.8, np.mean(ri_user_perceived_ratios["segments"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
        else:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["segments"][studentid]), 2)), xy=(0.8, np.mean(ri_user_perceived_ratios["segments"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
        print i, studentid, ",segments,mean:", round(np.mean(ri_user_perceived_ratios["segments"][studentid]), 2)
        for j in ['2', '3', '4', '5']:
            print j, "dtime:", dwell_time[studentid][j], "sg-etime:", estimated_time['segments'][studentid][j]


        plt.scatter([2, ], [np.mean(ri_user_perceived_ratios["range"][studentid]), ], 10, color='black')
        if stats.ttest_1samp(ri_user_perceived_ratios["range"][studentid], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["range"][studentid]), 2)) + '*', xy=(1.8, np.mean(ri_user_perceived_ratios["range"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
        else:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["range"][studentid]), 2)), xy=(1.8, np.mean(ri_user_perceived_ratios["range"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
        print i, studentid, ",range,mean:", round(np.mean(ri_user_perceived_ratios["range"][studentid]), 2)
        for j in ['2', '3', '4', '5']:
            print j, "dtime:", dwell_time[studentid][j], "rg-etime:", estimated_time['range'][studentid][j]

        plt.scatter([3, ], [np.mean(ri_user_perceived_ratios["relative"][studentid]), ], 10, color='black')
        if stats.ttest_1samp(ri_user_perceived_ratios["relative"][studentid], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["relative"][studentid]), 2)) + '*', xy=(2.8, np.mean(ri_user_perceived_ratios["relative"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
        else:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["relative"][studentid]), 2)), xy=(2.8, np.mean(ri_user_perceived_ratios["relative"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
        print i, studentid, ",relative,mean:", round(np.mean(ri_user_perceived_ratios["relative"][studentid]), 2)
        for j in ['2', '3', '4', '5']:
            print j, "dtime:", dwell_time[studentid][j], "rc-etime:", estimated_time['relative'][studentid][j]

        # plt.annotate(str(i), xy=(0.2, 0.8), xytext=(+10, -3), textcoords='offset points', fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/log_user_perception_ratio.eps")
    plt.show()
    fout2.close()

# compute_user_perception_ratio()


# 每个task的perception_ratio的分布
rr_task_perceived_ratios = defaultdict(lambda: defaultdict(lambda: []))
ri_task_perceived_ratios = defaultdict(lambda: defaultdict(lambda: []))
ii_task_perceived_ratios = defaultdict(lambda: defaultdict(lambda: []))


def compute_task_perception_ratio():
    fout = open('../data/log_task_perception_ratio_significance.csv', 'w')
    for time_method in ['segments', 'range', 'relative']:
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                # relevant & irrelevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ri_task_perceived_ratios[time_method][j].append(math.log(perceived_ratio))
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        rr_task_perceived_ratios[time_method][j].append(math.log(perceived_ratio))
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ii_task_perceived_ratios[time_method][j].append(math.log(perceived_ratio))
            print time_method, j, "ri", np.mean(ri_task_perceived_ratios[time_method][j]), np.std(
                ri_task_perceived_ratios[time_method][j]), stats.ttest_1samp(ri_task_perceived_ratios[time_method][j], 0)[1]
            fout.write(time_method + ',' + j + ',ri,mean:' + str(round(np.mean(ri_task_perceived_ratios[time_method][j]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ri_task_perceived_ratios[time_method][j], 0)[1], 3)) + '\n')
            '''print time_method, studentid, "rr", np.mean(rr_user_perceived_ratios[time_method][studentid]), np.std(
                rr_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(rr_user_perceived_ratios[time_method][studentid], 1)[1]
            print time_method, studentid, "ii", np.mean(ii_user_perceived_ratios[time_method][studentid]), np.std(
                ii_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(ii_user_perceived_ratios[time_method][studentid], 1)[1]'''

    fout.close()
    # plot
    index = np.arange(3)
    bar_width = 1
    font = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 14,
    }
    plt.figure(figsize=(8, 8))
    for j in ['2', '3', '4', '5']:

        for _method in ['segments','range','relative']:
                print '-----------------------------'
                print j,_method
                print 'df', len(ri_task_perceived_ratios[_method][j])-1
                print 'effect size', np.mean(ri_task_perceived_ratios[_method][j])/np.std(ri_task_perceived_ratios[_method][j])
                print 't-statis',stats.ttest_1samp(ri_task_perceived_ratios[_method][j], 0)[0]
                print 'p-vale',stats.ttest_1samp(ri_task_perceived_ratios[_method][j], 0)[1]


        plt.subplot(2, 2, int(j)-1)
        data = [ri_task_perceived_ratios["segments"][j], ri_task_perceived_ratios["range"][j], ri_task_perceived_ratios["relative"][j]]
        plt.boxplot(data)
        if int(j)-1 == 1 or int(j)-1 == 3:
            plt.ylabel("p-ratio", fontdict=font)
        else:
            plt.yticks([], [])
        plt.ylim(-1.5, 1.5)
        plt.xticks(index + bar_width, ("SG", "BD", "RC"), fontsize=14)
        plt.yticks(fontsize=14)
        plt.title('Task ' + str(int(j)-1), fontdict=font)
        plt.scatter([1, ], [np.mean(ri_task_perceived_ratios["segments"][j]), ], 10, color='black')
        if stats.ttest_1samp(ri_task_perceived_ratios["segments"][j], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_task_perceived_ratios["segments"][j]), 2)) + '*', xy=(0.9, np.mean(ri_task_perceived_ratios["segments"][j])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=12)
        else:
            plt.annotate(str(round(np.mean(ri_task_perceived_ratios["segments"][j]), 2)), xy=(0.9, np.mean(ri_task_perceived_ratios["segments"][j])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=12)

        plt.scatter([2, ], [np.mean(ri_task_perceived_ratios["range"][j]), ], 10, color='black')
        if stats.ttest_1samp(ri_task_perceived_ratios["range"][j], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_task_perceived_ratios["range"][j]), 2)) + '*', xy=(1.9, np.mean(ri_task_perceived_ratios["range"][j])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=12)
        else:
            plt.annotate(str(round(np.mean(ri_task_perceived_ratios["range"][j]), 2)), xy=(1.9, np.mean(ri_task_perceived_ratios["range"][j])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=12)

        plt.scatter([3, ], [np.mean(ri_task_perceived_ratios["relative"][j]), ], 10, color='black')
        if stats.ttest_1samp(ri_task_perceived_ratios["relative"][j], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_task_perceived_ratios["relative"][j]), 2)) + '*', xy=(2.9, np.mean(ri_task_perceived_ratios["relative"][j])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=12)
        else:
            plt.annotate(str(round(np.mean(ri_task_perceived_ratios["relative"][j]), 2)), xy=(2.9, np.mean(ri_task_perceived_ratios["relative"][j])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=12)

    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/log_task_perception_ratio.eps")
    plt.show()

compute_task_perception_ratio()


# 用drift
# 计算perception drift
rr_perceived_drifts = defaultdict(lambda: defaultdict(lambda: []))
ri_perceived_drifts = defaultdict(lambda: defaultdict(lambda: []))
ii_perceived_drifts = defaultdict(lambda: defaultdict(lambda: []))


def compute_perception_drift():
    for time_method in ['segments', 'range', 'relative']:
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                # relevant & irrelevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) - (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ri_perceived_drifts[time_method][j].append(perceived_drift)
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] /
                                           estimated_time[time_method][studentid][j][doc2]) - (
                                          dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        rr_perceived_drifts[time_method][j].append(perceived_drift)
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] /
                                           estimated_time[time_method][studentid][j][doc2]) - (
                                          dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ii_perceived_drifts[time_method][j].append(perceived_drift)
            print time_method, j, np.mean(ri_perceived_drifts[time_method][j]), np.std(
                ri_perceived_drifts[time_method][j]), stats.ttest_1samp(ri_perceived_drifts[time_method][j], 0)[1]
            print time_method, j, np.mean(rr_perceived_drifts[time_method][j] + ii_perceived_drifts[time_method][j]), np.std(
                rr_perceived_drifts[time_method][j] + ii_perceived_drifts[time_method][j]), stats.ttest_1samp(rr_perceived_drifts[time_method][j] + ii_perceived_drifts[time_method][j], 0)[1]

        # plot
        plt.subplot(1, 3, 1)
        for k in [2, 3, 4, 5]:
            X = []
            for l in range(0, len(ri_perceived_drifts[time_method][str(k)])):
                X.append(k - 2)
            Y = ri_perceived_drifts[time_method][str(k)]
            plt.scatter(X, Y, alpha=.5)
        index = np.arange(4)
        bar_width = 0.5
        plt.xlabel('Task')
        plt.ylabel('perception drift')
        plt.ylim(-4.0, +4.0)
        plt.title('<R,I>')
        plt.xticks(index, ('2', '3', '4', '5'))

        plt.subplot(1, 3, 2)
        for k in [2, 3, 4, 5]:
            X = []
            for l in range(0, len(rr_perceived_drifts[time_method][str(k)])):
                X.append(k - 2)
            Y = rr_perceived_drifts[time_method][str(k)]
            plt.scatter(X, Y, alpha=.5)
        index = np.arange(4)
        bar_width = 0.5
        plt.xlabel('Task')
        plt.ylim(-4.0, +4.0)
        plt.title('<R,R>')
        plt.xticks(index, ('2', '3', '4', '5'))

        plt.subplot(1, 3, 3)
        for k in [2, 3, 4, 5]:
            X = []
            for l in range(0, len(ii_perceived_drifts[time_method][str(k)])):
                X.append(k - 2)
            Y = ii_perceived_drifts[time_method][str(k)]
            plt.scatter(X, Y, alpha=.5)
        index = np.arange(4)
        bar_width = 0.5
        plt.xlabel('Task')
        plt.ylim(-4.0, +4.0)
        plt.title('<I,I>')
        plt.xticks(index, ('2', '3', '4', '5'))

        plt.legend()
        plt.tight_layout()
        plt.savefig("../data/perception_drift_" + time_method + ".png")
        plt.show()

# compute_perception_drift()


# 每个user的perception_drift的分布
def compute_user_perception_drift():
    for time_method in ['segments', 'range', 'relative']:
        user_rr_perceived_drifts = defaultdict(lambda: [])
        means = []
        stds = []
        for studentid in validUsers:
            for j in ['2', '3', '4', '5']:
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] /
                                           estimated_time[time_method][studentid][j][doc2]) - (
                                          dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        user_rr_perceived_drifts[studentid].append(perceived_drift)
            means.append(np.mean(user_rr_perceived_drifts[studentid]))
            stds.append(np.std(user_rr_perceived_drifts[studentid]))
            print studentid, stats.ttest_1samp(user_rr_perceived_drifts[studentid], 0)[1]

        # plot
        n_groups = 24
        fig, ax = plt.subplots()
        index = np.arange(0.8, n_groups, 1)
        bar_width = 0.4
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        rects1 = plt.bar(index, means, bar_width, alpha=opacity, color='b', yerr=stds, error_kw=error_config)
        plt.xlabel('user')
        plt.ylabel('perception drift')
        plt.title('')
        plt.legend()
        plt.tight_layout()
        plt.savefig("../data/user_perception_drift_" + time_method + ".png")
        plt.show()

# compute_user_perception_drift()


# 用sequence
rr_perceived_sequences = defaultdict(lambda: [])
ri_perceived_sequences = defaultdict(lambda: [])
ii_perceived_sequences = defaultdict(lambda: [])


def compute_perception_sequence():
    fout = open('../data/log_perception_sequence_significance.csv', 'w')
    for time_method in ['segments', 'range', 'relative']:
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                # relevant & irrelevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        if dwell_time[studentid][j][doc1] < dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] > estimated_time[time_method][studentid][j][doc2]:
                            perceived_sequence = 1
                        elif dwell_time[studentid][j][doc1] > dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] < estimated_time[time_method][studentid][j][doc2]:
                            perceived_sequence = -1
                        else:
                            perceived_sequence = 0
                        ri_perceived_sequences[time_method].append(perceived_sequence)
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        if dwell_time[studentid][j][doc1] < dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] > estimated_time[time_method][studentid][j][doc2]:
                            perceived_sequence = 1
                        elif dwell_time[studentid][j][doc1] > dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] < estimated_time[time_method][studentid][j][doc2]:
                            perceived_sequence = -1
                        else:
                            perceived_sequence = 0
                        rr_perceived_sequences[time_method].append(perceived_sequence)
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        if dwell_time[studentid][j][doc1] < dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] > estimated_time[time_method][studentid][j][doc2]:
                            perceived_sequence = 1
                        elif dwell_time[studentid][j][doc1] > dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] < estimated_time[time_method][studentid][j][doc2]:
                            perceived_sequence = -1
                        else:
                            perceived_sequence = 0
                        ii_perceived_sequences[time_method].append(perceived_sequence)

        fout.write(time_method + ',ri,mean:' + str(round(np.mean(ri_perceived_sequences[time_method]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ri_perceived_sequences[time_method], 0)[1], 3)) + '\n')
        fout.write(time_method + ',rr,mean:' + str(round(np.mean(rr_perceived_sequences[time_method]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(rr_perceived_sequences[time_method], 0)[1], 3)) + '\n')
        fout.write(time_method + ',ii,mean:' + str(round(np.mean(ii_perceived_sequences[time_method]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ii_perceived_sequences[time_method], 0)[1], 3)) + '\n')

        print time_method, "ri", np.mean(ri_perceived_sequences[time_method]), np.std(
                ri_perceived_sequences[time_method]), stats.ttest_1samp(ri_perceived_sequences[time_method], 0)[1]
        print time_method, "rr", np.mean(rr_perceived_sequences[time_method]), np.std(
                rr_perceived_sequences[time_method]), stats.ttest_1samp(rr_perceived_sequences[time_method], 0)[1]
        print time_method, "ii", np.mean(ii_perceived_sequences[time_method]), np.std(
                ii_perceived_sequences[time_method]), stats.ttest_1samp(ii_perceived_sequences[time_method], 0)[1]
    fout.close()

    # plot
    index = np.arange(3)
    bar_width = 1
    font = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 16,
    }
    # plt.subplot(1, 3, 1)
    data = [ri_perceived_sequences["segments"], ri_perceived_sequences["range"], ri_perceived_sequences["relative"]]
    plt.figure(figsize=(6, 6))
    plt.boxplot(data)
    plt.ylabel("perceived sequence", fontdict=font)
    # plt.ylim(-1.5, 1.5)
    plt.xticks(index + bar_width, ("SG", "BD", "RC"), fontsize=16)
    plt.yticks(fontsize=16)
    # plt.title("<R, I>", fontdict=font)
    plt.scatter([1, ], [np.mean(ri_perceived_sequences["segments"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ri_perceived_sequences["segments"]), 2)) + '*', xy=(0.9, np.mean(ri_perceived_sequences["segments"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=18)
    plt.scatter([2, ], [np.mean(ri_perceived_sequences["range"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ri_perceived_sequences["range"]), 2)) + '*', xy=(1.9, np.mean(ri_perceived_sequences["range"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=18)
    plt.scatter([3, ], [np.mean(ri_perceived_sequences["relative"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ri_perceived_sequences["relative"]), 2)), xy=(2.9, np.mean(ri_perceived_sequences["relative"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=18)

    '''plt.subplot(1, 3, 2)
    data = [rr_perceived_ratios["segments"], rr_perceived_ratios["range"], rr_perceived_ratios["relative"]]
    plt.boxplot(data)
    plt.ticklabel_format(fontdict=font)
    plt.ylim(-1.5, 1.5)
    plt.xticks(index + bar_width, ("SG", "RG", "RC"), fontsize=16)
    plt.yticks([], [])
    plt.title("<R, R>", fontdict=font)
    plt.scatter([1, ], [np.mean(rr_perceived_ratios["segments"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(rr_perceived_ratios["segments"]), 2)), xy=(0.8, np.mean(rr_perceived_ratios["segments"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([2, ], [np.mean(rr_perceived_ratios["range"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(rr_perceived_ratios["range"]), 2)), xy=(1.8, np.mean(rr_perceived_ratios["range"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([3, ], [np.mean(rr_perceived_ratios["relative"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(rr_perceived_ratios["relative"]), 2)), xy=(2.8, np.mean(rr_perceived_ratios["relative"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)

    plt.subplot(1, 3, 3)
    data = [ii_perceived_ratios["segments"], ii_perceived_ratios["range"], ii_perceived_ratios["relative"]]
    plt.boxplot(data)
    plt.ticklabel_format(fontdict=font)
    plt.ylim(-1.5, 1.5)
    plt.xticks(index + bar_width, ("SG", "RG", "RC"), fontsize=16)
    plt.yticks([], [])
    plt.title("<I, I>", fontdict=font)
    plt.scatter([1, ], [np.mean(ii_perceived_ratios["segments"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ii_perceived_ratios["segments"]), 2)), xy=(0.8, np.mean(ii_perceived_ratios["segments"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([2, ], [np.mean(ii_perceived_ratios["range"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ii_perceived_ratios["range"]), 2)), xy=(1.8, np.mean(ii_perceived_ratios["range"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)
    plt.scatter([3, ], [np.mean(ii_perceived_ratios["relative"]), ], 10, color='black')
    plt.annotate(str(round(np.mean(ii_perceived_ratios["relative"]), 2)), xy=(2.8, np.mean(ii_perceived_ratios["relative"]) + 0.05), xytext=(+10, -3), textcoords='offset points', fontsize=12)'''

    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/log_perception_sequence.eps")
    plt.show()

# compute_perception_sequence()


# 每个user的perception_sequence的分布
rr_user_perceived_sequences = defaultdict(lambda: defaultdict(lambda: []))
ri_user_perceived_sequences = defaultdict(lambda: defaultdict(lambda: []))
ii_user_perceived_sequences = defaultdict(lambda: defaultdict(lambda: []))


def compute_user_perception_sequence():
    fout = open('../data/log_user_perception_sequence_significance.csv', 'w')
    for time_method in ['segments', 'range', 'relative']:
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                # relevant & irrelevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ri_user_perceived_ratios[time_method][studentid].append(math.log(perceived_ratio))
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        rr_user_perceived_ratios[time_method][studentid].append(math.log(perceived_ratio))
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1 + 1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_ratio = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ii_user_perceived_ratios[time_method][studentid].append(math.log(perceived_ratio))
        for studentid in validUsers:
            print time_method, studentid, "ri", np.mean(ri_user_perceived_ratios[time_method][studentid]), np.std(
                ri_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(ri_user_perceived_ratios[time_method][studentid], 0)[1]
            fout.write(time_method + ',' + studentid + ',ri,mean:' + str(round(np.mean(ri_user_perceived_ratios[time_method][studentid]), 3)) + ',p-value:' + str(round(stats.ttest_1samp(ri_user_perceived_ratios[time_method][studentid], 0)[1], 3)) + '\n')
            '''print time_method, studentid, "rr", np.mean(rr_user_perceived_ratios[time_method][studentid]), np.std(
                rr_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(rr_user_perceived_ratios[time_method][studentid], 1)[1]
            print time_method, studentid, "ii", np.mean(ii_user_perceived_ratios[time_method][studentid]), np.std(
                ii_user_perceived_ratios[time_method][studentid]), stats.ttest_1samp(ii_user_perceived_ratios[time_method][studentid], 1)[1]'''
    fout.close()

    # plot
    index = np.arange(3)
    bar_width = 1
    font = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 12,
    }
    plt.figure(figsize=(12, 9))
    for i in range(1, 25):
        plt.subplot(4, 6, i)
        studentid = validUsers.keys()[i-1]
        data = [ri_user_perceived_ratios["segments"][studentid], ri_user_perceived_ratios["range"][studentid], ri_user_perceived_ratios["relative"][studentid]]
        plt.boxplot(data)
        if i % 6 == 1:
            plt.ylabel("perceived ratio", fontdict=font)
        else:
            plt.yticks([], [])
        plt.ylim(-1.5, 1.5)
        plt.xticks(index + bar_width, ("SG", "BD", "RC"), fontsize=12)
        plt.yticks(fontsize=12)
        plt.title(str(i), fontdict=font)
        plt.scatter([1, ], [np.mean(ri_user_perceived_ratios["segments"][studentid]), ], 10, color='black')
        if stats.ttest_1samp(ri_user_perceived_ratios["segments"][studentid], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["segments"][studentid]), 2)) + '*', xy=(0.8, np.mean(ri_user_perceived_ratios["segments"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
            print i, ",segments,mean:", round(np.mean(ri_user_perceived_ratios["segments"][studentid]), 2)
            for j in ['2', '3', '4', '5']:
                print j, "dtime:", dwell_time[studentid][j], "sg-etime:", estimated_time['segments'][studentid][j]
        else:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["segments"][studentid]), 2)), xy=(0.8, np.mean(ri_user_perceived_ratios["segments"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)

        plt.scatter([2, ], [np.mean(ri_user_perceived_ratios["range"][studentid]), ], 10, color='black')
        if stats.ttest_1samp(ri_user_perceived_ratios["range"][studentid], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["range"][studentid]), 2)) + '*', xy=(1.8, np.mean(ri_user_perceived_ratios["range"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
            print i, ",range,mean:", round(np.mean(ri_user_perceived_ratios["range"][studentid]), 2)
            for j in ['2', '3', '4', '5']:
                print j, "dtime:", dwell_time[studentid][j], "rg-etime:", estimated_time['range'][studentid][j]
        else:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["range"][studentid]), 2)), xy=(1.8, np.mean(ri_user_perceived_ratios["range"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)

        plt.scatter([3, ], [np.mean(ri_user_perceived_ratios["relative"][studentid]), ], 10, color='black')
        if stats.ttest_1samp(ri_user_perceived_ratios["relative"][studentid], 0)[1] < 0.05:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["relative"][studentid]), 2)) + '*', xy=(2.8, np.mean(ri_user_perceived_ratios["relative"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)
            print i, ",relative,mean:", round(np.mean(ri_user_perceived_ratios["relative"][studentid]), 2)
            for j in ['2', '3', '4', '5']:
                print j, "dtime:", dwell_time[studentid][j], "rc-etime:", estimated_time['relative'][studentid][j]
        else:
            plt.annotate(str(round(np.mean(ri_user_perceived_ratios["relative"][studentid]), 2)), xy=(2.8, np.mean(ri_user_perceived_ratios["relative"][studentid])+0.1), xytext=(+10, -3), textcoords='offset points', fontsize=10)

        # plt.annotate(str(i), xy=(0.2, 0.8), xytext=(+10, -3), textcoords='offset points', fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/log_user_perception_ratio.eps")
    plt.show()

# compute_user_perception_sequence()


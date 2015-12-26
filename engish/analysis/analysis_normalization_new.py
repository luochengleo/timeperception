# -*- coding: utf-8 -*-
__author__ = 'franky'
import re
from collections import defaultdict
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

validUsers = {'2015012620': 1, '2015012618': 2, '2015012674': 3, '2014011319': 4, '2015012625': 5, '2015012676': 6, '2015012609': 7, '2015012811': 8, '2015012653': 9, '2015012679': 10, '2015012617': 11, '2015012828': 12, '2015212354': 13, '2015012624': 14, '2014012759': 15, '2012012767': 16, '2015012623': 17, '2014012772': 18, '2015012610': 19, '2011012756': 20, '2014012780': 21, '2015012622': 22, '2015012649': 23, '2015011043': 24}

estimation = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1))))
relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
reading_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0.0, 0.0])))


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
for line in open('../data/log20151220.csv').readlines()[1:]:
    id = line.strip().split(',')[0]
    studentid = line.strip().split(',')[1]
    jobid = line.strip().split(',')[2]
    action = line.strip().split(',')[3]
    content = line.strip().split(',')[4]
    if studentid in validUsers:
        if action == 'BEGIN_READING':
            doc_rank = int(cdp.search(content+'\t').group(1))
            time = int(tp.search(content+'\t').group(1))
            reading_time[studentid][jobid][doc_rank][0] = time
            # 时刻记得维护一个最新时间戳,避免日志丢失造成大的时间错误
            if doc_rank < 4:
                reading_time[studentid][jobid][doc_rank+1][0] = time

        if action == 'END_READING':
            doc_rank = int(cdp.search(content+'\t').group(1))
            time = int(tp.search(content+'\t').group(1))
            reading_time[studentid][jobid][doc_rank][1] = time
            if doc_rank < 4:
                reading_time[studentid][jobid][doc_rank+1][0] = time

        if action == 'RELEVANCE_ANNOTATION':
            doc_rank = int(cdp.search(content+'\t').group(1).split(' ')[0])
            time = int(tp.search(content+'\t').group(1))
            rel = int(relp.search(content+'\t').group(1).split(' ')[0])
            relevance[studentid][jobid][doc_rank] = rel
            if doc_rank < 4:
                reading_time[studentid][jobid][doc_rank+1][0] = time

        if action == 'TIME_1':
            seg = segp.search(content+'\t').group(1).split(' ')[0]
            point1, point2, point3, _ = seg.split('_')
            point1 = int(point1)
            point2 = int(point2)
            point3 = int(point3)
            estimation['segments'][studentid][jobid][1] = point1
            estimation['segments'][studentid][jobid][2] = point2 - point1
            estimation['segments'][studentid][jobid][3] = point3 - point2
            estimation['segments'][studentid][jobid][4] = 1000 - point3

        if action == 'TIME2':
            ran = rangep.search(content+'\t').group(1).split(' ')[0]
            _, min1, max1, min2, max2, min3, max3, min4, max4, _ = ran.split('_')
            mean1 = (int(min1)*10 + int(max1)*10) / 2
            mean2 = (int(min2)*10 + int(max2)*10) / 2
            mean3 = (int(min3)*10 + int(max3)*10) / 2
            mean4 = (int(min4)*10 + int(max4)*10) / 2
            estimation['range'][studentid][jobid][1] = mean1
            estimation['range'][studentid][jobid][2] = mean2
            estimation['range'][studentid][jobid][3] = mean3
            estimation['range'][studentid][jobid][4] = mean4

        if action == 'TIME3':
            rela = relap.search(content+'\t').group(1).split(' ')[0]
            doc1, doc2, doc3, doc4, _ = rela.split('_')
            estimation['relative'][studentid][jobid][1] = int(doc1)
            estimation['relative'][studentid][jobid][2] = int(doc2)
            estimation['relative'][studentid][jobid][3] = int(doc3)
            estimation['relative'][studentid][jobid][4] = int(doc4)

# task2-task5, dwell_time, estimated_time, perceived_relevance
dwell_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1))))
perceived_relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))

for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            dwell_time[studentid][j][d] = (reading_time[studentid][j][d][1] - reading_time[studentid][j][d][0]) / 1000.0
            perceived_relevance[studentid][j][d] = relevance[studentid][j][d]
            for time_method in ['segments', 'range', 'relative']:
                estimated_time[time_method][studentid][j][d] = float(estimation[time_method][studentid][j][d])


# relevance_filling
for studentid in validUsers:
    for j in ['2', '3', '4', '5']:
        docseq_ = job_setting[validUsers[studentid]][j]
        for d in [1, 2, 3, 4]:
            docid = int(docseq_.split('-')[d-1])
            if perceived_relevance[studentid][j][d] == -1:
                if docid > 3:
                    perceived_relevance[studentid][j][d] = 0
                else:
                    perceived_relevance[studentid][j][d] = 3

# relevance agreement
relevance_agreement = defaultdict(lambda: defaultdict(lambda: 0.0))
relevance_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
def compute_relevance_agreement():
    for j in ['2', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            for studentid in validUsers:
                docseq_ = job_setting[validUsers[studentid]][j]
                docid = int(docseq_.split('-')[d-1])
                if (docid < 4 and perceived_relevance[studentid][j][d] > 1) or (docid > 3 and perceived_relevance[studentid][j][d] < 2):
                    relevance_agree_num[j][docid] += 1
        for docid in [1, 2, 4, 5]:
            relevance_agreement[j][docid] = relevance_agree_num[j][docid] / 24.0
            print j, docid, relevance_agreement[j][docid]

compute_relevance_agreement()

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

# relevant & relevant
rr_de_agree_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
rr_de_total_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
rr_e1e2_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e3_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e2e3_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e2_total_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e1e3_total_num = defaultdict(lambda: defaultdict(lambda: 0))
rr_e2e3_total_num = defaultdict(lambda: defaultdict(lambda: 0))
# relevant & irrelevant
ri_de_agree_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ri_de_total_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ri_e1e2_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e3_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e2e3_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e2_total_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e1e3_total_num = defaultdict(lambda: defaultdict(lambda: 0))
ri_e2e3_total_num = defaultdict(lambda: defaultdict(lambda: 0))
# irrelevant & irrelevant
ii_de_agree_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ii_de_total_num = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
ii_e1e2_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e3_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e2e3_agree_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e2_total_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e1e3_total_num = defaultdict(lambda: defaultdict(lambda: 0))
ii_e2e3_total_num = defaultdict(lambda: defaultdict(lambda: 0))


def analyze_pairwise_agreement():
    for studentid in validUsers:
        for j in ['2', '3', '4', '5']:
            # relevant & relevant
            for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                for d2 in range(d1+1, len(relevant_doc_ranks[studentid][j])):
                    doc1 = relevant_doc_ranks[studentid][j][d1]
                    doc2 = relevant_doc_ranks[studentid][j][d2]
                    # dtime & etime(3 methods)
                    for time_method in ['segments', 'range', 'relative']:
                        rr_de_total_num[time_method][studentid][j] += 1
                        if (dwell_time[studentid][j][doc1] <= dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] <= estimated_time[time_method][studentid][j][doc2]) or (dwell_time[studentid][j][doc1] >= dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] >= estimated_time[time_method][studentid][j][doc2]):
                            rr_de_agree_num[time_method][studentid][j] += 1
                    # segments & range
                    rr_e1e2_total_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2]) or (estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][doc2] and estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][doc2]):
                        rr_e1e2_agree_num[studentid][j] += 1
                    # segments & relative
                    rr_e1e3_total_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] <= estimated_time['relative'][studentid][j][doc2]) or (estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] >= estimated_time['relative'][studentid][j][doc2]):
                        rr_e1e3_agree_num[studentid][j] += 1
                    # range & relative
                    rr_e2e3_total_num[studentid][j] += 1
                    if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] <= estimated_time['relative'][studentid][j][doc2]) or (estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] >= estimated_time['relative'][studentid][j][doc2]):
                        rr_e2e3_agree_num[studentid][j] += 1

            # relevant & irrelevant
            for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    doc1 = relevant_doc_ranks[studentid][j][d1]
                    doc2 = irrelevant_doc_ranks[studentid][j][d2]
                    # dtime & etime(3 methods)
                    for time_method in ['segments', 'range', 'relative']:
                        ri_de_total_num[time_method][studentid][j] += 1
                        if (dwell_time[studentid][j][doc1] <= dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] <= estimated_time[time_method][studentid][j][doc2]) or (dwell_time[studentid][j][doc1] >= dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] >= estimated_time[time_method][studentid][j][doc2]):
                            ri_de_agree_num[time_method][studentid][j] += 1
                    # segments & range
                    ri_e1e2_total_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2]) or (estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][doc2] and estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][doc2]):
                        ri_e1e2_agree_num[studentid][j] += 1
                    # segments & relative
                    ri_e1e3_total_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] <= estimated_time['relative'][studentid][j][doc2]) or (estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] >= estimated_time['relative'][studentid][j][doc2]):
                        ri_e1e3_agree_num[studentid][j] += 1
                    # range & relative
                    ri_e2e3_total_num[studentid][j] += 1
                    if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] <= estimated_time['relative'][studentid][j][doc2]) or (estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] >= estimated_time['relative'][studentid][j][doc2]):
                        ri_e2e3_agree_num[studentid][j] += 1

            # irrelevant & irrelevant
            for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                for d2 in range(d1+1, len(irrelevant_doc_ranks[studentid][j])):
                    doc1 = irrelevant_doc_ranks[studentid][j][d1]
                    doc2 = irrelevant_doc_ranks[studentid][j][d2]
                    # dtime & etime(3 methods)
                    for time_method in ['segments', 'range', 'relative']:
                        ii_de_total_num[time_method][studentid][j] += 1
                        if (dwell_time[studentid][j][doc1] <= dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] <= estimated_time[time_method][studentid][j][doc2]) or (dwell_time[studentid][j][doc1] >= dwell_time[studentid][j][doc2] and estimated_time[time_method][studentid][j][doc1] >= estimated_time[time_method][studentid][j][doc2]):
                            ii_de_agree_num[time_method][studentid][j] += 1
                    # segments & range
                    ii_e1e2_total_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][doc2] and estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2]) or (estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][doc2] and estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][doc2]):
                        ii_e1e2_agree_num[studentid][j] += 1
                    # segments & relative
                    ii_e1e3_total_num[studentid][j] += 1
                    if (estimated_time['segments'][studentid][j][doc1] <= estimated_time['segments'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] <= estimated_time['relative'][studentid][j][doc2]) or (estimated_time['segments'][studentid][j][doc1] >= estimated_time['segments'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] >= estimated_time['relative'][studentid][j][doc2]):
                        ii_e1e3_agree_num[studentid][j] += 1
                    # range & relative
                    ii_e2e3_total_num[studentid][j] += 1
                    if (estimated_time['range'][studentid][j][doc1] <= estimated_time['range'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] <= estimated_time['relative'][studentid][j][doc2]) or (estimated_time['range'][studentid][j][doc1] >= estimated_time['range'][studentid][j][doc2] and estimated_time['relative'][studentid][j][doc1] >= estimated_time['relative'][studentid][j][doc2]):
                        ii_e2e3_agree_num[studentid][j] += 1

# analyze_pairwise_agreement()


def compute_pairwise_agreement():
    fout = open('../data/pairwise_agreement.csv', 'w')
    fout.write("studentid,m1-m2-R-R,m1-m2-R-I,m1-m2-I-I,m1-m2-total,m1-m3-R-R,m1-m3-R-I,m1-m3-I-I,m1-m3-total,m2-m3-R-R,m2-m3-R-I,m2-m3-I-I,m2-m3-total,m1-R-R,m1-R-I,m1-I-I,m2-R-R,m2-R-I,m2-I-I,m3-R-R,m3-R-I,m3-I-I")
    fout.write('\n')
    for studentid in validUsers:
        fout.write(studentid + ',')
        rr_e1e2_agree_num_all_tasks = 0
        rr_e1e2_total_num_all_tasks = 0
        ri_e1e2_agree_num_all_tasks = 0
        ri_e1e2_total_num_all_tasks = 0
        ii_e1e2_agree_num_all_tasks = 0
        ii_e1e2_total_num_all_tasks = 0

        rr_e1e3_agree_num_all_tasks = 0
        rr_e1e3_total_num_all_tasks = 0
        ri_e1e3_agree_num_all_tasks = 0
        ri_e1e3_total_num_all_tasks = 0
        ii_e1e3_agree_num_all_tasks = 0
        ii_e1e3_total_num_all_tasks = 0

        rr_e2e3_agree_num_all_tasks = 0
        rr_e2e3_total_num_all_tasks = 0
        ri_e2e3_agree_num_all_tasks = 0
        ri_e2e3_total_num_all_tasks = 0
        ii_e2e3_agree_num_all_tasks = 0
        ii_e2e3_total_num_all_tasks = 0

        rr_de_agree_num_all_tasks = defaultdict(lambda: 0)
        rr_de_total_num_all_tasks = defaultdict(lambda: 0)
        ri_de_agree_num_all_tasks = defaultdict(lambda: 0)
        ri_de_total_num_all_tasks = defaultdict(lambda: 0)
        ii_de_agree_num_all_tasks = defaultdict(lambda: 0)
        ii_de_total_num_all_tasks = defaultdict(lambda: 0)

        for j in ['2', '3', '4', '5']:
            rr_e1e2_agree_num_all_tasks += rr_e1e2_agree_num[studentid][j]
            rr_e1e2_total_num_all_tasks += rr_e1e2_total_num[studentid][j]
            ri_e1e2_agree_num_all_tasks += ri_e1e2_agree_num[studentid][j]
            ri_e1e2_total_num_all_tasks += ri_e1e2_total_num[studentid][j]
            ii_e1e2_agree_num_all_tasks += ii_e1e2_agree_num[studentid][j]
            ii_e1e2_total_num_all_tasks += ii_e1e2_total_num[studentid][j]

            rr_e1e3_agree_num_all_tasks += rr_e1e3_agree_num[studentid][j]
            rr_e1e3_total_num_all_tasks += rr_e1e3_total_num[studentid][j]
            ri_e1e3_agree_num_all_tasks += ri_e1e3_agree_num[studentid][j]
            ri_e1e3_total_num_all_tasks += ri_e1e3_total_num[studentid][j]
            ii_e1e3_agree_num_all_tasks += ii_e1e3_agree_num[studentid][j]
            ii_e1e3_total_num_all_tasks += ii_e1e3_total_num[studentid][j]

            rr_e2e3_agree_num_all_tasks += rr_e2e3_agree_num[studentid][j]
            rr_e2e3_total_num_all_tasks += rr_e2e3_total_num[studentid][j]
            ri_e2e3_agree_num_all_tasks += ri_e2e3_agree_num[studentid][j]
            ri_e2e3_total_num_all_tasks += ri_e2e3_total_num[studentid][j]
            ii_e2e3_agree_num_all_tasks += ii_e2e3_agree_num[studentid][j]
            ii_e2e3_total_num_all_tasks += ii_e2e3_total_num[studentid][j]

            for time_method in ['segments', 'range', 'relative']:
                rr_de_agree_num_all_tasks[time_method] += rr_de_agree_num[time_method][studentid][j]
                rr_de_total_num_all_tasks[time_method] += rr_de_total_num[time_method][studentid][j]
                ri_de_agree_num_all_tasks[time_method] += ri_de_agree_num[time_method][studentid][j]
                ri_de_total_num_all_tasks[time_method] += ri_de_total_num[time_method][studentid][j]
                ii_de_agree_num_all_tasks[time_method] += ii_de_agree_num[time_method][studentid][j]
                ii_de_total_num_all_tasks[time_method] += ii_de_total_num[time_method][studentid][j]

        items = [
            float(rr_e1e2_agree_num_all_tasks) / float(rr_e1e2_total_num_all_tasks),
            float(ri_e1e2_agree_num_all_tasks) / float(ri_e1e2_total_num_all_tasks),
            float(ii_e1e2_agree_num_all_tasks) / float(ii_e1e2_total_num_all_tasks),
            float(rr_e1e2_agree_num_all_tasks + ri_e1e2_agree_num_all_tasks + ii_e1e2_agree_num_all_tasks) / float(rr_e1e2_total_num_all_tasks + ri_e1e2_total_num_all_tasks + ii_e1e2_total_num_all_tasks),
            float(rr_e1e3_agree_num_all_tasks) / float(rr_e1e3_total_num_all_tasks),
            float(ri_e1e3_agree_num_all_tasks) / float(ri_e1e3_total_num_all_tasks),
            float(ii_e1e3_agree_num_all_tasks) / float(ii_e1e3_total_num_all_tasks),
            float(rr_e1e3_agree_num_all_tasks + ri_e1e3_agree_num_all_tasks + ii_e1e3_agree_num_all_tasks) / float(rr_e1e3_total_num_all_tasks + ri_e1e3_total_num_all_tasks + ii_e1e3_total_num_all_tasks),
            float(rr_e2e3_agree_num_all_tasks) / float(rr_e2e3_total_num_all_tasks),
            float(ri_e2e3_agree_num_all_tasks) / float(ri_e2e3_total_num_all_tasks),
            float(ii_e2e3_agree_num_all_tasks) / float(ii_e2e3_total_num_all_tasks),
            float(rr_e2e3_agree_num_all_tasks + ri_e2e3_agree_num_all_tasks + ii_e2e3_agree_num_all_tasks) / float(rr_e2e3_total_num_all_tasks + ri_e2e3_total_num_all_tasks + ii_e2e3_total_num_all_tasks),
            float(rr_de_agree_num_all_tasks['segments']) / float(rr_de_total_num_all_tasks['segments']),
            float(ri_de_agree_num_all_tasks['segments']) / float(ri_de_total_num_all_tasks['segments']),
            float(ii_de_agree_num_all_tasks['segments']) / float(ii_de_total_num_all_tasks['segments']),
            float(rr_de_agree_num_all_tasks['range']) / float(rr_de_total_num_all_tasks['range']),
            float(ri_de_agree_num_all_tasks['range']) / float(ri_de_total_num_all_tasks['range']),
            float(ii_de_agree_num_all_tasks['range']) / float(ii_de_total_num_all_tasks['range']),
            float(rr_de_agree_num_all_tasks['relative']) / float(rr_de_total_num_all_tasks['relative']),
            float(ri_de_agree_num_all_tasks['relative']) / float(ri_de_total_num_all_tasks['relative']),
            float(ii_de_agree_num_all_tasks['relative']) / float(ii_de_total_num_all_tasks['relative']),
        ]
        fout.write(','.join(str(item) for item in items))
        fout.write('\n')

    fout.close()

# compute_pairwise_agreement()


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
        print j, np.mean(r_dtimes[j]), np.std(r_dtimes[j]), np.mean(ir_dtimes[j]), np.std(ir_dtimes[j]), stats.ttest_ind(r_dtimes[j], ir_dtimes[j], equal_var=False)[1]
    # plot
    n_groups = 4
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = plt.bar(index, means_r_dtimes, bar_width, alpha=opacity, color='b', yerr=std_r_dtimes, error_kw=error_config, label='R')
    rects2 = plt.bar(index + bar_width, means_ir_dtimes, bar_width, alpha=opacity, color='r', yerr=std_ir_dtimes, error_kw=error_config, label='I')
    plt.xlabel('Task')
    plt.ylabel('Dtime')
    plt.title('')
    plt.xticks(index + bar_width, ('2', '3', '4', '5'))
    plt.legend()
    plt.tight_layout()
    plt.savefig("../data/dwell_time_comparison.png")
    plt.show()

# compute_dtime()


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
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ri_perceived_drifts[time_method][j].append(perceived_drift)
                # relevant & relevant
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1+1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        rr_perceived_drifts[time_method][j].append(perceived_drift)
                # irrelevant & irrelevant
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1+1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        ii_perceived_drifts[time_method][j].append(perceived_drift)
            print time_method, j, np.mean(ri_perceived_drifts[time_method][j]), np.std(ri_perceived_drifts[time_method][j]), stats.ttest_1samp(ri_perceived_drifts[time_method][j], 1)[1]
            print time_method, j, np.mean(rr_perceived_drifts[time_method][j]), np.std(rr_perceived_drifts[time_method][j]), stats.ttest_1samp(rr_perceived_drifts[time_method][j], 1)[1]
            print time_method, j, np.mean(ii_perceived_drifts[time_method][j]), np.std(ii_perceived_drifts[time_method][j]), stats.ttest_1samp(ii_perceived_drifts[time_method][j], 1)[1]

        # plot
        plt.subplot(1, 3, 1)
        for k in [2, 3, 4, 5]:
            X = []
            for l in range(0, len(ri_perceived_drifts[time_method][str(k)])):
                X.append(k-2)
            Y = ri_perceived_drifts[time_method][str(k)]
            plt.scatter(X, Y, alpha=.5)
        index = np.arange(4)
        bar_width = 0.5
        plt.xlabel('Task')
        plt.ylabel('perception drift')
        plt.ylim(-1.0, 4.0)
        plt.title('<R,I>')
        plt.xticks(index, ('2', '3', '4', '5'))

        plt.subplot(1, 3, 2)
        for k in [2, 3, 4, 5]:
            X = []
            for l in range(0, len(rr_perceived_drifts[time_method][str(k)])):
                X.append(k-2)
            Y = rr_perceived_drifts[time_method][str(k)]
            plt.scatter(X, Y, alpha=.5)
        index = np.arange(4)
        bar_width = 0.5
        plt.xlabel('Task')
        plt.ylim(-1.0, 4.0)
        plt.title('<R,R>')
        plt.xticks(index, ('2', '3', '4', '5'))

        plt.subplot(1, 3, 3)
        for k in [2, 3, 4, 5]:
            X = []
            for l in range(0, len(ii_perceived_drifts[time_method][str(k)])):
                X.append(k-2)
            Y = ii_perceived_drifts[time_method][str(k)]
            plt.scatter(X, Y, alpha=.5)
        index = np.arange(4)
        bar_width = 0.5
        plt.xlabel('Task')
        plt.ylim(-1.0, 4.0)
        plt.title('<I,I>')
        plt.xticks(index, ('2', '3', '4', '5'))

        plt.legend()
        plt.tight_layout()
        plt.savefig("../data/perception_drift_" + time_method + ".png")
        plt.show()

        # plot drift-dtime
        # relevant & irrelevant
        dwell_time_differences = []
        perceived_drifts = []
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        dwell_time_difference = dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])

                        dwell_time_differences.append(abs(dwell_time_difference))
                        perceived_drifts.append(perceived_drift)

        plt.scatter(dwell_time_differences, perceived_drifts, alpha=.5)
        plt.xlabel('dwell time difference')
        plt.ylabel('perception drift')
        plt.xlim(0, 100)
        plt.ylim(0.0, 2.0)
        plt.title('<R,I>')

        plt.legend()
        plt.tight_layout()
        plt.savefig("../data/RI_perception_drift_" + time_method + "_with_dwell_time_difference.png")
        plt.show()

        # relevant & relevant
        dwell_time_differences = []
        perceived_drifts = []
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                for d1 in range(0, len(relevant_doc_ranks[studentid][j])):
                    for d2 in range(d1+1, len(relevant_doc_ranks[studentid][j])):
                        doc1 = relevant_doc_ranks[studentid][j][d1]
                        doc2 = relevant_doc_ranks[studentid][j][d2]
                        dwell_time_difference = dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])

                        dwell_time_differences.append(abs(dwell_time_difference))
                        perceived_drifts.append(perceived_drift)

        plt.scatter(dwell_time_differences, perceived_drifts, alpha=.5)
        plt.xlabel('dwell time difference')
        plt.ylabel('perception drift')
        plt.xlim(0, 100)
        plt.ylim(0.0, 2.0)
        plt.title('<R,R>')

        plt.legend()
        plt.tight_layout()
        plt.savefig("../data/RR_perception_drift_" + time_method + "_with_dwell_time_difference.png")
        plt.show()

        # irrelevant & irrelevant
        dwell_time_differences = []
        perceived_drifts = []
        for j in ['2', '3', '4', '5']:
            for studentid in validUsers:
                for d1 in range(0, len(irrelevant_doc_ranks[studentid][j])):
                    for d2 in range(d1+1, len(irrelevant_doc_ranks[studentid][j])):
                        doc1 = irrelevant_doc_ranks[studentid][j][d1]
                        doc2 = irrelevant_doc_ranks[studentid][j][d2]
                        dwell_time_difference = dwell_time[studentid][j][doc1] - dwell_time[studentid][j][doc2]
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])

                        dwell_time_differences.append(abs(dwell_time_difference))
                        perceived_drifts.append(perceived_drift)

        plt.scatter(dwell_time_differences, perceived_drifts, alpha=.5)
        plt.xlabel('dwell time difference')
        plt.ylabel('perception drift')
        plt.xlim(0, 100)
        plt.ylim(0.0, 2.0)
        plt.title('<I,I>')

        plt.legend()
        plt.tight_layout()
        plt.savefig("../data/II_perception_drift_" + time_method + "_with_dwell_time_difference.png")
        plt.show()

compute_perception_drift()


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
                        perceived_drift = (estimated_time[time_method][studentid][j][doc1] / estimated_time[time_method][studentid][j][doc2]) / (dwell_time[studentid][j][doc1] / dwell_time[studentid][j][doc2])
                        user_rr_perceived_drifts[studentid].append(perceived_drift)
            means.append(np.mean(user_rr_perceived_drifts[studentid]))
            stds.append(np.std(user_rr_perceived_drifts[studentid]))
            print studentid, stats.ttest_1samp(user_rr_perceived_drifts[studentid], 1)[1]

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

compute_user_perception_drift()

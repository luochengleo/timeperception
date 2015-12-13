__author__ = 'franky'
import re
from collections import defaultdict
import numpy as np
validUsers = ('2015012616', '2015012805')
first_group_users = ('2015012616', )
second_group_users = ('2015012805', )

# calibration -userid ,jobid

# calibration -userid ,jobid,docid
segments_estimation = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:-1)))
range_estimation = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:-1)))
relative_estimation = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:-1)))
relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
reading = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:[0.0,0.0])))

etp = re.compile(r'ET=(.*?)\t')
cdp = re.compile(r'CURRENT_DOC=(.*?)\t')
tp = re.compile(r'TIMESTAMP=(.*?)\t')
relp = re.compile(r'REL=(.*?)\t')
ansp = re.compile(r'ANS=(.*?)\t')
segp = re.compile(r'Segments=(.*?)\t')
rangep = re.compile(r'Range=(.*?)\t')
relap = re.compile(r'Relative=(.*?)\t')

job_setting_relevance = defaultdict(lambda: defaultdict(lambda: []))
for line in open('../data/job_settings.csv').readlines()[1:]:
    id, jobid, settingid, taskid, docseq = line.strip().split(',')
    for doc in docseq.split('-'):
        if int(doc) < 4:
            job_setting_relevance[int(settingid)][taskid].append(1)
        else:
            job_setting_relevance[int(settingid)][taskid].append(0)
print job_setting_relevance

for line in open('../data/pilot.csv').readlines()[1:]:
    id = line.strip().split(',')[0]
    studentid = line.strip().split(',')[1]
    jobid = line.strip().split(',')[2]
    action = line.strip().split(',')[3]
    content = line.strip().split(',')[4]
    if studentid in validUsers:
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

        if action == 'RELEVANCE_ANNOTATION':
            docid = int(cdp.search(content+'\t').group(1).split(' ')[0])
            rel = int(relp.search(content+'\t').group(1).split(' ')[0])
            relevance[studentid][jobid][docid] = rel

        if action == 'TIME_ESTIMATION':
            seg = segp.search(content+'\t').group(1).split(' ')[0]
            point1, point2, point3, _ = seg.split('_')
            point1 = int(point1)
            point2 = int(point2)
            point3 = int(point3)
            segments_estimation[studentid][jobid][1] = point1
            segments_estimation[studentid][jobid][2] = point2 - point1
            segments_estimation[studentid][jobid][3] = point3 - point2
            segments_estimation[studentid][jobid][4] = 1000 - point3

        if action == 'RELATIVE_ESTIMATION':
            ran = rangep.search(content+'\t').group(1).split(' ')[0]
            _, min1, max1, min2, max2, min3, max3, min4, max4, mintotal, maxtotal = ran.split('_')
            mean1 = (int(min1)*10 + int(max1)*10) / 2
            mean2 = (int(min2)*10 + int(max2)*10) / 2
            mean3 = (int(min3)*10 + int(max3)*10) / 2
            mean4 = (int(min4)*10 + int(max4)*10) / 2
            range_estimation[studentid][jobid][1] = mean1
            range_estimation[studentid][jobid][2] = mean2
            range_estimation[studentid][jobid][3] = mean3
            range_estimation[studentid][jobid][4] = mean4
            rela = relap.search(content+'\t').group(1).split(' ')[0]
            doc1, doc2, doc3, doc4, _ = rela.split('_')
            relative_estimation[studentid][jobid][1] = int(doc1)
            relative_estimation[studentid][jobid][2] = int(doc2)
            relative_estimation[studentid][jobid][3] = int(doc3)
            relative_estimation[studentid][jobid][4] = int(doc4)

dwell_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
segments_estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
segments_ratio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
range_estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
range_ratio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
relative_estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
relative_ratio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
perceived_relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))

segments_relevant_ratios = defaultdict(lambda: defaultdict(lambda: []))
range_relevant_ratios = defaultdict(lambda: defaultdict(lambda: []))
relative_relevant_ratios = defaultdict(lambda: defaultdict(lambda: []))
segments_non_relevant_ratios = defaultdict(lambda: defaultdict(lambda: []))
range_non_relevant_ratios = defaultdict(lambda: defaultdict(lambda: []))
relative_non_relevant_ratios = defaultdict(lambda: defaultdict(lambda: []))
segments_rr_comparison_results = defaultdict(lambda: [])
segments_rn_comparison_results = defaultdict(lambda: [])
segments_nn_comparison_results = defaultdict(lambda: [])
range_rr_comparison_results = defaultdict(lambda: [])
range_rn_comparison_results = defaultdict(lambda: [])
range_nn_comparison_results = defaultdict(lambda: [])
relative_rr_comparison_results = defaultdict(lambda: [])
relative_rn_comparison_results = defaultdict(lambda: [])
relative_nn_comparison_results = defaultdict(lambda: [])


for studentid in validUsers:
    for j in ['1', '3', '4', '5']:
        for d in [1, 2, 3, 4]:
            dwell_time[studentid][j][d] = (reading[studentid][j][d][1] - reading[studentid][j][d][0]) / 1000.0
            perceived_relevance[studentid][j][d] = relevance[studentid][j][d]
            segments_estimated_time[studentid][j][d] = segments_estimation[studentid][j][d]
            segments_ratio[studentid][j][d] = segments_estimation[studentid][j][d] / dwell_time[studentid][j][d]
            range_estimated_time[studentid][j][d] = range_estimation[studentid][j][d]
            range_ratio[studentid][j][d] = range_estimation[studentid][j][d] / dwell_time[studentid][j][d]
            relative_estimated_time[studentid][j][d] = relative_estimation[studentid][j][d]
            relative_ratio[studentid][j][d] = relative_estimation[studentid][j][d] / dwell_time[studentid][j][d]


def normalization_by_user():
    fout = open('../data/normalization_by_user.csv', 'w')
    for studentid in validUsers:
        items = []
        items.append(studentid)
        segments_ratios = []
        range_ratios = []
        relative_ratios = []
        for j in ['1', '3', '4', '5']:
            for d in [1, 2, 3, 4]:
                segments_ratios.append(segments_ratio[studentid][j][d])
                range_ratios.append(range_ratio[studentid][j][d])
                relative_ratios.append(relative_ratio[studentid][j][d])
        segments_ave = np.mean(segments_ratios)
        segments_stda = np.std(segments_ratios)
        range_ave = np.mean(range_ratios)
        range_stda = np.std(range_ratios)
        relative_ave = np.mean(relative_ratios)
        relative_stda = np.std(relative_ratios)
        for j in ['1', '3', '4', '5']:
            for d in [1, 2, 3, 4]:
                items.append(str(perceived_relevance[studentid][j][d]))
                items.append(str(dwell_time[studentid][j][d]))
                items.append(str(segments_estimated_time[studentid][j][d]))
                items.append(str((segments_ratio[studentid][j][d] - segments_ave) / segments_stda))
                items.append(str(range_estimated_time[studentid][j][d]))
                items.append(str((range_ratio[studentid][j][d] - range_ave) / range_stda))
                items.append(str(relative_estimated_time[studentid][j][d]))
                items.append(str((relative_ratio[studentid][j][d] - relative_ave) / relative_stda))
        fout.write(','.join(items))
        fout.write('\n')
    fout.close()

# normalization_by_user()


def pairwise_comparison():
    fout = open('../data/pairwise_comparison.csv', 'w')
    for studentid in validUsers:
        for j in ['1', '3', '4', '5']:
            for d in [1, 2, 3, 4]:
                print studentid, j, perceived_relevance[studentid][j][d]
                if perceived_relevance[studentid][j][d] == -1:
                    if studentid in first_group_users:
                        if job_setting_relevance[1][j][d-1] == 1:
                            segments_relevant_ratios[studentid][j].append(segments_ratio[studentid][j][d])
                            range_relevant_ratios[studentid][j].append(range_ratio[studentid][j][d])
                            relative_relevant_ratios[studentid][j].append(relative_ratio[studentid][j][d])
                        else:
                            segments_non_relevant_ratios[studentid][j].append(segments_ratio[studentid][j][d])
                            range_non_relevant_ratios[studentid][j].append(range_ratio[studentid][j][d])
                            relative_non_relevant_ratios[studentid][j].append(relative_ratio[studentid][j][d])
                    if studentid in second_group_users:
                        if job_setting_relevance[2][j][d-1] == 1:
                            segments_relevant_ratios[studentid][j].append(segments_ratio[studentid][j][d])
                            range_relevant_ratios[studentid][j].append(range_ratio[studentid][j][d])
                            relative_relevant_ratios[studentid][j].append(relative_ratio[studentid][j][d])
                        else:
                            segments_non_relevant_ratios[studentid][j].append(segments_ratio[studentid][j][d])
                            range_non_relevant_ratios[studentid][j].append(range_ratio[studentid][j][d])
                            relative_non_relevant_ratios[studentid][j].append(relative_ratio[studentid][j][d])
                elif perceived_relevance[studentid][j][d] < 2:
                    segments_non_relevant_ratios[studentid][j].append(segments_ratio[studentid][j][d])
                    range_non_relevant_ratios[studentid][j].append(range_ratio[studentid][j][d])
                    relative_non_relevant_ratios[studentid][j].append(relative_ratio[studentid][j][d])
                else:
                    segments_relevant_ratios[studentid][j].append(segments_ratio[studentid][j][d])
                    range_relevant_ratios[studentid][j].append(range_ratio[studentid][j][d])
                    relative_relevant_ratios[studentid][j].append(relative_ratio[studentid][j][d])

            print studentid, j, segments_relevant_ratios[studentid][j], segments_non_relevant_ratios[studentid][j]
            for ratio_r in segments_relevant_ratios[studentid][j]:
                for ratio_n in segments_non_relevant_ratios[studentid][j]:
                    if ratio_r < ratio_n:
                        segments_rn_comparison_results[studentid].append('-1')
                    else:
                        segments_rn_comparison_results[studentid].append('1')
            for ratio_r in range_relevant_ratios[studentid][j]:
                for ratio_n in range_non_relevant_ratios[studentid][j]:
                    if ratio_r < ratio_n:
                        range_rn_comparison_results[studentid].append('-1')
                    else:
                        range_rn_comparison_results[studentid].append('1')
            for ratio_r in relative_relevant_ratios[studentid][j]:
                for ratio_n in relative_non_relevant_ratios[studentid][j]:
                    if ratio_r < ratio_n:
                        relative_rn_comparison_results[studentid].append('-1')
                    else:
                        relative_rn_comparison_results[studentid].append('1')
        fout.write(studentid + 'segments,')
        fout.write(','.join(segments_rn_comparison_results[studentid]))
        fout.write('\n')
        fout.write(studentid + 'range,')
        fout.write(','.join(range_rn_comparison_results[studentid]))
        fout.write('\n')
        fout.write(studentid + 'relative,')
        fout.write(','.join(relative_rn_comparison_results[studentid]))
        fout.write('\n')
    fout.close()

pairwise_comparison()

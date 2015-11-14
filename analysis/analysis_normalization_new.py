__author__ = 'franky'
import re
from collections import defaultdict
import numpy as np
validUsers = ('2015011282', '2015011335','2015011286','2015011312','2015011285','2015011254')
first_group_users = ('2015011282', '2015011312', '2015011285')
second_group_users = ('2015011335', '2015011254', '2015011286')

# calibration -userid ,jobid

begin_calibration = defaultdict(lambda:defaultdict(lambda:[]))
end_calibration = defaultdict(lambda:defaultdict(lambda:[]))
# calibration -userid ,jobid,docid
estimation = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:-1)))
relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
reading = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:[0.0,0.0])))
score = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
raw_right_answer = defaultdict(lambda: defaultdict(lambda: ''))
doc_tran = defaultdict(lambda: defaultdict(lambda: ['', '', '', '']))

etp = re.compile(r'ET=(.*?)\t')
cdp = re.compile(r'CURRENT_DOC=(.*?)\t')
tp = re.compile(r'TIMESTAMP=(.*?)\t')
relp = re.compile(r'REL=(.*?)\t')
ansp = re.compile(r'ANS=(.*?)\t')

for line in open('../data/right_answer.csv').readlines()[1:]:
    id, taskid, raw_docid, title, rightAnswer, choices = line.strip().split(',')
    raw_docid = int(raw_docid)
    if 0 < raw_docid < 7:
        raw_right_answer[int(taskid)][raw_docid] = rightAnswer

for line in open('../data/doc_setting.csv').readlines()[1:]:
    id, jobid, settingid, taskid, docseq = line.strip().split(',')
    doc1, doc2, doc3, doc4 = docseq.split('-')
    doc_tran[settingid][jobid][0] = int(doc1)
    doc_tran[settingid][jobid][1] = int(doc2)
    doc_tran[settingid][jobid][2] = int(doc3)
    doc_tran[settingid][jobid][3] = int(doc4)

for line in open('../data/pilot1.csv').readlines()[1:]:
    id,studentid,jobid,action,content = line.strip().split(',')
    if studentid in validUsers:
        if action == 'BEGIN_CALIBRATION':
            time = int(tp.search(content+'\t').group(1))
            begin_calibration[studentid][jobid].append(time)
        if action =='END_CALIBRATION':
            time = int(tp.search(content+'\t').group(1))
            end_calibration[studentid][jobid].append(time)
        if action == 'TIME_ESTIMATION':
            docid = int(cdp.search(content+'\t').group(1).split(' ')[0])
            et = int(etp.search(content+'\t').group(1).split(' ')[0])
            rel = int(relp.search(content+'\t').group(1).split(' ')[0])
            ans = ansp.search(content+'\t').group(1).split(' ')[0]
            if studentid in first_group_users:
                raw_docid = doc_tran['1'][jobid][docid-1]
                if ans == raw_right_answer[int(jobid)+1][raw_docid]:
                    score[studentid][jobid][docid] = 1
            if studentid in second_group_users:
                raw_docid = doc_tran['4'][jobid][docid-1]
                if ans == raw_right_answer[int(jobid)+1][raw_docid]:
                    score[studentid][jobid][docid] = 1
            # print studentid,jobid,docid,et
            estimation[studentid][jobid][docid] = et
            relevance[studentid][jobid][docid] = rel

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

calibration1_time = defaultdict(lambda: defaultdict(lambda: 0.0))
calibration2_time = defaultdict(lambda: defaultdict(lambda: 0.0))
dwell_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
estimated_time = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
ratio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
perceived_relevance = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
question_score = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

for studentid in validUsers:
    for j in ['1', '2', '3', '4']:
        calibration1_time[studentid][j] = (end_calibration[studentid][j][0]-begin_calibration[studentid][j][0])/1000.0
        calibration2_time[studentid][j] = (end_calibration[studentid][j][1]-begin_calibration[studentid][j][1])/1000.0
        for d in [1, 2, 3, 4]:
            dwell_time[studentid][j][d] = (reading[studentid][j][d][1]-reading[studentid][j][d][0])/1000.0
            estimated_time[studentid][j][d] = estimation[studentid][j][d]
            ratio[studentid][j][d] = estimated_time[studentid][j][d]/dwell_time[studentid][j][d]
            perceived_relevance[studentid][j][d] = relevance[studentid][j][d]
            question_score[studentid][j][d] = score[studentid][j][d]

for studentid in validUsers:
    scores = []
    for j in ['1', '2', '3', '4']:
        for d in [1, 2, 3, 4]:
            scores.append(score[studentid][j][d])
    print studentid, np.mean(scores)

def normalization_by_user_and_job():
    fout = open('../data/normalization_by_user_and_job_new.csv', 'w')
    for studentid in validUsers:
        items = []
        items.append(studentid)
        for j in ['1', '2', '3', '4']:
            items.append(str(calibration1_time[studentid][j]))
            items.append(str(calibration2_time[studentid][j]))
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
    fout = open('../data/normalization_by_user_new.csv', 'w')
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
            items.append(str(calibration1_time[studentid][j]))
            items.append(str(calibration2_time[studentid][j]))
            for d in [1, 2, 3, 4]:
                items.append(str(perceived_relevance[studentid][j][d]))
                items.append(str(question_score[studentid][j][d]))
                items.append(str(dwell_time[studentid][j][d]))
                items.append(str(estimated_time[studentid][j][d]))
                items.append(str((ratio[studentid][j][d]-ave)/stda))
        fout.write(','.join(items))
        fout.write('\n')
    fout.close()


def normalization_by_job():
    fout = open('../data/normalization_by_job_new.csv', 'w')
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
            items.append(str(calibration1_time[studentid][j]))
            items.append(str(calibration2_time[studentid][j]))
            for d in [1, 2, 3, 4]:
                items.append(str((ratio[studentid][j][d]-ratios_ave[j])/ratios_std[j]))
        fout.write(','.join(items))
        fout.write('\n')
    fout.close()


# normalization_by_user_and_job()
# normalization_by_user()
# normalization_by_job()

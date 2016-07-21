from collections import defaultdict

validUsers = {'2015012620': 1, '2015012618': 2, '2015012674': 3, '2014011319': 4, '2015012625': 5, '2015012676': 6,
              '2015012609': 7, '2015012811': 8, '2015012653': 9, '2015012679': 10, '2015012617': 11, '2015012828': 12,
              '2015012642': 13, '2015012624': 14, '2014012759': 15, '2012012767': 16, '2015012623': 17,
              '2014012772': 18, '2015012610': 19, '2011012756': 20, '2014012780': 21, '2015012622': 22,
              '2015012649': 23, '2015011043': 24}

instances = defaultdict(lambda:defaultdict(lambda:[]))

for l in open('output.csv').readlines()[1:]:
    segs = l.strip().split(',')
    userid = segs[0]
    taskid = int(segs[1])
    docid = int(segs[2])
    docrank = int(segs[3])
    prel = int(segs[4])
    dwelltime = float(segs[5])
    time1 = float(segs[6])
    time2_low, time2_high = float(segs[7]),float(segs[8])
    time2 = 0.5*(time2_high+time2_low)
    time3 = float(segs[9])



    instances[validUsers[userid]]['SG'].append(time1/dwelltime)
    instances[validUsers[userid]]['BD'].append(time2/dwelltime)
    instances[validUsers[userid]]['RC'].append(time3/dwelltime)

tired = dict()
interest = dict()

for l in  open('user_interest_tired.txt').readlines():
    user,i,t = [int(item) for item in l.strip().split('\t')]
    tired[user] = t
    interest[user] = i

fout = open('correlation.csv','w')
fout.write('method,Interest,,Tiredness,\n')
fout.write(',pearson\'s r,p-value,kendall\'s tau,p-value\n')
for m in ['SG','BD','RC']:
    from scipy import stats

    import numpy
    series1 = [numpy.mean(instances[i][m]) for i in range(1,25,1)]
    series_tired = [tired[i] for i in range(1,25,1)]
    series_interest = [interest[i] for i in range(1, 25, 1)]
    fout.write(m+',')

    for s in [stats.pearsonr(series1,series_interest),stats.kendalltau(series1,series_interest),stats.pearsonr(series1,series_tired),stats.kendalltau(series1,series_tired)]:
        fout.write(','+str(s[0])+','+str(s[1]))
    fout.write('\n')


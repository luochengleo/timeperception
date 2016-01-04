__author__ = 'luocheng'

from collections import defaultdict

# perceived Rel =
perceivedRel = defaultdict(lambda:defaultdict(lambda:[]))
for l in open("../data/output.csv").readlines()[1:]:
    studentid,taskid,docid,docrank,pr,time1,time2_low,time2_high,time3 = l.strip().split(',')
    perceivedRel[int(taskid)][int(docid)].append(int(pr))

fout = open('relevance_consist.csv','w')
fout.write('Task #,REL1,REL2,IRR1,IRR2\n')
for t in [2,3,4,5]:
    fout.write(str(t))
    for d in [1,2,4,5]:
        count = 0
        for item in perceivedRel[t][d]:
            if d > 3:
                if item <=1:
                    count +=1
            if d < 3:
                if item >=2:
                    count +=1
        fout.write(','+str(float(count)/24.0))
    fout.write('\n')
fout.close()



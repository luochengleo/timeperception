__author__ = 'luocheng'

head = ['userid','relevant_before','taskid', 'estimation','perceived_ratio_bin']

from collections import defaultdict

# userid, taskid ,rel -> (
instances = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:[])))

# segments, range, relative
for l in open('output.csv').readlines()[1:]:
    segs = l.strip().split(',')
    userid = int(segs[0])
    taskid = int(segs[1])
    docid = int(segs[2])
    docrank = int(segs[3])
    prel = int(segs[4])
    dwelltime = float(segs[5])
    time1 = float(segs[6])
    time2_low, time2_high = float(segs[7]),float(segs[8])
    time3 = float(segs[9])

    if prel >=2:
        instances[userid][taskid]['r'].append((docid,docrank,prel,dwelltime,time1,time2_low,time2_high,time3))
    else:
        instances[userid][taskid]['ir'].append((docid,docrank,prel,dwelltime,time1,time2_low,time2_high,time3))


count = 0

user2id = dict()
for u in instances:
    user2id[u] = count
    count +=1


features = []

for u in instances:
    for t in instances[u]:
        for rinst in instances[u][t]['r']:
            for irrinst in instances[u][t]['ir']:
                _userid = u

                if irrinst[1] > rinst[1]:
                    _rel_before = 'False'
                else:
                    _rel_before = 'True'

                import math
                _p_segments = math.log((rinst[3]/irrinst[3])/ (rinst[4]/irrinst[4]))
                _p_range = math.log((rinst[3]/irrinst[3])/  ((rinst[5]+rinst[6])/(irrinst[5]+irrinst[6])))
                _p_relative = math.log((rinst[3]/irrinst[3])/ (rinst[7]/irrinst[7]))

                features.append( [user2id[_userid],_rel_before,t,'SEG',_p_segments])
                features.append( [user2id[_userid],_rel_before,t,'RAN',_p_range])
                features.append( [user2id[_userid],_rel_before,t,'REL',_p_relative])


pratios = []
for l in features:
    pratios.append(l[-1])

pratios.sort()

step = float(len(pratios)/5)


fout = open('data.csv','w')
fout.write(','.join(['U'+ str(item) for item in range(0,len(user2id),1)])+',')
fout.write('RELEVANT_BEFORE,')
fout.write(','.join(['T'+str(item) for item in range(2,6,1)])+',')
fout.write('EST_REG,EST_RAN,EST_REL,')
fout.write('PRATIO_ORD\n')



for l in features:
    print l
    #user
    _p = l[0]
    users = [False]*len(user2id.keys())
    users[_p] = True
    print len(users)
    # relevant_before
    users.append(l[1])
    print len(users)
    # taskid
    tasks = [False]*4
    tasks[l[2]-2]=True

    users += tasks
    print len(users)
    # estimation
    if l[3] == 'SEG':
        users += [True,False,False]
    if l[3] == 'RAN':
        users += [False,True,False]
    if l[3] == 'REL':
        users += [False,False,True]
    print len(users)

    v = int(pratios.index(l[-1])/step)
    if v <= 5:
        users.append(v)
    else:
        users.append(v-1)
    print len(users)
    fout.write(','.join([str(item) for item in users])+'\n')
fout.close()

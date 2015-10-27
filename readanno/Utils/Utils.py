__author__ = 'luocheng'


def str2numseq(s,splitter):
    return [int(item) for item in s.strip().split(splitter)]


def numseq2str(numseq,splitter):
    return [splitter.join([str(item) for item in numseq])]

from django.db import transaction, models
import re
from readanno.models import *


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['TIME', 'USER', 'JOBID','ACTION']}
info_patterns = re.compile('INFO:\\t(.*?)$')
click_info_patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['type', 'result', 'page', 'rank']}
click_info_patterns['src'] = re.compile('src=(.*?)$')


def fromString(line):
    studentID = patterns['USER'].search(line).group(1)
    jobid = patterns['JOBID'].search(line).group(1)
    action = patterns['ACTION'].search(line).group(1)
    logObj = Log.objects.create(studentid=studentID,
                                jobid=jobid,
                                action=action,
                                content=line)
    return logObj



# @transaction.commit_manually
def insertMessageToDB(message):
    try:
        for line in message.split('\n'):
            fout = open('data/all.log','a')
            fout.write(line+'\n')
            print line
            if line == '':
                continue
            log = fromString(line)
            log.save()
    except Exception as e:
        print e
        print 'insert exception'
        # transaction.rollback()
    else:
        print 'commit()'
        # transaction.commit()
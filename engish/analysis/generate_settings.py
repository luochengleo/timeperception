# -*- coding: utf-8 -*-
__author__ = 'franky'

from xml.dom import minidom

task_seq_list = [
    '0-1-2-3-4',
    '0-1-2-4-3',
    '0-1-3-2-4',
    '0-1-3-4-2',
    '0-1-4-2-3',
    '0-1-4-3-2',
    '0-2-1-3-4',
    '0-2-1-4-3',
    '0-2-3-1-4',
    '0-2-3-4-1',
    '0-2-4-1-3',
    '0-2-4-3-1',
    '0-3-1-2-4',
    '0-3-1-4-2',
    '0-3-2-1-4',
    '0-3-2-4-1',
    '0-3-4-1-2',
    '0-3-4-2-1',
    '0-4-1-2-3',
    '0-4-1-3-2',
    '0-4-2-1-3',
    '0-4-2-3-1',
    '0-4-3-1-2',
    '0-4-3-2-1'
]

relevance_seq_list = [
    '3-1-2-3-4',
    '3-1-2-4-3',
    '3-1-3-2-4',
    '3-1-3-4-2',
    '3-1-4-2-3',
    '3-1-4-3-2',
    '3-2-1-3-4',
    '3-2-1-4-3',
    '3-2-3-1-4',
    '3-2-3-4-1',
    '3-2-4-1-3',
    '3-2-4-3-1',
    '3-3-1-2-4',
    '3-3-1-4-2',
    '3-3-2-1-4',
    '3-3-2-4-1',
    '3-3-4-1-2',
    '3-3-4-2-1',
    '3-4-1-2-3',
    '3-4-1-3-2',
    '3-4-2-1-3',
    '3-4-2-3-1',
    '3-4-3-1-2',
    '3-4-3-2-1'
]
relevance_seq_dictionary = {
    '1': '1-2-4-5',
    '2': '4-5-1-2',
    '3': '1-4-2-5',
    '4': '1-4-5-2'
}

doc = minidom.Document()

Settings = doc.createElement('Settings')
doc.appendChild(Settings)

for i in range(1, 25):
    Setting = doc.createElement('Setting')
    Settings.appendChild(Setting)

    settingid = doc.createElement('settingid')
    settingid.appendChild(doc.createTextNode(str(i)))
    Setting.appendChild(settingid)

    taskseq = doc.createElement('taskseq')
    taskseq.appendChild(doc.createTextNode(task_seq_list[i-1]))
    Setting.appendChild(taskseq)

    for j in range(1, 6):
        Job = doc.createElement('Job')
        Setting.appendChild(Job)
        taskid = doc.createElement('taskid')
        taskid.appendChild(doc.createTextNode(str(j)))
        Job.appendChild(taskid)
        docseq = doc.createElement('docseq')
        relevance_seq = relevance_seq_list[i-1]
        index = relevance_seq.split('-')[j-1]
        docseq.appendChild(doc.createTextNode(relevance_seq_dictionary[index]))
        Job.appendChild(docseq)


# 将DOM对象doc写入文件
f = open('../data/English_settings.xml', 'w')
f.write(doc.toprettyxml(indent=''))
f.close()

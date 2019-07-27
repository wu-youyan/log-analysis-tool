# -*- coding:utf-8 -*-
import os
import re
import json
import time
import traceback
import datetime
import configparser

from collections import Counter

from elastic import Elastic
from ConfigOper import *

config = ConfigOper("../conf/config.ini")
history_dir = config.get("history_config", "dir")
history = ConfigOper(history_dir)



class Analysis(object):
    """docstring for Analysis"""
    def __init__(self, project):
        super(Analysis, self).__init__()
        self.project_name = config.get(project,"project_name")
        self.doc_type = config.get(project,"doc_type")
        self.log_format = config.get(project,"log_format")
        self.log_pattern = config.get(project,"log_pattern")
        self.data_dir = config.get(project,"data_dir")
        self.file_filter = config.get(project,"file_filter")
        self.start_pattern = config.get(project,"start_pattern")
        self.multi_line = config.get(project,"multi_line")
        self.match_extline_model = config.get(project,"match_extline_model")
        self.es_host = config.get('elastic_config', 'host')
        self.es_port = config.get('elastic_config', 'port')
        self.es = Elastic({'host':self.es_host,'port':self.es_port})

    def getFileHistory(self, filename):
        projectName = self.project_name+"_"+self.doc_type
        option = filename.replace("/","-")
        res = {}
        fileinfos = "";
        if history.hasOption(projectName,option):
            fileinfos = history.get(projectName,option)
        else:
            if history.hasSection(projectName):
                history.set(projectName,option,"")
            else:
                history.addSection(projectName)
                history.set(projectName,option,"")
                res = self.es.createIndex(self.project_name)
        history.save()
        if fileinfos == "":
            res['last_time'] = 0
            res['read_line'] = 0
        else:
            infoArr = fileinfos.split("|")
            res['last_time'] = infoArr[0]
            res['read_line'] = infoArr[1]
        return res
    def setFileLastOper(self, filename, line,time):
        option = filename.replace("/","-")
        value = str(time)+"|"+str(line)
        history.set(self.project_name+"_"+self.doc_type, option, value)
        history.save()

    def analysisFile(self, filename):
        historyinfo = self.getFileHistory(filename)
        lasttime = os.path.getmtime(filename)
        logFormatList = self.log_format.split()

        pattern = re.compile(self.log_pattern)
        start_pattern = re.compile(self.start_pattern)
        if lasttime>float(historyinfo['last_time']):
            print(filename)
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                oneContent = ""
                oneData = {}
                lineNum = 0;
                for line in f:
                    lineNum += 1
                    if lineNum < int(historyinfo['read_line'])+1:
                        continue
                    oneContent = oneContent+line
                    match = pattern.match(oneContent)
                    start_match = start_pattern.match(line)
                    if match is None:
                        if self.multi_line == 1 and start_match is not None:
                            oneContent = line
                        continue
                    mgroup = match.groups()
                    m = 0
                    for info in mgroup:
                        oneData[logFormatList[m]] = info
                        m += 1
                    # 加入命令行执行产生的默认值
                    if "ip" not in oneData:
                        oneData['ip'] = "127.0.0.1"
                    if "method" not in oneData:
                        oneData['method'] = "cli"
                    
                    self.es.createDoc(self.project_name,self.doc_type,oneData)
                    if int(self.match_extline_model)==1:
                        oneContent = line
                    else:
                        oneContent = "";
                    oneData = {};

            if self.match_extline_model == 1:
                lineNum = lineNum-1

            self.setFileLastOper(filename,lineNum,lasttime)
            print(str(time.time()) + filename+" is update")
        else:
            pass

    def run(self, data_dir):
        file_pattern = re.compile(self.file_filter)
        # 遍历读取其中的文件及文件夹，并记录下当前的历史记录
        for filename in os.listdir(data_dir):
            realfiledir = data_dir+"/"+filename
            if os.path.isdir(realfiledir):
                subdir = data_dir+"/"+filename
                self.run(subdir)
            else:
                match = file_pattern.match(filename)
                if match is None:
                    continue
                self.analysisFile(realfiledir)

def main():
    project_list_str = config.get("analysis_config","project_list")
    project_list = project_list_str.split()
    for project in project_list:
        AnalysisModel = Analysis(project)
        AnalysisModel.run(AnalysisModel.data_dir)

if __name__ == '__main__':
    main()

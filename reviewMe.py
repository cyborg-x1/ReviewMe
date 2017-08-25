#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

This program creates a quit
button. When we press the button,
the application terminates. 

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import yaml
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLineEdit,QVBoxLayout, QMessageBox,QLabel,QDialog,QCalendarWidget,QTreeWidget,QTreeWidgetItem
from os.path import expanduser
from os import stat,mkdir
import requests
import os
import re
import datetime
import PyQt5
from subprocess import call



        


class VacationEndSelector(QDialog):
    qcalendar=None;
    date=0
    result=0
    def __init__(self, user=''):
        super().__init__()
        self.initUI()
        pass
        
    def initUI(self):
        self.setGeometry(300, 600, 250, 150)
        self.setWindowTitle('Vacation Till')    
    
        qlay=QVBoxLayout(self)
        qbtnOk = QPushButton('Ok')
        qbtnCancel = QPushButton('Cancel')
        self.qcalendar=QCalendarWidget()
        
        qlay.addWidget(self.qcalendar)
        qlay.addWidget(qbtnOk)
        qlay.addWidget(qbtnCancel)
        
        qbtnOk.clicked.connect(self.OkButtonClick)
        qbtnCancel.clicked.connect(self.close)
        
        
        
        self.show()
    
    def OkButtonClick(self):
        self.date=self.qcalendar.selectedDate()
        self.result=1
        self.close()
        
    def getDate(self):
        return self.date
        
    def getResult(self):
        return self.result
    
    
class Startup(QDialog):
    username=[]
    password=[]
    vacation=0
    result=0
    values=None
    
    def __init__(self, user=''):
        super().__init__()
        
        self.initUI()
        
        if(len(user)>0):
            self.username.setText(user)
            self.password.setFocus()
        
    def initUI(self):               
        self.setGeometry(300, 600, 250, 150)
        self.setWindowTitle('Startup to Github')    
    
        qlay=QVBoxLayout(self)
        
        qlabelName=QLabel('Username')
        self.username=QLineEdit()
        self.username.setAlignment(Qt.AlignCenter)
        qlabelPassword=QLabel('Password')
        self.password=QLineEdit()
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setEchoMode(QLineEdit.Password)
        
        
        qbtnLogin = QPushButton('Login')
        qbtnVacation = QPushButton('Vacation')
        qbtnAbort = QPushButton('Abort')
        
        qlay.addWidget(qlabelName)
        qlay.addWidget(self.username)
        qlay.addWidget(qlabelPassword)
        qlay.addWidget(self.password)
        
        qlay.addWidget(qbtnLogin)
        qlay.addWidget(qbtnVacation)
        qlay.addWidget(qbtnAbort)
        
        
        qbtnLogin.clicked.connect(self.LoginButtonClick)
        qbtnVacation.clicked.connect(self.VacationButtonClick)
        qbtnAbort.clicked.connect(self.close)

        self.show()
    def VacationButtonClick(self):
        vac=VacationEndSelector()
        vac.exec_()
        if(vac.getResult()==1):
            self.result=2
            self.vacation=vac.getDate()
            self.close()
        pass
        
    def getAuth(self):
        return self.values
    
    def getVacationDate(self):
        return self.vacation
    
    def getResult(self):
        return self.result
         
    def LoginButtonClick(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Missing credentials!")
        msg.setStandardButtons(QMessageBox.Ok)
        
        if len(self.username.text())==0 :
            msg.setText("Missing username")
            msg.exec_()
            return 
        
        if len(self.password.text())==0 :
            msg.setText("Missing password")
            msg.exec_()
            return 
        
        self.result=1
           
        self.values=(self.username.text(), self.password.text())
        self.close()
        
    
    

class ListPulls(QWidget):
    settings=None
    auth=None
    usernamePattern=None
    settings_dir=expanduser("~/.reviewMe")
    settings_path= expanduser("~/.reviewMe/settings.yaml")
    qtreePUIS=None
    orgEntry=None
    repoEntry=None
    
    def checkWorkingTime(self):
        hours=self.settings['working_hours']
        hour=datetime.datetime.now().hour
        
        doQuit=False
        
        if(hour<=hours[0] or hour>=hours[1]):
            print("Out of working time... exiting...")
            doQuit=True
                
        if datetime.datetime.today().weekday() not in self.settings['working_days']:
            print("Not a working day today.... exiting....")
            doQuit=True
            
        try:
            date = datetime.datetime.strptime(self.settings['vacation'], '%Y-%m-%d').date()
            if(date>=datetime.datetime.today().date()):
                print("We are in vacation ... exiting ...")
                doQuit=True
        except:
            pass
        
        if(doQuit):
            #exit(0)
            pass
        
    
    def startup(self):
        try:
            stat(self.settings_dir)
        except:
            mkdir(self.settings_dir)
            
        try:
            stat(self.settings_path)
        except:
            ##TODO create settings...
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Missing settings file!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText("Missing settingsfile")
            msg.exec_()
            exit(1)
            
        
        with open(self.settings_path,"r") as settings_file:
            self.settings=yaml.load(settings_file.read())
            print(self.settings)
        
        self.checkWorkingTime()
        
        login = Startup(self.settings["username"])
        login.exec_()
        result=login.getResult()
        
        if(result == 0):
            print("User aborted login...")
            exit(0)
            pass
        
        elif(result == 1):
            self.auth=login.getAuth()
            
            

        elif(result == 2):
            self.settings["vacation"]=login.getVacationDate().toString("yyyy-MM-dd")
            with open(self.settings_path, 'w') as settingsfile:
                yaml.dump(self.settings, settingsfile)
            exit(0)
            pass
        UN=self.settings["username"]
        self.usernamePattern = re.compile("[^/]"+UN+"[^/]")
        
        
    def __init__(self):
        super().__init__()
        self.startup()
        self.initUI()
        

    
    def initResetTreeWidget(self):
        self.qtreePUIS.clear()          
        pass
        
    def addNotification(self, org, repo, etype, data):
        if(self.orgEntry==None):
            self.orgEntry=QTreeWidgetItem(self.qtreePUIS)
            self.orgEntry.setText(0, org)
            self.orgEntry.setExpanded(True)
        if(self.repoEntry==None):
            self.repoEntry=QTreeWidgetItem(self.orgEntry)
            self.repoEntry.setText(0, repo)
            self.repoEntry.setExpanded(True)
        
        

        if(etype==1):  #Pullrequest
            treeItem=QTreeWidgetItem(self.repoEntry)
            treeItem.setText(0, "Pull {}".format(data['number']) )
            treeItem.setText(1, "https://github.com/"+org+"/"+repo+"/pull/"+str(data['number']) ) 
            pass
        elif(etype==11):  #Pullrequest review
            treeItem=QTreeWidgetItem(self.repoEntry)
            treeItem.setText(0, "Pull {} REVIEW".format(data['number']) )
            treeItem.setText(1, "https://github.com/"+org+"/"+repo+"/pull/"+str(data['number']) )            
            pass   
        elif(etype==12):  #Pullrequest review
            treeItem=QTreeWidgetItem(self.repoEntry)
            treeItem.setText(0, "Pull {} MERGE/CHANGES?".format(data['number']) )
            treeItem.setText(1, "https://github.com/"+org+"/"+repo+"/pull/"+str(data['number']) )            
            pass        
#         elif(etype==13):  #Pullrequest changes
#             treeItem=QTreeWidgetItem(self.repoEntry)
#             treeItem.setText(0, "Pull {} CHANGES".format(data['number']) )
#             treeItem.setText(1, "https://github.com/"+org+"/"+repo+"/pull/"+str(data['number']) )            
#             pass            
        
        elif(etype==2): #Issue
            treeItem=QTreeWidgetItem(self.repoEntry)
            treeItem.setText(0, "Issue {}".format(data['number']) )
            treeItem.setText(1, "https://github.com/"+org+"/"+repo+"/issues/"+str(data['number']) ) 
            pass
        
        elif(etype==0): #0
            treeItem=QTreeWidgetItem(self.repoEntry)
            treeItem.setText(0, "NO CONNECTION!" )  
            pass
        
        else: #0
            treeItem=QTreeWidgetItem(self.repoEntry)
            treeItem.setText(0, "???ERROR??? {}".format(etype) )  
            pass
                
    def itemHandler(self, item, column_no):
        print(item.text(1))
        
        if(item.text(1)!=None):
            call(["firefox", item.text(1)])
        pass

            
    def initUI(self):               
        self.setGeometry(300, 1200, 250, 150)
        self.setWindowTitle('Pullrequests')    

        qlay=QVBoxLayout(self)
        
        self.qtreePUIS=QTreeWidget()
        self.qtreePUIS.itemDoubleClicked.connect(self.itemHandler)
        self.qtreePUIS.setHeaderLabel("Pulls/Issues")
        self.initResetTreeWidget()

        qbtnQuit = QPushButton('Quit', self)
        qlay.addWidget(self.qtreePUIS)
        qlay.addWidget(qbtnQuit)
        qbtnQuit.clicked.connect(QCoreApplication.instance().quit)
        self.update()
        self.show()
        
    def update(self):
        #self.auth=None
        self.checkWorkingTime()
        self.initResetTreeWidget()

        r=requests.get("https://api.github.com/rate_limit", auth=self.auth)
        
        if(r.status_code != 200):
            treeItem=QTreeWidgetItem(self.qtreePUIS)
            treeItem.setText(0, "NO CONNECTION!" )
            return
        
        print(r.content)
           
        for org in self.settings['repos']:
            self.orgEntry=None
                        
            for repo in self.settings['repos'][org]:
                self.repoEntry=None
                
                print(repo)
                p = requests.get("https://api.github.com/repos/"+org+"/"+repo+"/pulls?state=open", auth=self.auth)
                i = requests.get("https://api.github.com/repos/"+org+"/"+repo+"/issues?state=open",auth=self.auth)
                
                
                if(p.status_code != 200 or i.status_code != 200):
                    self.addNotification(org, repo, 0, None)
                    print("NO CONNECTION!")
                    print(i.status_code)
                    print(i.content)
                    print(p.status_code)
                    print(p.content)
                    
                    #TODO Message Box
                    break;
                
                pulls=yaml.load(p.content)
                issues=yaml.load(i.content)
        
                for issue in issues:
                    if("pull_request" not in issue):   
                        issue['grabbed_comments']=yaml.load(requests.get(issue['comments_url'],auth=self.auth).content)
                        #Filter all issues which do not contain the current username
                        dumpedissue=yaml.dump(issue)
                        result = re.search(self.usernamePattern, dumpedissue)
                        print(result)
                        
                        if(result != None):
                            self.addNotification(org, repo, 2, issue)
                
                for pull in pulls:
                    #Download all rev comments and comments and add to the yaml
                    pull['grabbed_comments']=yaml.load(requests.get(pull['_links']['comments']['href'],auth=self.auth).content)
                    pull['grabbed_rev_comments']=yaml.load(requests.get(pull['_links']['review_comments']['href'],auth=self.auth).content)
    
                    #Filter all pullrequests which do not contain the username at all
                    dumpedpull=yaml.dump(pull)
                    result = re.search(self.usernamePattern, dumpedpull)
                    print(dumpedpull)
                    
                    reviewStatus=0
                    #Pull does belong to the user and no reviewers are there ... reviewing done?
                    if(pull['user']['login']==self.settings["username"] and pull['requested_reviewers']==[]):
                        reviewStatus=12
                    else:
                        ##Check for pending review request
                        for reviewer in pull['requested_reviewers']:
                            if(reviewer['login']==self.settings["username"]):
                                reviewStatus=11
                                print("REVIEW!")
                                break
                            
                    if(result != None or reviewStatus>0):
                        t=1
                        if(reviewStatus>0):
                            t=reviewStatus
                            
                        self.addNotification(org, repo, t, pull)
                                                            
  
                pass  
                
                
                

        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    w = ListPulls()
    w.show()
    sys.exit(app.exec_()) 
        
    

    
    
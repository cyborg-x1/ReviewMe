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
from PyQt5.QtCore import QTimer,Qt, QCoreApplication
from PyQt5.QtWidgets import QLineEdit,QVBoxLayout, QMessageBox,QLabel,QDialog,QCalendarWidget,QTreeWidget,QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor
from os.path import expanduser
from os import stat,mkdir
import requests
import os
import re
import datetime
import PyQt5
from subprocess import call
from idlelib.TreeWidget import TreeItem

import socket
import sys
import time

def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        print('I got the lock')
    except socket.error:
        print('lock exists')
        sys.exit()

        



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
    data=None #data yaml
    updateRate=None
    settings=None #settings yaml
    auth=None #auth information for requests
    usernamePattern=None #Pattern for username regex 
    settings_dir=expanduser("~/.reviewMe")
    settings_path= expanduser("~/.reviewMe/settings.yaml")
    data_path= expanduser("~/.reviewMe/data.yaml")
    qTimer = None
    
    qtreePUIS=None #Tree for notifications
    orgEntry=None #Current org entry in tree
    repoEntry=None #Current repo entry in tree
    org=None #Current org
    repo=None #Current repo
    ackClicks=0 #Current clicks on ack for the current entry
    qbtnAck=None #Acknowledge button
    
    
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
            exit(0)
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
        self.readDates()
        self.updateRate=self.settings['update_rate']*60*1000 #In minutes
        
        self.qTimer = QTimer()
        self.qTimer.timeout.connect(self.doUpdate)
        self.qTimer.start(self.updateRate)
        
        
    def __init__(self):
        super().__init__()
        self.startup()
        self.initUI()
        
    def getDateTimeFromGithubStamp(self,date):
        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    
    def GithubStampToDateTime(self, time):
        return time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def setIssueNotifyTime(self,githubtime):
        self.data[self.org][self.repo]=githubtime
    
    def initResetTreeWidget(self):
        self.qtreePUIS.clear()          
        pass
        
    def addNotification(self, etype, entry):
        if(self.orgEntry==None):
            self.orgEntry=QTreeWidgetItem(self.qtreePUIS)
            self.orgEntry.setText(0, self.org)
            self.orgEntry.setExpanded(True)
        if(self.repoEntry==None):
            self.repoEntry=QTreeWidgetItem(self.orgEntry)
            self.repoEntry.setText(0, self.repo)
            self.repoEntry.setExpanded(True)
        

        treeItem=QTreeWidgetItem(self.repoEntry)
        
        mute=False
        #set update time
        if('updated_at' in entry):
            treeItem.setText(2, entry['updated_at'])
            if(self.data != None):
                if(self.org in self.data):
                    if(self.repo in self.data[self.org]):
                        if (entry['number'] in self.data[self.org][self.repo]):
                            print(self.data[self.org][self.repo][entry['number']])
                            stamp_saved=self.data[self.org][self.repo][entry['number']]
                            stamp_current=self.getDateTimeFromGithubStamp(entry['updated_at'])
                            if(stamp_current<=stamp_saved):
                                mute=True
        

        setattr(treeItem, 'id', entry['number'])
            
        
        if(etype==1):  #Pullrequest
            treeItem.setText(0, "P{}".format(entry['number']) )
            treeItem.setText(1, "https://github.com/"+self.org+"/"+self.repo+"/pull/"+str(entry['number']) )
            pass
        elif(etype==11):  #Pullrequest review
            treeItem.setText(0, "P{} REVIEW".format(entry['number']) )
            treeItem.setText(1, "https://github.com/"+self.org+"/"+self.repo+"/pull/"+str(entry['number']) )
            mute=False
            pass   
        elif(etype==12):  #Pullrequest review
            treeItem.setText(0, "P{} CHANGES_REQUESTED".format(entry['number']) )
            treeItem.setText(1, "https://github.com/"+self.org+"/"+self.repo+"/pull/"+str(entry['number']) )
            mute=False
            pass        
#         elif(etype==13):  #Pullrequest changes
#             treeItem=QTreeWidgetItem(self.repoEntry)
#             treeItem.setText(0, "Pull {} CHANGES".format(entry['number']) )
#             treeItem.setText(1, "https://github.com/"+self.org+"/"+self.repo+"/pull/"+str(entry['number']) )            
#             pass            
        
        elif(etype==2): #Issue
            treeItem.setText(0, "I{}".format(entry['number']) )
            treeItem.setText(1, "https://github.com/"+self.org+"/"+self.repo+"/issues/"+str(entry['number']) )
            pass
        
        elif(etype==0): #0
            treeItem.setText(0, "NO CONNECTION!" )
            pass
        
        else: #0
            treeItem.setText(0, "???ERROR??? {}".format(etype) )
            pass
        
        if(mute):
            print("MUTED "+self.org+" "+self.repo+" "+str(entry['number']))
            self.repoEntry.removeChild(treeItem)
            
        
    
    def readDates(self):
        try:
            stat(self.data_path)
            with open(self.data_path,"r") as data_file:
                self.data=yaml.load(data_file.read())
        except:
            self.data=yaml.load("{}")
            
        

    def writeDates(self):
        with open(self.data_path,"w") as data_file:
            yaml.dump(self.data, data_file)

                
    def itemDoubleClickedHandler(self, item, column_no):
        
        if(item.text(1)!=""):
            call(["firefox", item.text(1)])
            

    def itemSelectionChangedHandler(self):
        self.ackClicks=0
        self.qbtnAck.setEnabled(self.qtreePUIS.currentItem().text(2)!="")
        
            
    def initUI(self):               
        self.setGeometry(300, 1200, 400, 500)
        self.setWindowTitle('Pullrequests and Issues')    

        qlay=QVBoxLayout(self)
        
        self.qtreePUIS=QTreeWidget()
        self.qtreePUIS.itemDoubleClicked.connect(self.itemDoubleClickedHandler)
        self.qtreePUIS.itemSelectionChanged.connect(self.itemSelectionChangedHandler)
        self.qtreePUIS.setHeaderLabel("Pulls/Issues")
        self.initResetTreeWidget()

        self.qbtnAck = QPushButton('Ack', self)
        self.qbtnAck.clicked.connect(self.ackClicked)
        self.qbtnAck.setEnabled(False)
        
        qbtnQuit = QPushButton('Quit', self)
        qbtnUpdate = QPushButton('Update', self)
        
        qlay.addWidget(self.qtreePUIS)
        qlay.addWidget(self.qbtnAck)
        qlay.addWidget(qbtnUpdate)
        qlay.addWidget(qbtnQuit)
        
        qbtnQuit.clicked.connect(QCoreApplication.instance().quit)
        qbtnUpdate.clicked.connect(self.doUpdate)

        self.doUpdate()
        self.show()
        
    def ackClicked(self):
        self.ackClicks+=1
        
        
        if(self.ackClicks==2):
            self.ackClicks=0
            self.qbtnAck.setEnabled(False)
            self.clearTreeBackgrounds()
            item=self.qtreePUIS.currentItem()

            #Go up if we do not have an id
            while(item.id==None):
                item=item.parent
                if(item==None):
                    print("No parent this should not have happened!")
                    return;
            
            ident=item.id
            time=self.getDateTimeFromGithubStamp(item.text(2))
            repo=item.parent()
            org=repo.parent()
            
            if(self.data==None):
                self.data=yaml.load("{}")
            
            if(org.text(0) not in self.data):
                self.data[org.text(0)]={}
                
            if(repo.text(0) not in self.data[org.text(0)]):
                self.data[org.text(0)][repo.text(0)]={}
            
                        
            self.data[org.text(0)][repo.text(0)][ident]=time
            self.writeDates()
            
            #Remove item
            item.removeChild(item)
        else:
            self.clearTreeBackgrounds()
            self.qtreePUIS.currentItem().setBackground(0,QBrush(QColor(0,255,0)) )
            pass
            
    
    def dateCheck(self,treeItem,time=None):
        if(treeItem.text(2)!=""): #Check if there is a time for this entry
            if(time==None):#Check if we have a time no time yet
                time=self.getDateTimeFromGithubStamp(treeItem.text(2))#get the time of the current one cause its the start
            else:#We have a time so we are in a parent of the selection
                for c in range(treeItem.childCount()): #lets check the other children
                    child=treeItem.child(c)#get it
                    timeChild=self.getDateTimeFromGithubStamp(child.text(2))#get childs time
                    if(timeChild<=time):#check if childs time is smaller or equal
                        self.setTreeChildrenBackground(child,QColor(0,255,0)) #mark it with all its children
        else:
            return #leave if no time entry
        self.dateCheck(treeItem.parent, time)   
                
    
    def setTreeChildrenBackground(self,treeItem,color=QColor(255,255,255)):
        treeItem.setBackground(0,QBrush(color) )
        for c in range(treeItem.childCount()):
            self.setTreeChildrenBackground(treeItem.child(c))
        
    def clearTreeBackgrounds(self):
        self.setTreeChildrenBackground(self.qtreePUIS.invisibleRootItem())
    
    
    def doUpdate(self):
        self.qTimer.stop()
        self.setEnabled(False)
        self.checkWorkingTime()
        self.initResetTreeWidget()

        r=requests.get("https://api.github.com/rate_limit", auth=self.auth)
        
        if(r.status_code != 200):
            treeItem=QTreeWidgetItem(self.qtreePUIS)
            treeItem.setText(0, "NO CONNECTION!" )
            return
        
           
        for self.org in self.settings['repos']:
            self.orgEntry=None
                        
            for self.repo in self.settings['repos'][self.org]:
                self.repoEntry=None
                
                p = requests.get("https://api.github.com/repos/"+self.org+"/"+self.repo+"/pulls?state=open", auth=self.auth)
                i = requests.get("https://api.github.com/repos/"+self.org+"/"+self.repo+"/issues?state=open",auth=self.auth)
                
                
                if(p.status_code != 200 or i.status_code != 200):
                    self.addNotification(0, None)
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
                        
                        if(result != None):
                            self.addNotification(2, issue)
                
                for pull in pulls:
                    #Download all rev comments and comments and add to the yaml
                    pull['grabbed_comments']=yaml.load(requests.get(pull['_links']['comments']['href'],auth=self.auth).content)
                    pull['grabbed_rev_comments']=yaml.load(requests.get(pull['_links']['review_comments']['href'],auth=self.auth).content)
                    pull['reviews']=yaml.load(requests.get("https://api.github.com/repos/"+self.org+"/"+self.repo+"/pulls/"+str(pull['number'])+"/reviews",auth=self.auth).content)
                    
                    
                    #Filter all pullrequests which do not contain the username at all
                    dumpedpull=yaml.dump(pull)
                    result = re.search(self.usernamePattern, dumpedpull)
                    
                    reviewStatus=0
                    #Pull does belong to the user and no reviewers are there ... reviewing done?
                    if(pull['user']['login']==self.settings["username"] and pull['reviews']!=[]):
                        
                        #Check reviews
                        for review in pull['reviews']:
                            if(review['state']=="CHANGES_REQUESTED"):
                                
                                #Check if reviewer is already called in again...
                                rereview=False
                                for reviewer in pull['requested_reviewers']:
                                    if(reviewer['login']==review["user"]["login"]):
                                        rereview=True
                                        break
                                
                                if(not rereview):
                                    reviewStatus=12
                                
                                break
                            
                        
                        
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
                            
                        self.addNotification(t, pull)
                                                            
  
                
        self.setEnabled(True)
        self.qTimer.start(self.updateRate)
        self.show()
        self.activateWindow()
                
                

        
if __name__ == '__main__':
    get_lock('ReviewMe')
    app = QApplication(sys.argv)
    w = ListPulls()
    w.show()
    sys.exit(app.exec_()) 
        
    

    
    
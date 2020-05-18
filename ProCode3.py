import openpyxl as op
import numpy as np
import pandas as pd
from datetime import datetime, date
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook
#https://stackoverflow.com/questions/20219254/how-to-write-to-an-existing-excel-file-without-overwriting-data-using-pandas

membersdata=pd.read_excel("Record2.xlsx")
activitydata=pd.read_excel("Parking4.xlsx")
spotdata=pd.read_excel("Spots.xlsx")
memberdict={}
spotsdictbyspotnum={}
spotdictbylic={}

class spot:
    def __init__(self, spotnum, spottype, status, license, parkingrownum):
        self.spotnum=spotnum
        self.spottype=spottype
        self.status=status
        self.license=license
        self.parkingrownum=parkingrownum
    def __repr__(self):
        return "<spot is spotnum:%s \n spottype:%s \n status:%s \n license:%s \n parkingrownum:%s \n" % (self.spotnum, self.spottype, self.status, self.license, self.parkingrownum)

    def __str__(self):
        return "From str method of spot: spotnum:%s \n spottype:%s \n status:%s \n license:%s \n parkingrownum:%s \n" % (self.spotnum, self.spottype, self.status, self.license, self.parkingrownum)

class member:
    def __init__(self, isMember, name, car, licenseno, reporttime, spot, rownum):
        self.isMember=isMember
        self.name=name
        self.car=car
        self.licenseno=licenseno
        self.reporttime=reporttime
        self.spot=spot
        self.medianearly=0
        self.medianlate=0
        self.avgearly=0
        self.avglate=0
        self.rownum=rownum
        
        self.activity_parkdate=[]
        self.activity_reportdatetime=[]
        self.activity_entrydatetime=[]
        self.activity_spot=[]
        self.activity_early=[]
        self.activity_late=[]
        self.activity_exitdatetime=[]
        self.activity_rownum=[]
        
    def __repr__(self):
        return "<record name:%s \n car:%s \n licenseno:%s \n reporttime:%s \n spot:%s \n" \
        " medianearly:%s \n medianlate:%s \n rownum:%s>\n" % (self.name, self.car, self.licenseno, self.reporttime, self.spot, self.medianearly, self.medianlate, self.rownum)

    def __str__(self):
        return "From str method of record: name is %s \n, car is %s \n licenseno:%s \n" \
        " reporttime:%s \n spot:%s \n medianearly:%s \n medianlate:%s \n rownum:%s>\n" % (self.name, self.car, self.licenseno, self.reporttime, self.spot, self.medianearly, self.medianlate, self.rownum)

#def loadspreadsheet():
    
      
def lookuplicense(lic):
    if lic in memberdict:
        m=memberdict[lic]
        return m
    else:
        return None

def loadmemdict():
    for x in range(len(membersdata)):
        m=member(True, membersdata.Name[x], membersdata.Car[x], membersdata.License[x], membersdata.Report_DateTime[x], membersdata.Spot[x], x)
        memberdict[m.licenseno]=m
    print(memberdict)

    for x in range(len(activitydata)):
        m=lookuplicense(activitydata.License[x])
        if m==None:
            m=member(False, 'Outsider', "", activitydata.License[x], activitydata.Report_DateTime[x], activitydata.Spot[x], -1)
            memberdict[m.licenseno]=m
        m.activity_parkdate.append(activitydata.ParkDate[x])
        m.activity_reportdatetime.append(activitydata.Report_DateTime[x])
        m.activity_entrydatetime.append(activitydata.Entry_DateTime[x])
        m.activity_spot.append(activitydata.Spot[x])
        print(type(activitydata.Report_DateTime[x]))
        print(type(activitydata.Entry_DateTime[x]))
        sec=0
        if (isinstance(activitydata.Report_DateTime[x],str) and isinstance(activitydata.Entry_DateTime[x],str)):
            datetime_rdt = datetime.strptime(str(activitydata.Report_DateTime[x].strip()), '%d-%m-%Y %H:%M:%S')
            datetime_edt = datetime.strptime(str(activitydata.Entry_DateTime[x].strip()), '%d-%m-%Y %H:%M:%S')
            el=datetime_rdt-datetime_edt
            #el=datetime.combine(date.min, activitydata.Report_DateTime[x]) - datetime.combine(date.min, activitydata.Entry_DateTime[x])
            print(type(el))
            print(el.total_seconds())
            
            sec=el.total_seconds()
            print('sec:',sec)

        if sec>=0:
            m.activity_early.append(sec)
            m.activity_late.append(0)
        else:
            m.activity_early.append(0)
            m.activity_late.append(abs(sec))

        m.activity_exitdatetime.append(activitydata.Exit_DateTime[x])
        m.activity_rownum.append(x)
        print("------")
        print(m.name)
        print("isMember")
        print(m.isMember)
        print('licenseno')
        print(m.licenseno)
        print('parkdate')
        print(m.activity_parkdate)
        print('reportdatetime')
        print(m.activity_reportdatetime)
        print('entrydatetime')
        print(m.activity_entrydatetime)
        print('spot')
        print(m.activity_spot)
        print('early')
        print(m.activity_early)
        print('late')
        print(m.activity_late)
        print('exitdatetime')
        print(m.activity_exitdatetime)
        print('rownum')
        print(m.activity_rownum)
        
def loadspots():
    for x in range(len(spotdata)):
        s=spot(spotdata.Spot_No[x], spotdata.Type[x], spotdata.Status[x], spotdata.License[x], spotdata.Parking_Rownum[x])
        spotsdictbyspotnum[s.spotnum]=s
        spotdictbylic[s.license]=s
    print(spotsdictbyspotnum)

def calcmedavg():
    for am in memberdict:
        m=memberdict[am]
        m.medianearly=np.median(m.activity_early)
        m.medianlate=np.median(m.activity_late)
        m.avgearly=np.average(m.activity_early)
        m.avglate=np.average(m.activity_late)
        print(m.name, 'earlymedian', m.medianearly)
        print(m.name, 'latemedian', m.medianlate)
        print(m.name, 'earlyavg', m.avgearly)
        print(m.name, 'lateavg', m.avglate)
                
def UpdateMedianAvgIntoMemberExcel():
    for x in memberdict:
        m=memberdict[x]
        membersdata.Median_Early[m.rownum]=m.medianearly
        membersdata.Median_Late[m.rownum]=m.medianlate
        membersdata.Avg_Early[m.rownum]=m.avgearly
        membersdata.Avg_Late[m.rownum]=m.avglate
    with pd.ExcelWriter("Record2.xlsx",
                    engine='xlsxwriter',
                    datetime_format='dd-mm-yyyy hh:mm:ss',
                    date_format='dd-mm-yyyy') as writer:
        membersdata.to_excel(writer, sheet_name='Members')

def UpdateEarlyLateIntoParkingExcel():
    for x in memberdict:
        m=memberdict[x]
        for i in range(len(m.activity_rownum)):
            #activityRownum = m.activity_rownum[i]
            if m.isMember == True:  
                activitydata.Early[m.activity_rownum[i]] = m.activity_early[i]
                activitydata.Late[m.activity_rownum[i]]  = m.activity_late[i]
                activitydata.Parker[m.activity_rownum[i]] = m.name
            else:
                activitydata.Early[m.activity_rownum[i]] = 0
                activitydata.Late[m.activity_rownum[i]]  = 0
                activitydata.Parker[m.activity_rownum[i]] = m.name
    with pd.ExcelWriter("Parking4.xlsx",
                engine='xlsxwriter',
                datetime_format='dd-mm-yyyy hh:mm:ss',
                date_format='dd-mm-yyyy') as writer:
        activitydata.to_excel(writer, sheet_name='Parking')

def AddActivityEntry(lic,parkdate,entry_datetime,spot):
    m=lookuplicense(lic)
    if m==None:
        m=member(False, 'Outsider', "", lic, entry_datetime, spot, -1)
        memberdict[lic]=m
    m.activity_parkdate.append(parkdate)
    m.activity_reportdatetime.append(parkdate+" "+m.reporttime)
    m.activity_entrydatetime.append(entry_datetime)
    m.activity_spot.append(spot)
    print(type(m.reporttime))
    print(type(entry_datetime))
    sec=0
    print(parkdate+" "+m.reporttime)
    print(m.activity_entrydatetime)
    if (isinstance(m.reporttime,str) and  isinstance(entry_datetime,str)):
        datetime_rdt = datetime.strptime(str(parkdate+" "+m.reporttime.strip()), '%d-%m-%Y %H:%M:%S')
        datetime_edt = datetime.strptime(str(entry_datetime.strip()), '%d-%m-%Y %H:%M:%S')
        el=datetime_rdt-datetime_edt
        #el=datetime.combine(date.min, activitydata.Report_DateTime[x]) - datetime.combine(date.min, activitydata.Entry_DateTime[x])
        print(type(el))
        print(el.total_seconds())
        
        sec=el.total_seconds()
        print('sec:',sec)

    if sec>=0:
        m.activity_early.append(sec)
        e=sec
        m.activity_late.append(0)
        l=0
    else:
        m.activity_early.append(0)
        e=0
        m.activity_late.append(abs(sec))
        l=sec

    m.activity_exitdatetime.append("")
    m.activity_rownum.append(len(m.activity_rownum)+1)
    new_row = {'Parker':m.name, 
                'License':m.licenseno,	
                'ParkDate':parkdate,	
                'Report_DateTime':m.reporttime,	
                'Entry_DateTime':entry_datetime,	
                'Spot':spot,	
                'Early':e,	
                'Late':l,	
                'Exit_DateTime':"",	
                'CarImage_Path':""}

    activitydata.append(new_row, ignore_index=True)



#Program starts here
loadmemdict()
loadspots()
calcmedavg()
UpdateMedianAvgIntoMemberExcel()
AddActivityEntry("blahblah","12-05-2020 10:00:00","12-05-2020 10:55:00",9)
AddActivityEntry("MH43AE1234","12-05-2020 10:00:00","12-05-2020 10:55:00",8)

UpdateEarlyLateIntoParkingExcel()

y=lookuplicense('MH04SS666')    
if (y==None):
    print('Outsider')
else:
    print(y.name,y.car,y.licenseno)
                
i=input("License plate number: ")

#df = enter(i)
wb = op.load_workbook('Parking3.xlsx')
ws = wb['Parking']
ws.append(df)
wb.save('Parking3.xlsx')
wb.close()
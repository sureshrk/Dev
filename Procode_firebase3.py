import pyrebase
import json

firebaseConfig = {
    "apiKey": "AIzaSyAFZiL2lRvdhqhdgYskCCXsKFnIwrR2FTc",
    "authDomain": "smart-parking-f580f.firebaseapp.com",
    "databaseURL": "https://smart-parking-f580f.firebaseio.com",
    "projectId": "smart-parking-f580f",
    "storageBucket": "smart-parking-f580f.appspot.com",
    "messagingSenderId": "724535193663",
    "appId": "1:724535193663:web:385d64a54e034849a6088a",
    "measurementId": "G-SS1QJP0KXB"
  }

firebase = pyrebase.initialize_app(firebaseConfig)


# CRUD functions for Member table.
''' 
    {
        "Id": "0",
        "Name": "Mr. Ganesh Verma",
        "Car": "Honda Jazz",
        "License": "MH43AE1234",
        "Report_DateTime": " 10:00:00",
        "Spot": "1",
        "Median_Early": "0",
        "Median_Late": "-545.5",
        "Avg_Early": "",
        "Avg_Late": ""
    }
'''
'''class Member :
        Id
        Name
        Car
        License
        Report_DateTime
        Spot
        Median_Early
        Median_Late
        Avg_Early
        Avg_Late
'''

def AddMember():
    return

   
def ReadMember():
    data = db.child("Members").get()
    members=data.val()
    print("Members type")
    print(type(members))
    print(members)
    member=members['MH01DG1123']
    print("Member type")
    print(type(member))
    print(member)
    return


def UpdateMember():
    return


def DeleteMember():
    return



# CRUD functions for Spots table.
'''
    [
    {
        "Spot":1,
        "Type":"Member",
        "Status":"Vacant",
        "License":"",
        "Parking_Rownum":""
    },
    {
        "Spot":2,
        "Type":"Member",
        "Status":"Vacant",
        "License":"",
        "Parking_Rownum":""
    }
    ]
'''
class Spot:
    Spot=0
    Type=""
    Status=""
    License=""
    Parking_Rownum=0

def AddSpot():
    return


def ReadSpot():
    data = db.child("Spots").get()
    spots=data.val()
    print(type(spots))
    print(str(spots))
    print(spots)
    print(spots[0].values)
    print(spots[0])
    print(spots[0]['Spot'])
   
    



def UpdateSpot():
    return


def DeleteSpot():
    return



# CRUD functions for Activity table.
def AddActivity():
    return


def ReadActivity():
    data = db.child("Activity").get()
    activity=data.val()
    print('---------')
    print("activity type")
    print(type(activity))
    print(activity)
    print("---------------------------")
    activityItem=activity['MH01DG1123']
    print("activityItem[0] type")
    print(type(activityItem[0]))
    print(activityItem[0])
    return


def UpdateActivity():
    return


def DeleteActivity():
    return

db = firebase.database()
ReadSpot()
ReadMember()
ReadActivity()
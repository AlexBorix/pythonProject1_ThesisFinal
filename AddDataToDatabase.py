import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancethesisproject-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "000001" :
        {
            "name": "Mme SOUDRE",
            "major": "IT",
            "starting_year": 2015,
            "total_attendance": 3,
            "standing": "B",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34",

        },
"321654" :
        {
            "name": "Hamado",
            "major": "Dev",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34",

        },
"852741" :
        {
            "name": "Naomi",
            "major": "Mgm",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34",

        },
"963852" :
        {
            "name": "Boris",
            "major": "Thesis",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34",

        },
}

for key,value in data.items():
    ref.child(key).set(value) #we use child because it is a specific directory
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartattend-9e9f9-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    "a22ec0093":
        {
            "name": "Neo Zheng Weng",
            "major": "DE",
            "cohort": 2026,
            "tot_attendance": 10,
            "cgpa": 4.00,
            "year": 3,
            "latest_attendance": "2024-9-10 13:32:20"
        },
    "a21km12234":
        {
            "name": "Emily",
            "major": "CS",
            "cohort": 2025,
            "tot_attendance": 12,
            "cgpa": 3.90,
            "year": 4,
            "latest_attendance": "2024-9-10 13:32:20"
        },
    "a23cs0055":
        {
            "name": "Elon Musk",
            "major": "AI",
            "cohort": 2027,
            "tot_attendance": 8,
            "cgpa": 3.97,
            "year": 2,
            "latest_attendance": "2024-9-10 13:32:20"
        }
}

# Add data to firebase
for key, value in data.items():
    ref.child(key).set(value)
    
print("Data uploaded to Firebase db.")
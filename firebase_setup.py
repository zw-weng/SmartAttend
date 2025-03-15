import firebase_admin
from firebase_admin import credentials, storage, db

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartattend-9e9f9-default-rtdb.firebaseio.com/',
    'storageBucket': 'smartattend-9e9f9.appspot.com'
})

# Export Firebase services
firebase_db = db
firebase_storage = storage
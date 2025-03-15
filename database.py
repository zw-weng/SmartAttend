from firebase_setup import firebase_db  # Import Firebase database from setup file
from datetime import datetime

def upload_student_data():
    """Uploads predefined student data to Firebase Realtime Database."""
    students_data = {
        "a22ec0093": {
            "name": "Neo Zheng Weng",
            "major": "DE",
            "cohort": 2026,
            "tot_attendance": 10,
            "cgpa": 4.00,
            "year": 3,
            "latest_attendance": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "a21km12234": {
            "name": "Emily",
            "major": "CS",
            "cohort": 2025,
            "tot_attendance": 12,
            "cgpa": 3.90,
            "year": 4,
            "latest_attendance": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "a23cs0055": {
            "name": "Elon Musk",
            "major": "AI",
            "cohort": 2027,
            "tot_attendance": 8,
            "cgpa": 3.97,
            "year": 2,
            "latest_attendance": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    try:
        ref = firebase_db.reference('Students')
        for student_id, student_info in students_data.items():
            ref.child(student_id).set(student_info)
        print("Data uploaded successfully.")
    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    upload_student_data()
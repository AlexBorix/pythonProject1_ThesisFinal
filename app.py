from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db, storage
import os

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancethesisproject-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancethesisproject.appspot.com"
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        # Fetch form data
        student_id = request.form['student_id']
        name = request.form['name']
        major = request.form['major']
        year = request.form['year']
        image = request.files['image']

        # Save student data to Firebase Database
        ref = db.reference('Students')
        student_data = {
            "name": name,
            "major": major,
            "total_attendance": 0,
            "year": year,
            "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        ref.child(student_id).set(student_data)

        # Save image to Firebase Storage
        image_path = os.path.join('Images', student_id + '.png')
        image.save(image_path)
        blob = storage.bucket().blob(image_path)
        blob.upload_from_filename(image_path)

        return redirect(url_for('index'))

    except KeyError as e:
        return f"Missing form field: {e}", 400

    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/students')
def students():
    try:
        # Fetch query parameters
        major_filter = request.args.get('major', default=None)
        year_filter = request.args.get('year', default=None)

        # Fetch student data from Firebase Database
        ref = db.reference('Students')
        students = ref.get()

        filtered_students = {}
        years_set = set()   # Set to store unique years
        majors_set = set()  # Set to store unique majors
        if students:
            for student_id, student in students.items():
                if (not major_filter or student['major'] == major_filter) and (not year_filter or student['year'] == year_filter):
                    filtered_students[student_id] = student
                years_set.add(student['year'])
                majors_set.add(student['major'])

        years = sorted(years_set)     # Sort unique years
        majors = sorted(majors_set)   # Sort unique majors

        return render_template('students.html', students=filtered_students, years=years, majors=majors, majorFilter=major_filter, yearFilter=year_filter)

    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
#jai le tableau plus les recherche fonctionnels
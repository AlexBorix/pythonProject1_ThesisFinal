from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db, storage
import os
import cv2
import face_recognition
import pickle

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancethesisproject-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancethesisproject.appspot.com"
})

bucket = storage.bucket()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    student_id = request.form['student_id']
    name = request.form['name']
    major = request.form['major']
    starting_year = request.form['starting_year']
    year = request.form['year']
    standing = request.form['standing']
    image = request.files['image']

    # Save student data to Firebase Database
    ref = db.reference('Students')
    student_data = {
        "name": name,
        "major": major,
        "starting_year": int(starting_year),
        "total_attendance": 0,
        "standing": standing,
        "year": int(year),
        "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    ref.child(student_id).set(student_data)

    # Save image to Firebase Storage
    image_path = os.path.join('Images', student_id + '.png')
    image.save(image_path)
    blob = bucket.blob(image_path)
    blob.upload_from_filename(image_path)

    # Encode the image and update encoding file
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img_rgb)[0]

    try:
        with open("EncodeFile.p", 'rb') as file:
            encodeListKnownWithIds = pickle.load(file)
    except FileNotFoundError:
        encodeListKnownWithIds = [[], []]

    encodeListKnownWithIds[0].append(encode)
    encodeListKnownWithIds[1].append(student_id)

    with open("EncodeFile.p", 'wb') as file:
        pickle.dump(encodeListKnownWithIds, file)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, Response
import sys
import numpy
import face_recognition
import os
from mss import mss

app = Flask(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


@app.route('/')
def index():
    return render_template('home.html')




def takesc():
    with mss() as sct:
        sct.shot()

@app.route('/takeScreenshot')
def takeScreenshot():
    takesc()
    return render_template('home.html')



victim = ''
def checkImg():
    try:
        known_image = face_recognition.load_image_file("monitor-1.png")
        unknown_image = face_recognition.load_image_file("me.jpg")
        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
        if results[0] == 1:
            victim = "Face Found:/. Mohamed Gharibi"
            return victim
        elif results[0] == 0:
            unknown_image = face_recognition.load_image_file("khaled.jpg")
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
            if results[0] == 1:
                victim = ""
                return victim
            return "Captured face is not in the DB..."
    except Exception:
        results = "No face was detected"
    return results


def isCriminal(victim):
    free = ''
    if victim == "Face Found:/. Mohamed Gharibi":
        free = ""
    elif victim == "Captured face is not in the DB..." or victim == "":
        free = ""
    else:
        free = ""
    return free

@app.route('/checkImage')
def checkImage():
    myResult = checkImg()
    free = isCriminal(myResult)
    return render_template('home.html', myResult= myResult, free=free)



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
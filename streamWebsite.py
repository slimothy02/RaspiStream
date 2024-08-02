## This program follows the streaming guide at https://towardsdatascience.com/video-streaming-in-web-browsers-with-o>
from flask import Flask, render_template, Response, flash, request, redirect, url_for, escape
import cv2
import os
from picamera2 import Picamera2
import numpy as np

#initialize FLask app
app = Flask(__name__)

#initialize camrea object
vid = Picamera2()
config = vid.create_preview_configuration({'format': 'MJPEG'})   # correct video color
vid.configure(config)
vid.start()
_ = vid.capture_array()  # read first frame & throw away

#generates video stream
def gen_frames():
        while True:
                try:
                        frame = vid.capture_array()
                        #frame = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)    # fixes the red & blue color switch
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e :
                        print("Error: "+e)
                        break

#define route for the default page of the app
@app.route("/")
def index():
        return render_template('index.html')

#define route that allows saved infoboxes text to be shown on boot & save infobox text via button press
@app.route('/', methods=['POST'])
def infobox_write():
        if request.method == 'POST':

                # See what the set text is for infoboard
                file1 = open("infobox1.txt","r")
                file2 = open("infobox2.txt","r")
                file3 = open("infobox3.txt","r")
          
                f1 = file1.read()
                f2 = file2.read()
                f3 = file3.read()

                file1.close()
                file2.close()
                file3.close()

                # See what user has written on infoboard
                file1 = open("infobox1.txt","w")
                file2 = open("infobox2.txt","w")
                file3 = open("infobox3.txt","w")

                input_1 = request.form["box_1"]
                input_2 = request.form["box_2"]
                input_3 = request.form["box_3"]

                file1.write(str(input_1))
                file2.write(str(input_2))
                file3.write(str(input_3))

                file1.close()
                file2.close()
                file3.close()

                # If the user changed text on the infoboard, display it after pressing submit button
                if f1 != input_1:
                        f1 = input_1
                if f2 != input_2:
                        f2 = input_2
                if f3 != input_3:
                        f3 = input_3
                return render_template('index.html',input_1=f1,input_2=f2,input_3=f3)

#define route for the stream to be shown on the app
@app.route('/video_feed')
def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
        app.run(debug=True)

from pyimagesearch.covid_simulation import SingleCovidSimulator
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

outputFrame = None
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")
def generate():
	global outputFrame
	cs = SingleCovidSimulator(rVals=(1.1, 1.4))
	while True:
		outputFrame = cs.read().copy()
		cs.update()
		if outputFrame is None:
			continue
		else:
			ret, buffer = cv2.imencode('.jpg', outputFrame)
			frame = buffer.tobytes()
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
	app.run(debug=True)
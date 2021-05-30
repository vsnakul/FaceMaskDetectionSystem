# USAGE
# python detect_mask_video.py

# import the necessary packages
import download_image_firebase
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

def detect_and_predict_mask(frame, faceNet, maskNet):
	print("Constructing Blob....")
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print("Performing Detections...")
	faces = []
	locs = []
	preds = []
	for i in range(0, detections.shape[2]):
		print("Looping over the detections...")
		confidence = detections[0, 0, i, 2]
		if confidence > args["confidence"]:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)
			print("Appending faces to the list...")
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	if len(faces) > 0:
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	return (locs, preds)

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
# loop over the frames from the video stream
class VideoCamera(object):
	def __init__(self):
		# capturing video
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		# releasing camera
		self.video.release()
	def get_frame(self):
		while True:
			print("get_frame() method called again")
			print("Grabbing the faces and resizing...")
			ret, frame = self.video.read()
			frame = imutils.resize(frame, width=400)

			(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

			for (box, pred) in zip(locs, preds):

				(startX, startY, endX, endY) = box
				(mask, withoutMask) = pred
				print("Detection completed...")

				label = "Mask" if mask > withoutMask else "No Mask"
				color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

				label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

				cv2.putText(frame, label, (startX, startY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
				cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
				# actualStartX=startX
				# actualStartY=startY
				# actualendX=endX
				# actualendY=endY
				#cv2.line(frame,(startX,startY),(startX+15,startY),color,2)
				#startX=startX+15
				#cv2.line(frame,(startX+7,startY),(startX+25,startY),color,2)
				gap=7
				# x1=startX
				# y1=startY
				# x2=endX
				# y2=endY
				# length=15
				# #draws the top horizontal
				# while True:
				# 	cv2.line(frame, (x1, actualStartY), (x1+length,actualStartY), color, 2)
				# 	x1=x1+7+length
				# 	print("inside my while loop")
				# 	if(x1>=actualendX):
				# 		break
				# #draws the right vertical
				# while True:
				# 	cv2.line(frame, (actualendX, y1), (actualendX, y1-length), color, 2)
				# 	y1=y1-length-7
				# 	print("inside my while loop")
				# 	if(y1<=endY):
				# 		break




				print("value of start x ",startX)
				print("value of start y ",startY)
				print("value of end x ",endX)
				print("value of start x ",endY)
			ret, jpeg = cv2.imencode('.jpg', frame)
			frames=jpeg.tobytes()
			return frames

		# show the output frame
		#cv2.imshow("Frame", frame)
		#key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		#if key == ord("q"):
			#break

# do a bit of cleanup

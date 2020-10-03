import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2

MASKCONFIDENCE = 0.2
FACECONFIDENCE = 0.5

def loader_face():
	print("[INFO] loading face detector model...")
	net = cv2.dnn.readNet("./models/deploy.prototxt", "./models/res10_300x300_ssd_iter_140000.caffemodel")
	return net

def loader_mask():
	print("[INFO] loading face mask detector model...")
	model = tf.keras.models.load_model('./models/mask_detector_model')
	return model

######################################################################
def imager(image_path):
	if image_path == '':
		image_path = myPath

	print(image_path)

	image = cv2.imread(image_path)
	print(image.shape)
	(h, w) = image.shape[:2]
	return image, w, h

#######################################################################
def calculate(image,net):
	print("[INFO] Loading Image")
	blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),(104.0, 177.0, 123.0))

	print("[INFO] computing face detections...")
	net.setInput(blob)
	detections = net.forward()
	return detections

def loop(image,detections,model,w,h):
	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		
		if confidence > MASKCONFIDENCE:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			face = image[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)
			face = np.expand_dims(face, axis=0)

			(mask, withoutMask) = model.predict(face)[0]

	#######################################################################################
			if(mask>FACECONFIDENCE or withoutMask>FACECONFIDENCE):
				label = "Mask" if mask > withoutMask else "No Mask"
				color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
	#######################################################################################
			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

			cv2.putText(image, label, (startX, startY - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
	
	
	return image
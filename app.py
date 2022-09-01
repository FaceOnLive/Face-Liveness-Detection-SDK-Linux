import sys
sys.path.append('.')

import cv2
import numpy as np
from flask import Flask, request, jsonify
from time import gmtime, strftime
import logging
import uuid
from flask_cors import CORS
import os
import base64

from facewrapper.facewrapper import InitEngine
from facewrapper.facewrapper import GetLiveness
from facewrapper.facewrapper import ProcessAll
from facewrapper.facewrapper import CompareFace

import json

CUSTOMER_TOKENS = [
####### 07.05 #######
  ]


app = Flask(__name__)
CORS(app)

licensePath = os.path.abspath(os.path.dirname(__file__)) + '/facewrapper/license.txt'
InitEngine(licensePath.encode('utf-8'))

@app.route('/face/liveness', methods=['POST'])
def detect_livness():
  print('>>>>>>>>>>>>>/face/liveness', strftime("%Y-%m-%d %H:%M:%S", gmtime()), '\t\t\t', request.remote_addr)
  app.logger.info(request.remote_addr)

  file = request.files['image']

  image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
  file_name = uuid.uuid4().hex[:6]
  save_path = 'dump2/' + file_name + '.png'
  cv2.imwrite(save_path, image)

  bbox = np.zeros([4], dtype=np.int32)
  live_score = GetLiveness(image, image.shape[1], image.shape[0], bbox)

  if live_score == 1:
    result = "Genuine"
  elif live_score == -102:
    result = "Face not detected"
  elif live_score == -103:
    result = "Liveness failed"
  elif live_score == 0:
    result = "Spoof"
  elif live_score == -3:
    result = "Face is too small"
  elif live_score == -4:
    result = "Face is too large"
  else:
    result = "Error"
  status = "ok"

  response = jsonify({"status": status, "data": {"result": result, "box": {"x": int(bbox[0]), "y": int(bbox[1]), "w": int(bbox[2] - bbox[0] + 1), "h" : int(bbox[3] - bbox[1] + 1)}, "score": live_score}})

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/face/attribute', methods=['POST'])
def processAll():
  print('>>>>>>>>>>>>>/face/attribute', strftime("%Y-%m-%d %H:%M:%S", gmtime()), '\t\t\t', request.remote_addr)
  app.logger.info(request.remote_addr)

  file = request.files['image']

  image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
  file_name = uuid.uuid4().hex[:6]
  save_path = 'dump2/' + file_name + '.png'
  cv2.imwrite(save_path, image)

  bbox = np.zeros([4], dtype=np.int32)
  attribute = np.zeros([4], dtype=np.int32)
  angles = np.zeros([3], dtype=np.float)
  liveness = np.zeros([1], dtype=np.int32)
  age = np.zeros([1], dtype=np.int32)
  gender = np.zeros([1], dtype=np.int32)
  mask = np.zeros([1], dtype=np.int32)
  feature = np.zeros([4096], dtype=np.uint8)
  featureSize = np.zeros([1], dtype=np.int32)
  ret = ProcessAll(image, image.shape[1], image.shape[0], bbox, attribute, angles, liveness, age, gender, mask, feature, featureSize, 0)

  print("facebox: ", bbox[0], " ", bbox[1], " ", bbox[2], " ", bbox[3])
  print(f"wearGlasses: {attribute[0]}, leftEyeOpen: {attribute[1]}, rightEyeOpen: {attribute[2]}, mouthClose: {attribute[3]}")
  print(f"roll: {angles[0]} yaw: {angles[1]}, pitch: {angles[2]}")
  print(f"liveness: {liveness[0]}")
  print(f"age: {age[0]}")
  print(f"gender: {gender[0]}")
  print(f"mask: {mask[0]}")
  print(f"feature size: {featureSize[0]}")

  if ret == 0:
    result = "Face detected"
  elif ret == -1:
    result = "Engine not inited"
  elif ret == -2:
    result = "No face detected"
  else:
    result = "Error"
  status = "ok"

  response = jsonify({"status": status, "data": {"result": result, "box": {"x": int(bbox[0]), "y": int(bbox[1]), "w": int(bbox[2] - bbox[0] + 1), "h" : int(bbox[3] - bbox[1] + 1)},
                                                 "attr": {"wear_glasses": int(attribute[0]), "left_eye_open": int(attribute[1]), "right_eye_open": int(attribute[2]), "mouth_close": int(attribute[3])},
                                                 "angles": {"roll": float(angles[0]), "yaw": float(angles[1]), "pitch": float(angles[2])},
                                                 "liveness": int(liveness[0]),
                                                 "age": int(age[0]),
                                                 "gender": int(gender[0]),
                                                 "mask": int(mask[0])
                                                 }})

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/face/compare', methods=['POST'])
def compareFace():
  print('>>>>>>>>>>>>>/face/compare', strftime("%Y-%m-%d %H:%M:%S", gmtime()), '\t\t\t', request.remote_addr)
  app.logger.info(request.remote_addr)

  file1 = request.files['image1']
  image1 = cv2.imdecode(np.fromstring(file1.read(), np.uint8), cv2.IMREAD_COLOR)

  file2 = request.files['image2']
  image2 = cv2.imdecode(np.fromstring(file2.read(), np.uint8), cv2.IMREAD_COLOR)

  bbox1 = np.zeros([4], dtype=np.int32)
  attribute1 = np.zeros([4], dtype=np.int32)
  angles1 = np.zeros([3], dtype=np.float)
  liveness1 = np.zeros([1], dtype=np.int32)
  age1 = np.zeros([1], dtype=np.int32)
  gender1 = np.zeros([1], dtype=np.int32)
  mask1 = np.zeros([1], dtype=np.int32)
  feature1 = np.zeros([4096], dtype=np.uint8)
  featureSize1 = np.zeros([1], dtype=np.int32)
  ret = ProcessAll(image1, image1.shape[1], image1.shape[0], bbox1, attribute1, angles1, liveness1, age1, gender1, mask1, feature1, featureSize1, 0)

  print('image1 results>>>>>>>>')
  print("facebox: ", bbox1[0], " ", bbox1[1], " ", bbox1[2], " ", bbox1[3])
  print(f"wearGlasses: {attribute1[0]}, leftEyeOpen: {attribute1[1]}, rightEyeOpen: {attribute1[2]}, mouthClose: {attribute1[3]}")
  print(f"roll: {angles1[0]} yaw: {angles1[1]}, pitch: {angles1[2]}")
  print(f"liveness: {liveness1[0]}")
  print(f"age: {age1[0]}")
  print(f"gender: {gender1[0]}")
  print(f"mask: {mask1[0]}")
  print(f"feature size: {featureSize1[0]}")
  print("<<<<<<<<<<<<<<")

  if ret != 0:
    if ret == -1:
      result = "Engine not inited"
    elif ret == -2:
      result = "No face detected in image1"
    else:
      result = "Error in image1"

    response = jsonify({"status": status, "data": {"result": result}})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

  bbox2 = np.zeros([4], dtype=np.int32)
  attribute2 = np.zeros([4], dtype=np.int32)
  angles2 = np.zeros([3], dtype=np.float)
  liveness2 = np.zeros([1], dtype=np.int32)
  age2 = np.zeros([1], dtype=np.int32)
  gender2 = np.zeros([1], dtype=np.int32)
  mask2 = np.zeros([1], dtype=np.int32)
  feature2 = np.zeros([4096], dtype=np.uint8)
  featureSize2 = np.zeros([1], dtype=np.int32)
  ret = ProcessAll(image2, image2.shape[1], image2.shape[0], bbox2, attribute2, angles2, liveness2, age2, gender2, mask2, feature2, featureSize2, 1)

  print('image2 results>>>>>>>>')
  print("facebox: ", bbox2[0], " ", bbox2[1], " ", bbox2[2], " ", bbox2[3])
  print(f"wearGlasses: {attribute2[0]}, leftEyeOpen: {attribute2[1]}, rightEyeOpen: {attribute2[2]}, mouthClose: {attribute2[3]}")
  print(f"roll: {angles2[0]} yaw: {angles2[1]}, pitch: {angles2[2]}")
  print(f"liveness: {liveness2[0]}")
  print(f"age: {age2[0]}")
  print(f"gender: {gender2[0]}")
  print(f"mask: {mask2[0]}")
  print(f"feature size: {featureSize2[0]}")
  print("<<<<<<<<<<<<<<")

  if ret != 0:
    if ret == -1:
      result = "Engine not inited"
    elif ret == -2:
      result = "No face detected in image2"
    else:
      result = "Error in image2"

    response = jsonify({"status": status, "data": {"result": result}})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

  confidence = CompareFace(feature1, featureSize1[0], feature2, featureSize2[0])
  if confidence > 0.82:
    result = "Same"
  else:
    result = "Different"
  status = "ok"

  response = jsonify({"status": status, "data": {"result": result, "similarity": float(confidence)}})

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response


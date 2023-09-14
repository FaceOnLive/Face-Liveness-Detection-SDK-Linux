import sys
sys.path.append('.')

from flask import Flask, request, jsonify
from time import gmtime, strftime
import os
import base64
import json
import cv2
import numpy as np

from facewrapper.facewrapper import ttv_version
from facewrapper.facewrapper import ttv_get_hwid
from facewrapper.facewrapper import ttv_init
from facewrapper.facewrapper import ttv_init_offline
from facewrapper.facewrapper import ttv_detect_face

app = Flask(__name__) 

app.config['SITE'] = "http://0.0.0.0:8000/"
app.config['DEBUG'] = False

licenseKey = "XXXXX-XXXXX-XXXXX-XXXXX"
licensePath = "license.txt"
modelFolder = os.path.abspath(os.path.dirname(__file__)) + '/facewrapper/dict'

version = ttv_version()
print("version: ", version.decode('utf-8'))

ret = ttv_init(modelFolder.encode('utf-8'), licenseKey.encode('utf-8'))
if ret != 0:
    print(f"online init failed: {ret}");

    hwid = ttv_get_hwid()
    print("hwid: ", hwid.decode('utf-8'))

    ret = ttv_init_offline(modelFolder.encode('utf-8'), licensePath.encode('utf-8'))
    if ret != 0:
        print(f"offline init failed: {ret}")
        exit(-1)
    else:
        print(f"offline init ok")

else:
    print(f"online init ok")

@app.route('/api/liveness', methods=['POST'])
def check_liveness():
  file = request.files['image']
  image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
  
  faceRect = np.zeros([4], dtype=np.int32)
  livenessScore = np.zeros([1], dtype=np.double)
  angles = np.zeros([3], dtype=np.double)
  ret = ttv_detect_face(image, image.shape[1], image.shape[0], faceRect, livenessScore, angles)
  if ret == -1:
      result = "license error!"
  elif ret == -2:
      result = "init error!"
  elif ret == 0:
      result = "no face detected!"
  elif ret > 1:
      result = "multiple face detected!"
  elif faceRect[0] < 0 or faceRect[1] < 0 or faceRect[2] >= image.shape[1] or faceRect[2] >= image.shape[0]:
      result = "faace is in boundary!"
  elif livenessScore[0] > 0.5:
      result = "genuine"
  else:
      result = "spoof"
  
  status = "ok"
  response = jsonify({"status": status, "data": {"result": result, "face_rect": {"x": int(faceRect[0]), "y": int(faceRect[1]), "w": int(faceRect[2] - faceRect[0] + 1), "h" : int(faceRect[3] - faceRect[1] + 1)}, "liveness_score": livenessScore[0],
    "angles": {"yaw": angles[0], "roll": angles[1], "pitch": angles[2]}}})

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/api/liveness_base64', methods=['POST'])
def check_liveness_base64():
  content = request.get_json()
  imageBase64 = content['image']
  image = cv2.imdecode(np.frombuffer(base64.b64decode(imageBase64), dtype=np.uint8), cv2.IMREAD_COLOR)

  faceRect = np.zeros([4], dtype=np.int32)
  livenessScore = np.zeros([1], dtype=np.double)
  angles = np.zeros([3], dtype=np.double)
  ret = ttv_detect_face(image, image.shape[1], image.shape[0], faceRect, livenessScore, angles)
  if ret == -1:
      result = "license error!"
  elif ret == -2:
      result = "init error!"
  elif ret == 0:
      result = "no face detected!"
  elif ret > 1:
      result = "multiple face detected!"
  elif faceRect[0] < 0 or faceRect[1] < 0 or faceRect[2] >= image.shape[1] or faceRect[2] >= image.shape[0]:
      result = "faace is in boundary!"
  elif livenessScore[0] > 0.5:
      result = "genuine"
  else:
      result = "spoof"
  
  status = "ok"
  response = jsonify({"status": status, "data": {"result": result, "face_rect": {"x": int(faceRect[0]), "y": int(faceRect[1]), "w": int(faceRect[2] - faceRect[0] + 1), "h" : int(faceRect[3] - faceRect[1] + 1)}, "liveness_score": livenessScore[0],
    "angles": {"yaw": angles[0], "roll": angles[1], "pitch": angles[2]}}})

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

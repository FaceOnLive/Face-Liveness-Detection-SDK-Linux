import sys
sys.path.append('.')

from flask import Flask, render_template, request, jsonify, send_from_directory
from time import gmtime, strftime
import os
import base64
import json
import uuid
import cv2
import numpy as np

from ocrengine.ocrengine import TTVOcrGetHWID
from ocrengine.ocrengine import TTVOcrSetActivation
from ocrengine.ocrengine import TTVOcrInit
from ocrengine.ocrengine import TTVOcrProcess
from ocrengine.ocrengine import TTVOcrCreditCard
from ocrengine.ocrengine import TTVOcrBarCode
from ocrengine.ocrengine import ttv_if_checker

app = Flask(__name__)

ocrHWID = TTVOcrGetHWID()
licenseKey = os.environ.get("LICENSE_KEY")
ocrRet = TTVOcrSetActivation(licenseKey.encode('utf-8'))
print('ocr activation: ', ocrRet.decode('utf-8'))

dictPath = os.path.abspath(os.path.dirname(__file__)) + '/ocrengine/dict'
ocrRet = TTVOcrInit(dictPath.encode('utf-8'))
print('ocr engine init: ', ocrRet.decode('utf-8'))

@app.route('/ocr/idcard', methods=['POST'])
def ocr_idcard():
  file1 = request.files['image1']

  file_name1 = uuid.uuid4().hex[:6]
  save_path1 = '/tmp/' + file_name1 + '_' + file1.filename
  file1.save(save_path1)

  file_path1 = os.path.abspath(save_path1)

  if 'image2' not in request.files:
    file_path2 = ''
  else:
    file2 = request.files['image2']

    file_name2 = uuid.uuid4().hex[:6]
    save_path2 = '/tmp/' + file_name2 + '_' + file2.filename
    file2.save(save_path2)

    file_path2 = os.path.abspath(save_path2)


  ocrResult = TTVOcrProcess(file_path1.encode('utf-8'), file_path2.encode('utf-8'))
  status = "ok"
  if not ocrResult:
    ocrResDict = {}
    status = "error"
  else:
    ocrResDict = json.loads(ocrResult)  

  if_check = ttv_if_checker(file_path1.encode('utf-8'))
  response = jsonify({"status": status, "data": ocrResDict, "authenticity": if_check})

  os.remove(file_path1)
  if 'image2' in request.files:
    os.remove(file_path2)

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/ocr/idcard_base64', methods=['POST'])
def ocr_idcard_base64():
  content = request.get_json()
  imageBase64 = content['image']

  file_name = uuid.uuid4().hex[:6]
  save_path = '/tmp/' + file_name
  with open(save_path, "wb") as fh:
    fh.write(base64.b64decode(imageBase64))

  file_path = os.path.abspath(save_path)

  ocrResult = TTVOcrProcess(file_path.encode('utf-8'))
  status = "ok"
  if not ocrResult:
    ocrResDict = {}
    status = "error"
  else:
    ocrResDict = json.loads(ocrResult)  

  if_check = ttv_if_checker(file_path.encode('utf-8'))
  response = jsonify({"status": status, "data": ocrResDict, "authenticity": if_check})

  os.remove(file_path)

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response


@app.route('/ocr/credit', methods=['POST'])
def ocr_credit():
  file = request.files['image']
  print('ocr_credit ', file)

  image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
  file_name = uuid.uuid4().hex[:6]
  save_path = '/tmp/' + file_name + '.png'
  cv2.imwrite(save_path, image)

  file_path = os.path.abspath(save_path)

  ocrResult = TTVOcrCreditCard(file_path.encode('utf-8'))
  status = "ok"
  if not ocrResult:
    ocrResDict = {}
    status = "error"
  else:
    ocrResDict = json.loads(ocrResult)  

  response = jsonify({"status": status, "data": ocrResDict})

  os.remove(file_path)

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/ocr/credit_base64', methods=['POST'])
def ocr_credit_base64():
  print('ocr_credit_base64');
  content = request.get_json()
  imageBase64 = content['image']
  image = cv2.imdecode(np.frombuffer(base64.b64decode(imageBase64), dtype=np.uint8), cv2.IMREAD_COLOR)

  file_name = uuid.uuid4().hex[:6]
  save_path = '/tmp/' + file_name + '.png'
  cv2.imwrite(save_path, image)

  file_path = os.path.abspath(save_path)

  ocrResult = TTVOcrCreditCard(file_path.encode('utf-8'))
  status = "ok"
  if not ocrResult:
    ocrResDict = {}
    status = "error"
  else:
    ocrResDict = json.loads(ocrResult)

  response = jsonify({"status": status, "data": ocrResDict})

  os.remove(file_path)

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/ocr/barcode', methods=['POST'])
def ocr_barcode():
  file = request.files['image']
  print('ocr_barcode ', file)

  image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
  file_name = uuid.uuid4().hex[:6]
  save_path = '/tmp/' + file_name + '.png'
  cv2.imwrite(save_path, image)

  file_path = os.path.abspath(save_path)

  ocrResult = TTVOcrBarCode(file_path.encode('utf-8'))
  status = "ok"
  if not ocrResult:
    ocrResDict = {}
    status = "error"
  else:
    ocrResDict = json.loads(ocrResult)  

  response = jsonify({"status": status, "data": ocrResDict})

  os.remove(file_path)

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@app.route('/ocr/barcode_base64', methods=['POST'])
def ocr_barcode_base64():
  content = request.get_json()
  imageBase64 = content['image']
  image = cv2.imdecode(np.frombuffer(base64.b64decode(imageBase64), dtype=np.uint8), cv2.IMREAD_COLOR)

  file_name = uuid.uuid4().hex[:6]
  save_path = '/tmp/' + file_name + '.png'
  cv2.imwrite(save_path, image)

  file_path = os.path.abspath(save_path)
  print('file_path: ', file_path)

  ocrResult = TTVOcrBarCode(file_path.encode('utf-8'))
  status = "ok"
  if not ocrResult:
    ocrResDict = {}
    status = "error"
  else:
    ocrResDict = json.loads(ocrResult)

  response = jsonify({"status": status, "data": ocrResDict})

  os.remove(file_path)

  response.status_code = 200
  response.headers["Content-Type"] = "application/json; charset=utf-8"

  return response



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

import os
import sys
import numpy as np
import ctypes, ctypes.util
from enum import Enum
from ctypes import *
from numpy.ctypeslib import ndpointer

def print_log(fmt): print("[LOG] \033[98m{}\033[00m" .format(fmt))
def print_info(fmt): print("[INFO] \033[92m{}\033[00m" .format(fmt))
def print_error(fmt): print("[ERR] \033[91m{}\033[00m" .format(fmt)) 
def print_warning(fmt): print("[WARNING] \033[93m{}\033[00m" .format(fmt))

class ENGINE_CODE(Enum):
    E_NO_FACE = 0
    E_ACTIVATION_ERROR = -1
    E_ENGINE_INIT_ERROR = -2
    
class LIVENESS_CODE(Enum):
    L_TOO_SMALL_FACE = -100
    L_BORDERLINE_FACE = -200
    L_TOO_TURNED_FACE = -300
    L_COVERED_FACE = -400
    L_MULTIPLE_FACE = -500
    L_DEEP_FAKE = -600

lib_path = os.path.abspath(os.path.dirname(__file__)) + '/libliveness_v7.so'
lib = cdll.LoadLibrary(lib_path)

get_version = lib.ttv_version
get_version.argtypes = []
get_version.restype = ctypes.c_char_p

get_deviceid = lib.ttv_get_hwid
get_deviceid.argtypes = []
get_deviceid.restype = ctypes.c_char_p

init_sdk = lib.ttv_init
init_sdk.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
init_sdk.restype = ctypes.c_int32

init_sdk_offline = lib.ttv_init_offline
init_sdk_offline.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
init_sdk_offline.restype = ctypes.c_int32


detect_face_rgb = lib.ttv_detect_face
detect_face_rgb.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32, ctypes.c_int32, ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_double, flags='C_CONTIGUOUS')]
detect_face_rgb.restype = ctypes.c_int32

DEFAULT_THRESHOLD = 0
def check_liveness(image_mat, spoof_threshold = DEFAULT_THRESHOLD):
    result = ""
    score = 0

    if image_mat is None:
        result = "Failed to open image"
        return result, None, None, None
    
    face_rect = np.zeros([4], dtype=np.int32)
    liveness_score = np.zeros([1], dtype=np.double)
    angles = np.zeros([3], dtype=np.double)

    width = image_mat.shape[1]
    height = image_mat.shape[0]

    ret = detect_face_rgb(image_mat, width, height, face_rect, liveness_score, angles)

    if ret <= 0:
        if ret == ENGINE_CODE.E_ACTIVATION_ERROR.value:
            result = "ACTIVATION ERROR"
        elif ret == ENGINE_CODE.E_ENGINE_INIT_ERROR.value:
            result = "ENGINE INIT ERROR"
        elif ret == ENGINE_CODE.E_NO_FACE.value:
            result = "NO FACE"
        return result, None, None, None
    
    score = liveness_score[0]
    if score == LIVENESS_CODE.L_TOO_SMALL_FACE.value:
        result = "TOO SMALL FACE"
    elif score == LIVENESS_CODE.L_BORDERLINE_FACE.value:
        result = "FACE CUT OFF"
    elif score == LIVENESS_CODE.L_TOO_TURNED_FACE.value:
        result = "TOO TURNED FACE"
    elif score == LIVENESS_CODE.L_COVERED_FACE.value:
        result = "COVERED FACE"
    elif score == LIVENESS_CODE.L_MULTIPLE_FACE.value:
        result = "MULTIPLE FACES"
    elif score == LIVENESS_CODE.L_DEEP_FAKE.value:
        result = "DEEP FAKE DETECTED"
    elif score > spoof_threshold:
        result = "REAL"
    else:
        result = "SPOOF"

    return result, face_rect, score, angles

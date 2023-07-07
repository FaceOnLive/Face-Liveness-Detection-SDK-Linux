import ctypes, ctypes.util
from ctypes import *
from numpy.ctypeslib import ndpointer
import sys
import os
sys.path.append('/opt/intel/openvino_2022/runtime/lib/intel64')

lib_path = os.path.abspath(os.path.dirname(__file__)) + '/libs/libttvfaceengine7.so'
liveness_engine = cdll.LoadLibrary(lib_path)

ttv_version = liveness_engine.ttv_version
ttv_version.argtypes = []
ttv_version.restype = ctypes.c_char_p

ttv_get_hwid = liveness_engine.ttv_get_hwid
ttv_get_hwid.argtypes = []
ttv_get_hwid.restype = ctypes.c_char_p

ttv_init = liveness_engine.ttv_init
ttv_init.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ttv_init.restype = ctypes.c_int32

ttv_init_offline = liveness_engine.ttv_init_offline
ttv_init_offline.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ttv_init_offline.restype = ctypes.c_int32


ttv_detect_face = liveness_engine.ttv_detect_face
ttv_detect_face.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32, ctypes.c_int32, ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_double, flags='C_CONTIGUOUS')]
ttv_detect_face.restype = ctypes.c_int32


import ctypes, ctypes.util
from ctypes import *
from numpy.ctypeslib import ndpointer
import sys
import os

dll_path = os.path.abspath(os.path.dirname(__file__)) + '/libttvrecog.so'
face_engine = cdll.LoadLibrary(dll_path)

dll_path = os.path.abspath(os.path.dirname(__file__)) + '/libttvsdk.so'
face_engine = cdll.LoadLibrary(dll_path)

dll_path = os.path.abspath(os.path.dirname(__file__)) + '/libttvfaceengine.so'
face_engine = cdll.LoadLibrary(dll_path)

dll_path = os.path.abspath(os.path.dirname(__file__)) + '/libfacewrapper.so'
face_engine = cdll.LoadLibrary(dll_path)

InitEngine = face_engine.InitEngine
InitEngine.argtypes = [ctypes.c_char_p]
InitEngine.restype = ctypes.c_int32

GetLiveness = face_engine.GetLiveness
GetLiveness.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32, ctypes.c_int32, ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS')]
GetLiveness.restype = ctypes.c_int32

ProcessAll = face_engine.ProcessAll
ProcessAll.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32, ctypes.c_int32, ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ctypes.c_int32]
ProcessAll.restype = ctypes.c_int32

CompareFace = face_engine.CompareFace
CompareFace.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32, ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32]
CompareFace.restype = ctypes.c_double

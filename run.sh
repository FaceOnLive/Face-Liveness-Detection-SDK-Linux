#!/bin/sh

echo starting FaceOnLive Service
cd /root/FaceOnLive_face
/root/miniconda3/envs/py36/bin/python ./waitress_server.py

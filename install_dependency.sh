#!/bin/bash

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=15ilPQKc3SM0bEQHrJfovO97ejhftW7zr' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=15ilPQKc3SM0bEQHrJfovO97ejhftW7zr" -O openvino.tar.xz && rm -rf /tmp/cookies.txt

tar -xvxf openvino.tar.xz
sudo cp ./openvino/* /usr/lib -rf

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1td4iJU1O4NyIxAD5och_pyg6DfBKiR0V' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1td4iJU1O4NyIxAD5och_pyg6DfBKiR0V" -O dict.zip && rm -rf /tmp/cookies.txt

unzip dict.zip
mv ./dict ./facewrapper

lsb_result=$(lsb_release -a)

if [[ "$lsb_result" == *"Ubuntu 22.04"* ]]; then
  #echo "Current OS: Ubuntu 22.04"
  sudo cp ./facewrapper/libs/libimutils.so_for_ubuntu22 /usr/lib/libimutils.so
elif [[ "$lsb_result" == *"Ubuntu 20.04"* ]]; then
  #echo "Current OS: Ubuntu 20.04"
  sudo cp ./facewrapper/libs/libimutils.so /usr/lib
else
  echo "***No supported OS, Please try on Ubuntu 20.04 or later***"
  exit
fi

sudo apt-get update && sudo apt-get install -y python3-pip python3-opencv libcurl4-openssl-dev libssl-dev libtbb-dev

pip3 install -r requirements.txt
echo '*** Installed dependency, Please try python3 app.py ***'

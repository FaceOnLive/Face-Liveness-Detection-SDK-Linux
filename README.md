<div align="center">
  <a href="https://join.slack.com/t/faceonlive/shared_invite/zt-2drx19c5t-vQsR4TUGPD8oL7i7BXdKZA">Slack</a>
    ·
   <a href="https://www.faceonlive.com/">Website</a>
    ·
   <a href="https://portfolio.faceonlive.com">Portfolio</a>  
    ·
    <a href="https://www.huggingface.co/FaceOnLive">Hugging Face</a>
    ·
    <a href="https://getapi.faceonlive.com">Free APIs</a>
    ·
    <a href="https://github.com/FaceOnLive/OpenKYC">OpenKYC</a>  
    ·
    <a href="https://github.com/FaceOnLive/Mask-Face-Attendance-App-Flutter">Face Attendance</a>  
    ·
    <a href="mailto:contact@faceonlive.com">Contact</a>
</div>
<h1 align="center">Face Liveness Detection SDK For Linux</h1>
<p align="center">Fully Offline, On-Premise Face Liveness Detection SDK for Linux</p>

</br>
Documentation at https://docs.faceonlive.com
</br>

## :tada:  Try It Yourself on our [Portfolio Website](https://portfolio.faceonlive.com/#server_sdks/server/liv)

Integrated into [Huggingface Spaces 🤗](https://huggingface.co/spaces) using [Gradio](https://github.com/gradio-app/gradio). Try out the Web Demo: [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/FaceOnLive/Face-Liveness-Detection-SDK)


https://user-images.githubusercontent.com/91896009/187945910-4ca6d27c-d058-4749-a834-44914a5a957c.mp4


## :clap:  Supporters
[![Stargazers repo roster for @faceonlive/Face-Liveness-Detection-SDK-Linux](https://reporoster.com/stars/faceonlive/Face-Liveness-Detection-SDK-Linux)](https://github.com/faceonlive/Face-Liveness-Detection-SDK-Linux/stargazers)
[![Forkers repo roster for @faceonlive/Face-Liveness-Detection-SDK-Linux](https://reporoster.com/forks/faceonlive/Face-Liveness-Detection-SDK-Linux)](https://github.com/faceonlive/Face-Liveness-Detection-SDK-Linux/network/members)
<p align="center"><a href="https://github.com/nastyox/Rando.js#nastyox"><img src="http://randojs.com/images/barsSmallTransparentBackground.gif" alt="Animated footer bars" width="100%"/></a></p>

## 🏃  How to run
### 1. Download and install dependencies
To begin, follow these steps to download and install the necessary dependencies:
```
git clone https://github.com/FaceOnLive/Face-Liveness-Detection-SDK-Linux
cd Face-Liveness-Detection-SDK-Linux
chmod +x ./install_dependency.sh
sudo ./install_dependency.sh
```
### 2. Execute the Python Flask application
Next, run the Python Flask application by executing the following command:
```
python3 app.py
```
### 3. Activate the SDK
#### - Online License
If you have an online license, please update the license key provided by us in the following file:
https://github.com/FaceOnLive/Face-Liveness-Detection-SDK-Linux/blob/6e702fa01aeabbfb395d82c637a66dc18a93f2fb/app.py#L23-L23
#### - Offline License
If you have an offline license, please share your machine's HWID (Hardware ID) with us to receive the license.txt file. Update the HWID in the following file:
https://github.com/FaceOnLive/Face-Liveness-Detection-SDK-Linux/blob/6e702fa01aeabbfb395d82c637a66dc18a93f2fb/app.py#L24-L24
```
online init failed: 6
hwid:  IXwjedMe8M5cZX/GwU3NEOqJRcqLwldq27HSLyFiejbGDB9XVgytA1RgJukV3mWWTNo84NwTMYU=
```
### 4. Using Docker
- Build the Docker image:
```
sudo docker build --pull --rm -f Dockerfile -t faceonlive_v7:latest .
```
- Run Docker with online license:
```
sudo docker docker run --network host faceonlive_v7
```
- Run Docker with offline license:
```
sudo docker run -v license.txt:/root/FaceOnLive_v7/license.txt --network host faceonlive_v7
```
### 5. Test endpoint
To test the endpoint, download the Postman Collection from the following link:
[FaceOnLive.postman_collection.json](https://github.com/FaceOnLive/Face-Liveness-Detection-SDK-Linux/blob/main/FaceOnLive.postman_collection.json)

![image](https://github.com/FaceOnLive/Face-Liveness-Detection-SDK-Linux/assets/91896009/417e4fe3-9a01-43b3-a95b-d379ad4bdf17)

![image](https://github.com/FaceOnLive/Face-Liveness-Detection-SDK-Linux/assets/91896009/2275503e-49f0-4c72-9922-6e750a26dd62)


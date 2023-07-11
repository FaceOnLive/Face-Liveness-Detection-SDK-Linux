FROM ubuntu:20.04
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-opencv
RUN apt-get install -y libcurl4-openssl-dev libssl-dev
RUN mkdir -p /root/FaceOnLive_v7
RUN mkdir -p /root/FaceOnLive_v7/facewrapper
WORKDIR /root/FaceOnLive_v7
COPY ./facewrapper ./facewrapper
COPY ./facewrapper/libs/libimutils.so /usr/lib
COPY ./openvino /usr/lib
COPY ./app.py ./app.py
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "app.py"]
EXPOSE 8000

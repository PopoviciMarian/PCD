FROM alpine:3.7

#install python3

WORKDIR /usr/src/app
RUN apk add --no-cache python3 python3-dev g++

RUN pip3 install --upgrade pip

RUN pip3 install google-cloud-firestore
RUN pip3 install google-cloud-pubsub
RUN pip3 install google-cloud-storage

COPY . .

CMD ["python3", "./src/tester.py"]
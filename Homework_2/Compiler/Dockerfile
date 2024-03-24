FROM alpine:3.7

#install ++ and python3
RUN apk add --no-cache gcc musl-dev python3 python3-dev g++


WORKDIR /usr/src/app

RUN pip3 install --upgrade pip

RUN pip3 install google-cloud-firestore
RUN pip3 install google-cloud-pubsub
RUN pip3 install google-cloud-storage

COPY . .

CMD ["python3", "./src/compiler.py"]

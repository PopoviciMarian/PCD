
# Homenwork 1


## Usage (docker-compose)

```bash 
docker-compose up --build
```

## Parameters (.env file)

```bash
# Protocol
PROTOCOL=UDP # TCP or UDP
MECHANISM=STOP_AND_WAIT # STREAMING or STOP_AND_WAIT
CHUNK_SIZE=16384 # (bytes)
FILE_NAME=sample.txt
```


## Results without saving the file

<!-- 
TCP - STREAMING - 0.099s - Chunks sent: 12800  -  Chunks received: 22004 -209715200 bytes
TCP - STOP_AND_WAIT -0.60s - Chunks sent: 12800  -  Chunks received: 12800 -209715200 bytes

UDP - STREAMING - 1.930s - Chunks sent: 12800  -  Chunks received: 12798 -209715200 bytes - received: 209682432 bytes
UDP - STOP_AND_WAIT - 3.479s - Chunks sent: 12800  -  Chunks received: 12800 -209715200 bytes

Create a table with the results
--> 

| Protocol | Mechanism | Time | Chunks Sent | Chunks Received | Bytes Sent | Bytes Received |
|----------|-----------|------|-------------|-----------------|------------|----------------|
| TCP      | STREAMING | 0.099s | 12800 | 22004 | 209715200 | 209715200 |
| TCP      | STOP_AND_WAIT | 0.60s | 12800 | 12800 | 209715200 | 209715200 |
| UDP      | STREAMING | 1.930s | 12800 | 12798 | 209715200 | 209682432 |
| UDP      | STOP_AND_WAIT | 3.479s | 12800 | 12800 | 209715200 | 209715200 |


## Results saving the file

<!--
TCP - STREAMING - 1.516s - Chunks sent: 12800  -  Chunks received: 12800 -209715200 bytes 

TCP - STOP_AND_WAIT -  1.6569246s - Chunks sent: 12800  -  Chunks received: 12800 -209715200 bytes

UDP - STREAMING -3.478s - Chunks sent: 12800  -  Chunks received: 12708 -209715200 bytes - received: 208207872 bytes

UDP - STOP_AND_WAIT - 3.799s - Chunks sent: 12800  -  Chunks received: 12800 -209715200 bytes

Create a table with the results
-->

| Protocol | Mechanism | Time | Chunks Sent | Chunks Received | Bytes Sent | Bytes Received |
|----------|-----------|------|-------------|-----------------|------------|----------------|
| TCP      | STREAMING | 1.516s | 12800 | 12800 | 209715200 | 209715200 |
| TCP      | STOP_AND_WAIT | 1.656s | 12800 | 12800 | 209715200 | 209715200 |
| UDP      | STREAMING | 3.478s | 12800 | 12708 | 209715200 | 208207872 |
| UDP      | STOP_AND_WAIT | 3.799s | 12800 | 12800 | 209715200 | 209715200 |


 
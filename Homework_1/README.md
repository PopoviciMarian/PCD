
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


## Results without saving


| Protocol | Mechanism | Time | Chunks Sent | Chunks Received | Bytes Sent | Bytes Received |
|----------|-----------|------|-------------|-----------------|------------|----------------|
| TCP      | STREAMING | 0.099s | 12800 | 22004 | 209715200 | 209715200 |
| TCP      | STOP_AND_WAIT | 0.60s | 12800 | 12800 | 209715200 | 209715200 |
| UDP      | STREAMING | 1.930s | 12800 | 12798 | 209715200 | 209682432 |
| UDP      | STOP_AND_WAIT | 3.479s | 12800 | 12800 | 209715200 | 209715200 |


## Results saving the sent file (200 MB)

| Protocol | Mechanism | Time | Chunks Sent | Chunks Received | Bytes Sent | Bytes Received |
|----------|-----------|------|-------------|-----------------|------------|----------------|
| TCP      | STREAMING | 1.516s | 12800 | 12800 | 209715200 | 209715200 |
| TCP      | STOP_AND_WAIT | 1.656s | 12800 | 12800 | 209715200 | 209715200 |
| UDP      | STREAMING | 3.478s | 12800 | 12708 | 209715200 | 208207872 |
| UDP      | STOP_AND_WAIT | 3.799s | 12800 | 12800 | 209715200 | 209715200 |

## 500 MB

| Protocol | Mechanism | Time | Chunks Sent | Chunks Received | Bytes Sent | Bytes Received |
|----------|-----------|------|-------------|-----------------|------------|----------------|
| TCP      | STREAMING | 0.433s | 32000 | 32000 | 524288000 | 524288000 |
| TCP      | STOP_AND_WAIT | 1.374s | 32000 | 32000 | 524288000 | 524288000 |
| UDP      | STREAMING | 7.0790s | 32000 | 31996 | 524288000 | 524222464 |
| UDP      | STOP_AND_WAIT | 8.576s | 32000 | 32000 | 524288000 | 524288000 |



 
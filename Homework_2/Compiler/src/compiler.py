# This script is use to compile and deliver the binary of a C++ code
# Steps:
# 1. Receive a message from the subscriber containing the id of the code from firebase
# 2. Update the status of the code to "compiling" in the firebase
# 3. Write the code to a file named id.cpp
# 4. Compile the code using gpp
# 5. Save the output of the compilation (binaries) to Google Cloud Storage
# 6. Update the status of the code to "compiled" in the firebase
# 7. Publish a message to the topic "executor" containing the id of the code
# 8. Delete the folder containing the code
# 9. Acknowledge the message
# 10. Repeat

import os
import re 
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import logging
import constants
from google.cloud import firestore
import json
from google.cloud import storage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = constants.CERT_PATH
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
db = firestore.Client()
storage_client = storage.Client()
bucket = storage_client.bucket(constants.BUCKET_NAME)

def upload_blob(source_file_name: str, destination_blob_name: str) -> None:
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def publish_message(message: dict) -> None:
    message = json.dumps(message).encode('utf-8')
    future = publisher.publish(constants.EXECUTOR_TOPIC, data=message)
    future.result()
    logging.info(f"Published message to {constants.EXECUTOR_TOPIC} with message_id {future.result()}")

def update_status(id: str, status: str) -> None:
    doc_ref = db.collection(u'solutions').document(id)
    doc_ref.update({
        u'status': status
    })

def get_code(id: str) -> str:
    doc_ref = db.collection(u'solutions').document(id)
    doc = doc_ref.get()
    code = doc.to_dict()["code"]
    return code

def write_code_to_file(id: str, code: str) -> None:
    if not os.path.exists(os.path.join(".", "tmp")):
        os.makedirs(os.path.join(".", "tmp"))
    path = os.path.join(".", "tmp", f"{id}.cpp")
    with open(path, "w") as f:
        f.write(code)

def compile_code(id: str) -> bool:
    try:
        path = os.path.join(".", "tmp", f"{id}.cpp")
        #use gpp to compile the code
        r = os.system(f"g++ {path} -o {os.path.join('.', 'tmp', id)}")
        if r != 0:
            logging.error("Error compiling code")
            update_status(id, "error compiling")
            return False
        return True
    except Exception as e:
        logging.error(f"Error compiling code: {e}")
        update_status(id, "error")
        return  False

def delete_folder(id: str) -> None:
    os.remove(os.path.join(".", "tmp", f"{id}.cpp"))
    os.remove(os.path.join(".", "tmp", f"{id}"))

def callback(message) -> None:
    message_dict = json.loads(message.data.decode("utf-8"))
    id = message_dict["id"]
    logging.info(f"Received message with id {id}")
    try:
        update_status(id, "compiling")
        code = get_code(id)
        write_code_to_file(id, code)
        if not compile_code(id):
            update_status(id, "error compiling")
            message.ack()
            return
        upload_blob(os.path.join(".", "tmp", id), f"{id}")
        update_status(id, "compiled")
        publish_message({"id": id})
        delete_folder(id) 
    except Exception as e:
        logging.error(f"Error updating status: {e}")
        update_status(id, "error")

    message.ack()


 


def main():
    streaming_pull_future = subscriber.subscribe(constants.COMPILER_SUB, callback=callback, flow_control=pubsub_v1.types.FlowControl(max_messages=1))
    logging.info(f"Listening for messages on {constants.COMPILER_SUB}")
    with subscriber:
        try:

            streaming_pull_future.result()
        except KeyboardInterrupt:
            logging.info("Exiting")
            streaming_pull_future.cancel(await_msg_callbacks=False)
        except TimeoutError:
            streaming_pull_future.cancel()



if __name__ == "__main__":
    main()
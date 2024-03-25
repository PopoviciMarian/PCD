# This script is use to execute the binary of a C++ code and run the tests
# Steps:
# 1. Receive a message from the subscriber containing the id of the code from firebase
# 2. Update the status of the code to "executing" in the firebase
# 3. Download the binary from Google Cloud Storage
# 4. Get the tests from the firebase
# 5. Run the tests
# 6. Save the output of each test to firebase (Passed/Failed)
# 7. Update the status of the code to "executed" in the firebase
# 8. Publish a message to the topic "notifier" containing the id of the code (to notify the user)
# 9. Delete the binary
# 10. Acknowledge the message
# 11. Repeat



import os
import logging
import constants
import json
from google.cloud import pubsub_v1
from google.cloud import firestore
from google.cloud import storage
import subprocess
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = constants.CERT_PATH

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
db = firestore.Client()
storage_client = storage.Client()
bucket = storage_client.bucket(constants.BUCKET_NAME)

def download_blob(source_blob_name: str, destination_file_name: str) -> None:
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    os.chmod(destination_file_name, 0o777)

def update_status(id: str, status: str) -> None:
    doc_ref = db.collection(u'solutions').document(id)
    doc_ref.update({
        u'status': status
    })

def get_tests(id: str) -> list:
    doc_ref = db.collection(u'solutions').document(id)
    doc = doc_ref.get()
    problem_ref = doc.to_dict()["problem"]
    problem_doc = problem_ref.get()
    tests = problem_doc.to_dict()["tests"]
    #test are references
    tests = [{"test_id": test.id, "data": test.get().to_dict()} for test in tests]
    return tests

def delete_dir(path: str) -> None:
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))


def run_test(id: str, input: str, output: str, timeout: int) -> str:
    #status = Passed/Failed/Timeout
    result = {"status": "Failed", "output": ""}
    #create a file with the input called input.txt
    with open(os.path.join(".", "tmp", "input.txt"), "w") as f:
        f.write(input)
    logging.info(f"Running test with input {input} and expected output {output}")
    absolute_path = os.path.abspath(os.path.join(".", "tmp", id))
    logging.info(f"Running binary {absolute_path}")
    start = time.time()
    #run the binary with the input file
    process = subprocess.Popen((absolute_path), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        #wait for the process to finish
        process.wait(timeout=timeout)
        #get the output of the process
        if not os.path.exists(os.path.join(".", "output.txt")):
            result["status"] = "Output file not found"
        else:    
            with open(os.path.join(".", "output.txt"), "w") as f:
                result["output"] = f.read()
                logging.info(f"Output: {result['output']}")
            #compare the output with the expected output, trim the output to remove whitespaces
            if result["output"].strip() == output.strip():
                result["status"] = "Passed"
    except subprocess.TimeoutExpired:
        result["status"] = "Timeout"
    end = time.time()
    result["time"] = end - start
    return result



def save_result(solution_id: str, test_id: str, result: dict) -> None:
    doc_ref = db.collection(u'results').document()
    doc_ref.set({
        u'solution_id': db.collection(u'solutions').document(solution_id),
        u'test_id': db.collection(u'tests').document(test_id),
        u'time': result["time"],
        u'status': result["status"]
    })

    sol = db.collection(u'solutions').document(solution_id)
    sol.update({
        u'results': firestore.ArrayUnion([doc_ref])
    })

def run_tests(id: str, tests: list) -> None:
    for test in tests:
        test_id = test["test_id"]
        test_input = test["data"]["input"]
        test_output = test["data"]["output"]
        timeout = test["data"]["timeout"]
        logging.info(f"Running test {test_id} with input {test_input} and output {test_output} and timeout {timeout}")
        result = run_test(id, test_input, test_output, timeout)
        logging.info(f"Test {test_id} result: {result}")
        #save result to firebase

def callback(message) -> None:
    id = json.loads(message.data.decode('utf-8'))["id"]
    logging.info(f"Received message {id}")
    update_status(id, "executing")
    try:
        download_blob(f"{id}", os.path.join(".", "tmp", f"{id}"))
        tests = get_tests(id)
        for test in tests:
            test_id = test["test_id"]
            test_data = test["data"]
            logging.info(f"Running test {test_id} with input {test_data['input']} and output {test_data['output']}")
            result = run_test(id, test_data["input"], test_data["output"], test_data["timeout"])
            save_result(id, test_id, result)
        update_status(id, "executed")
    except Exception as e:
        logging.error(f"Error executing code: {e}")
        update_status(id, "error")
    message.ack()


def main():
    if not os.path.exists(os.path.join(".", "tmp")):
        os.makedirs(os.path.join(".", "tmp"))
    streaming_pull_future = subscriber.subscribe(constants.TESTER_SUB, callback=callback, flow_control=pubsub_v1.types.FlowControl(max_messages=1))
    logging.info(f"Listening for messages on {constants.TESTER_SUB}")
    with subscriber:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
        except TimeoutError:
            streaming_pull_future.cancel()
        


if __name__ == "__main__":
    main()
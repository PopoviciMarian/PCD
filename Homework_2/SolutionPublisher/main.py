# This is an Google Function.
# It is triggered when a new solution is added to the firebase.
# And is responsible adding the solution id in the compilation topic.

from cloudevents.http import CloudEvent
import functions_framework
from google.events.cloud import firestore
from google.cloud import pubsub_v1
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


publisher = pubsub_v1.PublisherClient()
TOPIC = "projects/tidal-reactor-418113/topics/compiler"


def publish_message(message: dict) -> None:
    message = json.dumps(message).encode('utf-8')
    future = publisher.publish(TOPIC, data=message)
    future.result()
    logging.info(f"Published message to {TOPIC} with message_id {future.result()}")

@functions_framework.cloud_event
def solution_publisher(cloud_event: CloudEvent) -> None:
    firestore_payload = firestore.DocumentEventData()
    firestore_payload._pb.ParseFromString(cloud_event.data)
    value = firestore_payload.value
    if value.name.split("/")[-2] != "solutions":
        return
    object_id = value.name.split("/")[-1]
    message = {"id": object_id}
    publish_message(message)
    logging.info(f"Published message to compiler topic with id {object_id}")

     




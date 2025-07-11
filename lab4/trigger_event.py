from azure.eventhub import EventHubProducerClient, EventData
import time
import json
import random
import uuid

CONNECTION_STR = 'Endpoint=sb://clickstream-namespace-xr.servicebus.windows.net/;'
EVENT_HUB_NAME = 'click-events'



producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)

def generate_sample_event():
    return {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2)
    }

def send_events(batch_size=10, delay=2):
    while True:
        event_data_batch = producer.create_batch()
        for _ in range(batch_size):
            data = generate_sample_event()
            event_data_batch.add(EventData(json.dumps(data)))
        producer.send_batch(event_data_batch)
        print(f"Sent {batch_size} events.")
        time.sleep(delay)

send_events()




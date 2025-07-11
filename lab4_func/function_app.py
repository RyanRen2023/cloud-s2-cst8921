import azure.functions as func
# import logging

# app = func.FunctionApp()

# @app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="click-events",
#                                connection="clickstreamnamespacexr_RootManageSharedAccessKey_EVENTHUB") 
# def eventhub_trigger(azeventhub: func.EventHubEvent):
#     logging.info('Python EventHub trigger processed an event: %s',
#                 azeventhub.get_body().decode('utf-8'))

import json, logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from uuid import uuid4

# ADLS connection string (use Key Vault in production)
BLOB_CONN_STR = "<your_storage_connection_string>"
CONTAINER = "click-events-raw"

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", 
                               event_hub_name="click-events",
                               connection="clickstreamnamespacexr_RootManageSharedAccessKey_EVENTHUB") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    try:
        # Decode and parse the event body as JSON
        body = json.loads(azeventhub.get_body().decode('utf-8'))

        # Generate a timestamp-based path and UUID-based file name
        ts = datetime.utcnow()
        blob_path = f"{ts.year}/{ts.month:02d}/{ts.day:02d}/{ts.hour:02d}/{ts.minute:02d}/{uuid4()}.json"

        # Initialize the Blob service client and get the target container
        blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
        container_client = blob_service.get_container_client(CONTAINER)

        # Upload the JSON data to Blob Storage
        container_client.upload_blob(blob_path, json.dumps(body), overwrite=False)

        # Log successful storage
        logging.info(f"✅ Stored event to blob: {blob_path}")
    except Exception as e:
        # Log any error that occurs during processing
        logging.error(f"❌ Error processing event: {e}")

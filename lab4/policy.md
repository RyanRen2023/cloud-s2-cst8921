
Endpoint=sb://clickstream-namespace-xr.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;



import azure.functions as func
import logging

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="click-events",
                               connection="clickstream-namespace-xr_RootManageSharedAccessKey_EVENTHUB") 
def eventhub_trigger1(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))




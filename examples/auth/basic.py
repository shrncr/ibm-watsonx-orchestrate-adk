from ibm_watsonx_orchestrate.client.credentials import Credentials
from ibm_watsonx_orchestrate.client.client import Client

# Set platform details.
# Note: wxo_instance_id pertains to the wxO tenant ID.
wxo_url = "https://dev-conn.watson-orchestrate.ibm.com"
wxo_api_key = "xxxxx"
wxo_instance_id = "20240527-1123-0088-305a-b311748cb470"


# Initialize wxo client.
credentials = Credentials(url=wxo_url, api_key=wxo_api_key, instance_id=wxo_instance_id)
client = Client(credentials=credentials)

# Get list of threads created.
print("Getting list of threads...")
threads = client.threads.list()
thread_id = threads[0].get('id') if len(threads) > 0 else None

if thread_id:
    print("Show list of messages in a thread")
    thread_messages = client.chat_messages.get_messages_in_thread(thread_id)
    print(thread_messages)


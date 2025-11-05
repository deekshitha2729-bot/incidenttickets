import pandas as pd
from elasticsearch import Elasticsearch, helpers

# --- CONNECT TO ELASTICSEARCH ---
client = Elasticsearch(
    hosts=["https://miniproject-a4b243.es.us-central1.gcp.elastic.cloud:443"],
    api_key="TmU2Y1Nwb0ItVFo4VmtZTFZtcHg6UnFnWTBVQ1B2NV9aYmtZTnFOTUhudw==",
    verify_certs=False  # This skips SSL check (okay for testing)
)

# Step 2: Set the index name
index_name = "incident_tickets"

# Step 3: Load the CSV file
df = pd.read_csv("dummy_incident_tickets.csv")


# --- CONVERT TO LIST OF DICTS ---
records = df.to_dict(orient="records")

# --- BULK INDEX INTO ELASTICSEARCH ---
actions = [
    {"_index": index_name, "_source": record}
    for record in records
]

helpers.bulk(client, actions)
print("Data indexed successfully!")

# --- VERIFY DATA ---
res = client.search(index=index_name, query={"match_all": {}}, size=5)
print("Sample indexed documents:")
for hit in res["hits"]["hits"]:
    print(hit["_source"])
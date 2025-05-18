import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
import plotly.express as px

# --- Settings ---
ES_HOST = "https://6a5dbb110e064dbf92b651d18e65f96c.us-east-1.aws.found.io"  # e.g., https://my-cluster.es.us-east-1.aws.found.io
ES_USERNAME = "nathan"
ES_PASSWORD = "mullet11"
INDEX_NAME = "testmoodleuserdata"  # TODO: Replace with actual index name

# --- Connect to Elasticsearch ---
es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    verify_certs=True
)

# --- Elasticsearch Query ---
query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"user_action": "enroll"}},
                {"exists": {"field": "course_id"}},
                {"exists": {"field": "user_name"}}
            ]
        }
    },
    "_source": ["course_id", "user_name"]
}

# --- Run the search ---
response = es.search(index=INDEX_NAME, body=query, size=1000)

# --- Parse results ---
hits = response['hits']['hits']
data = [
    {
        "course_id": hit['_source'].get("course_id", "unknown"),
        "user_name": hit['_source'].get("user_name", "unknown")
    }
    for hit in hits
]

df = pd.DataFrame(data)

# --- Display Multi-level Pie Chart ---
st.title("Enrollments by Course and User")

if not df.empty:
    fig = px.sunburst(
        df,
        path=['course_id', 'user_name'],
        values=None,  # Default: count of occurrences
        title="Multi-level Enrollment Breakdown"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found matching the query.")

import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
import plotly.express as px

# Streamlit title
st.title("Top 5 Usernames from Elasticsearch")

# Elastic credentials
cloud_id = "CCD_AF:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbzo0NDMkNmE1ZGJiMTEwZTA2NGRiZjkyYjY1MWQxOGU2NWY5NmMkY2VhMzU5YmJhY2NlNGY0YmFmMDBkYThkZmEzMmEyYzE="
api_key = "YjRwTjVaWUIyY1RBOEJfTlJIYVM6bXljWkdyT2JSM1MwMFZGUDdGMHlkZw=="
index_name = "moodle_mysql"

# Connect to Elasticsearch
es = Elasticsearch(
    cloud_id=cloud_id,
    api_key=api_key
)

# Query Elasticsearch: Get top 5 most frequent `username_custom`
query = {
    "size": 0,
    "aggs": {
        "top_usernames": {
            "terms": {
                "field": "username_custom.keyword",  # use `.keyword` for aggregations
                "size": 5
            }
        }
    }
}

# Execute the query
response = es.search(index=index_name, body=query)

# Extract data
buckets = response["aggregations"]["top_usernames"]["buckets"]
usernames = [bucket["key"] for bucket in buckets]
counts = [bucket["doc_count"] for bucket in buckets]

# Convert to DataFrame
df = pd.DataFrame({
    "Username": usernames,
    "Count": counts
})

# Display bar chart
fig = px.bar(df, x="Username", y="Count", title="Top 5 Most Common `username_custom` Values")
st.plotly_chart(fig)

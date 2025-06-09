import os
from elasticsearch8 import Elasticsearch

es_client = Elasticsearch(
    "https://6a5dbb110e064dbf92b651d18e65f96c.us-east-1.aws.found.io:443",
    api_key=os.environ["ES_API_KEY"]
)

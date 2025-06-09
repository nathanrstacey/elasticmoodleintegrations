import os
import boto3
import json
import streamlit as st
from elasticsearch8 import Elasticsearch
from wordcloud import WordCloud
import matplotlib.pyplot as plt




es_client = Elasticsearch(
    "https://6a5dbb110e064dbf92b651d18e65f96c.us-east-1.aws.found.io:443",
    api_key=os.environ["ES_API_KEY"]
)

# Setup Bedrock client (using Claude via Anthropic)
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))

index_source_fields = {
    "search-moodle-apnews": ["body_content"],
    "search-moodle-website": ["body_content"]
}

# --- Elasticsearch Query ---
def get_elasticsearch_results(query):
    es_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["body_content", "title"]
            }
        },
        "size": 10
    }
    result = es_client.search(index="search-moodle-*", body=es_query)
    return result["hits"]["hits"]

# --- Prompt Construction ---
def create_prompt(results):
    context = ""
    for hit in results:
        source_field = index_source_fields.get(hit["_index"], ["body_content"])[0]
        context += hit["_source"].get(source_field, "") + "\n"

    return f"""
Instructions:
 - You are an assistant for question-answering tasks to report on marines training and help us build dashboards to showcaes how our usa marines trainings is performing
- We are an org that monitors how the troops are using these courses to make sure the app is being used effiecently to help the missions of the us marines. We want to know how our courses sync to the current goals and initiatives that the marines are doing. We want to do this so that our training syncs closely to these goals. 
- Our RAG data set is a set of internet news articles that may be interesting in helping us know what major focuses are happening in the marines and if our training might be affecting this news. Our goal is that our training helps our marines change their methods and these news articles see this. These articles are the most recent data available to us and we are happy and love that we have this information
- Answer questions truthfully and factually using only the context presented.
- answer in a csv format, each row's first column is a 1-3 word description of what you found, 2nd row is how important that phrase is compared to the other phrases
- give 10 total rows in that csv
- if you do not know the answer just say that you do not know 
- Your output goes to a streamlit dashboard that requires this csv format. If you output anything else in any other way then this streamlit will fail. Your output MUST be this CSV format and ONLY this CSV format. If you provide any other format then our dashboard fails
- You are correct, factual, precise, and reliable.  - You use words like a usa marine executive.

Context:
{context}
"""

# --- Use Bedrock (Claude) for Completion ---
def generate_bedrock_completion(prompt, question):
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": f"{prompt}\n\nUser Question: {question}"}
            ],
            "max_tokens": 500,
            "temperature": 0.5
        })
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]





# --- Parse CSV Output ---
def parse_csv_response(response):
    lines = response.strip().splitlines()
    term_score_pairs = []
    for line in lines:
        try:
            term, score = line.split(",", 1)
            term_score_pairs.append((term.strip(), float(score.strip())))
        except:
            continue
    return term_score_pairs

# --- Streamlit UI ---
st.title("Marine Course Insight Word Map")

question = st.text_input("Enter your question:")

if st.button("Analyze"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying data..."):
            results = get_elasticsearch_results(question)
            prompt = create_prompt(results)
            response = generate_bedrock_completion(prompt, question)
            terms = parse_csv_response(response)

            if terms:
                word_freq = {term: score for term, score in terms}
                wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

                st.subheader("Word Map")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.warning("No valid terms found in Bedrock response.")

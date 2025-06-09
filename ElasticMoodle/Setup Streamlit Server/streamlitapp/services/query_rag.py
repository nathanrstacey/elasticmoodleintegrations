# services/query_rag.py

from services.elasticsearch_client import es_client
from services.bedrock_client import bedrock
import json

INDEX_SOURCES = {
    "search-moodle-training-website": ["body_content"],
    "search-moodle-apnews": ["body_content"],
    "search-moodle-website": ["body_content"]
}

def get_rag_context(query):
    context = ""
    for index in INDEX_SOURCES.keys():
        response = es_client.search(
            index=index,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": INDEX_SOURCES[index]
                    }
                },
                "size": 5
            }
        )
        for hit in response["hits"]["hits"]:
            field = INDEX_SOURCES[index][0]
            content = hit["_source"].get(field, "")
            context += content.strip() + "\n\n"
    return context

def ask_bedrock_question(context, question):
    prompt = f"""
- You are an assistant for question-answering tasks
- We are an org that monitors how the troops are using the app that manages training courses to make sure the missions of the us marines are met. 
- Sometimes questions will have to due with our org's role and other times it will be about any topic on earth
- You are supposed to answer questions no matter what RAG data was sent to you. Sometimes the RAG data will not be relevant to the question, but you still must answer the question.
- Our RAG data set is a set of internet news articles as well as our training website that has summaries and access to all of our trainings. That may be interesting in helping us know what major focuses are happening in the marines and if our training might be affecting this news. Our goal is that our training helps our marines change their methods and these news articles see this. These articles are the most recent data available to us and we are happy and love that we have this information
- Answer questions truthfully and factually
- Answer as if you are a professional military executive
- You are correct, factual, precise, and reliable. 

Context:
{context}
"""
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
            "temperature": 0.3
        })
    )
    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]

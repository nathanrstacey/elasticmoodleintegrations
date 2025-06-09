These are all of the items needed to fully instrument a Moodle Website with Elasticsearch/Kibana. This particular example is building a training website for marines. So many of the datasets are focused on this use-case
In this Github are items to do the following
1. Create a Moodle Website on Ubuntu
2. Improve the mysql connector in Kibana to join different mysql databases together and flatten the information. Most notably if a person or class is mentioned in any database row then all of hte information of that class/person are added to that row's representation in the Elastic doc of that row
3. Kibana Synthetic Examples of how to add an event in Moodle as well as check your class info. these are written in Playwright
4. Kibana Crawl websites that have information that help training leaders to know how to improve their training. This inludes grabbing ap news articles pertainant to the marines as well as a few sites focused on Marines
5. Create a Streamlit server and app which takes the above data from Elastic and connects it to a AWS Bedrock AI to create AI-centric graphs/charts/chatbot of the data.


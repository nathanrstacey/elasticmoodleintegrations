import streamlit as st
import streamlit.components.v1 as components

st.title("Kibana Lens Embedded in Streamlit")

kibana_url = "https://cea359bbacce4f4baf00da8dfa32a2c1.us-east-1.aws.found.io:9243/s/moodle/app/lens#/edit/345c3754-40dc-4aec-90df-b6b70d99dede?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-30d/d,to:now))"

# Optional: make height and width dynamic
iframe_code = f"""
<iframe src="{kibana_url}" width="100%" height="800" frameborder="0"></iframe>
"""

components.html(iframe_code, height=820)
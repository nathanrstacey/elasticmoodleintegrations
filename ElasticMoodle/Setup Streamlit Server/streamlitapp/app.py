import streamlit as st
from components.word_map import word_map_tab

st.set_page_config(page_title="Marines Moodle AI Dashboard", layout="wide")

st.title("Marines Moodle AI Dashboard")

st.markdown(
    """
    <div style='margin-top: 20px;'>
        <a href="https://cea359bbacce4f4baf00da8dfa32a2c1.us-east-1.aws.found.io:9243/s/moodle/app/dashboards#/view/4e7662b3-f936-40d7-800f-9ec3bf1e902c?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-15m,to:now))" target="_blank">
            <button style='font-size: 16px; padding: 8px 16px; background-color: #1f77b4; color: white; border: none; border-radius: 5px;'>Go to Kibana Moodle Main Page</button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Word Map", "Other Visualizations"])


with tab1:
    word_map_tab()

with tab2:
    st.write("Coming soon: Additional visualizations")



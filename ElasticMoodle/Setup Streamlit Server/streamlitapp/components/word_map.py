import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from services.query_utils import (
    get_elasticsearch_results, 
    create_prompt, 
    generate_bedrock_completion
)
from utils.parsing import parse_csv_response

# NEW: Import the new RAG utilities
from services.query_rag import get_rag_context, ask_bedrock_question


def word_map_tab():
    st.header("Marine Training Efficiency")

    question = st.text_input("Topic of training to assess:")

    if st.button("Analyze", key="analyze_word_map"):
        if not question:
            st.warning("Please enter a question.")
            return

        with st.spinner("Generating word maps..."):
            col1, col2, col3 , col4, col5 = st.columns([1, 0.05, 1 , 0.05, 1])  # Narrow spacer in middle

            # Column 1: AP News
            with col1:
                st.markdown("### 📰 Keywords from the News\n(What matters now)")

                # Use wildcard index and fields from both sources
                index_combined = "search-moodle-*"
                fields_combined = {
                    "search-moodle-apnews": ["body_content"],
                    "search-moodle-website": ["body_content"]
                }

                results_combined = get_elasticsearch_results(question, index_combined)
                prompt_combined = create_prompt(results_combined, fields_combined)
                response_combined = generate_bedrock_completion(prompt_combined, question)
                terms_combined = parse_csv_response(response_combined)

                if terms_combined:
                    word_freq_combined = {term: score for term, score in terms_combined}
                    wc_combined = WordCloud(width=600, height=300, background_color='white').generate_from_frequencies(word_freq_combined)
                    fig_combined, ax_combined = plt.subplots(figsize=(4.5, 2.5))
                    ax_combined.imshow(wc_combined, interpolation="bilinear")
                    ax_combined.axis("off")
                    st.pyplot(fig_combined)
                else:
                    st.warning("No valid terms from News.")


            # Column 2: Vertical separator
            with col2:
                st.markdown(
                   """
                    <style>
                    .vertical-line {
                        border-left: 1px solid #ccc;
                        height: 300px;
                        margin: auto;
                    }
                    </style>
                    <div class="vertical-line"></div>
                    """,
                    unsafe_allow_html=True
                )

            # Column 3: Training Site
            with col3:
                st.markdown("### 📘 Our Moodle Training\n(What we are currently training)")
                index_training = "search-moodle-training-website"
                fields_training = {index_training: ["body_content"]}

                results_train = get_elasticsearch_results(question, index_training)
                prompt_train = create_prompt(results_train, fields_training)
                response_train = generate_bedrock_completion(prompt_train, question)
                terms_train = parse_csv_response(response_train)

                if terms_train:
                    word_freq_train = {term: score for term, score in terms_train}
                    wc_train = WordCloud(width=600, height=300, background_color='white').generate_from_frequencies(word_freq_train)
                    fig_train, ax_train = plt.subplots(figsize=(4.5, 2.5))
                    ax_train.imshow(wc_train, interpolation="bilinear")
                    ax_train.axis("off")
                    st.pyplot(fig_train)
                else:
                    st.warning("No valid terms from Training index.")


            # Column 4: Vertical separator
            with col4:
                st.markdown(
                   """
                    <style>
                    .vertical-line {
                        border-left: 1px solid #ccc;
                        height: 300px;
                        margin: auto;
                    }
                    </style>
                    <div class="vertical-line"></div>
                    """,
                    unsafe_allow_html=True
                )

            # Add a fourth column 
            with col5:
                st.markdown("### 🌐 Internal Chats\n(Is our message sticking?)")
                index_website = "search-moodle-website"
                fields_website = {index_website: ["body_content"]}

                results_web = get_elasticsearch_results(question, index_website)
                prompt_web = create_prompt(results_web, fields_website)
                response_web = generate_bedrock_completion(prompt_web, question)
                terms_web = parse_csv_response(response_web)

                if terms_web:
                    word_freq_web = {term: score for term, score in terms_web}
                    wc_web = WordCloud(width=800, height=300, background_color='white').generate_from_frequencies(word_freq_web)
                    fig_web, ax_web = plt.subplots(figsize=(6.5, 3))
                    ax_web.imshow(wc_web, interpolation="bilinear")
                    ax_web.axis("off")
                    st.pyplot(fig_web)
                else:
                    st.warning("No valid terms from Website index.")


    st.markdown("---")
    st.subheader("🎯 Ask a Direct Question (RAG Search)")
    user_question = st.text_input("Ask a specific question about the training or its impact:")

    if st.button("Get Answer", key="rag_answer_button"):
        if not user_question:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Querying Elasticsearch and generating answer..."):
                rag_context = get_rag_context(user_question)
                rag_answer = ask_bedrock_question(rag_context, user_question)
                st.text_area("Answer from Bedrock:", rag_answer, height=200)

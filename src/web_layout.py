import streamlit as st


def create_layout():
    st.set_page_config(page_title="GenAI", page_icon="🤖")

    st.markdown(
        '<h1 style="text-align: center;">GenAI App To Retrieve information from SQL Database</h1>',
        unsafe_allow_html=True,
    )

    user_input = st.text_input(
        "Input: ",
        key="input",
        placeholder="Enter your question (do not include personal data)",
    )
    st.markdown(
        """
    <div style="color:red; font-weight:bold; text-align:center;">
    ⚠️ Note: This application is for informational purposes only. 
    Do not use generated recommendations as a substitute for professional medical advice.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        submit_clicked = st.button("Ask the Question")
        overwrite_db = st.button("Update Database")

    return user_input, submit_clicked, overwrite_db

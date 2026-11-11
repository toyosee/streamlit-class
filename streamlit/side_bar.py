import streamlit as st
# import pandas as pd

# details = {
#     "Name": ["John", "Jane", "Doe"],
#     "Age": [30, 25, 22],
#     "Weight": [4.4, 3.6, 3.9]
# }

# st.code(details["Name"])

# options = details["Name"]
# st.selectbox("Choose an option", options)
# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "List of best meals?", options
# )

# # Using "with" notation
# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )
import pandas as pd

uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "pdf"])
st.write(uploaded_file)
if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")
    structured = pd.read_csv(uploaded_file)
    st.dataframe(structured)
    st.write(structured["StockPrice"].value_counts())
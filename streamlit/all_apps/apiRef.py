import streamlit as st
import csv

# A streamlit form component and submit button that takes details and save as csv

st.title("API Reference Form")
with st.form("api_reference_form"):
    api_name = st.text_input("API Name")
    api_endpoint = st.text_input("API Endpoint")
    api_method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
    api_description = st.text_area("API Description")

    submitted = st.form_submit_button("Submit")
    if submitted:
        # Save the details to a CSV file
        with open("api_references.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([api_name, api_endpoint, api_method, api_description])
        st.success("API reference saved successfully!")
        
st.feedback("faces")

# camera should activste only by clicking not automatically when the page loads
button = st.button("Take a picture")
if button:
    imaging = st.camera_input("Take a picture")
    if imaging:
        st.image(imaging)
    # button to quit camera
    quit_button = st.button("Quit Camera")
    if quit_button:
        st.stop()
        
snow_flakes = st.button("Show Snowflakes")
if snow_flakes:
    st.snow()

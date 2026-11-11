import streamlit as st
import pandas as pd

st.title("Python Class")
st.divider()
# name = "Elijah"
# st.write(f"Hello, {name}!")

# st.badge("New")

# payment_details = {
#     "Names": ["Elijah", "John", "Jane"],
#     "Salary":[50000, 60000, 70000]
# }

# df = pd.DataFrame(payment_details)

# # st.dataframe(df)
# st.line_chart(df["Salary"])

# Buttons

prices = [100,250,300,400,500]
price = st.selectbox("Select a price", prices)

verify = st.checkbox("Are you sure?")

payment_button = st.button("Pay Now")

if payment_button and verify:
    st.success(f"Payment successful!, You paid {price} naira")
    if price == 500:
        st.balloons()
    # st.balloons()
    # st.snow()
elif payment_button and not verify:
    st.error("Please verify your payment details before proceeding.")
else:
    st.info("Please select a price and verify your payment details before proceeding.")
# Code With Toyo
# StreamLit App Demo
# pip install streamlit

import streamlit as st

st.title("Tolu Class")
# st.header("UI on the go")
# st.badge("Class 3")

# # Select box example
# food = ["Pizza", "Burger", "Pasta", "Salad"]
# option = st.selectbox("Select your favorite food", food)
# st.write(f"You selected: {option}")

# # Input field example
# name = st.text_input("Enter your name", placeholder="Elijah")
# st.write(f"Hello, {name}!")

# message = st.text_input("How Do You Feel")
# button = st.button("Renewd Hope")
# if button:
#     st.write(message.upper().split(" "))
#     st.balloons()
# # Exploring buttons
# if st.button("Click me"):
#     st.write("Good Morning and Welcome!")

st.divider()

# base = st.number_input("Enter Base")
# height = st.number_input("Enter Height")
# area = 0.5 * base * height
# button = st.button("Calculate")

# if button:
#     st.success(f"Area is {area} cm2")
    # st.balloons()
    # st.badge('pro')
#   st.code("I am here")

# Exploting Check boxes   
# st.checkbox("I agree to the terms and conditions")

# if st.checkbox("Subscribe to our newsletter"):
#     st.success("Thank you for subscribing!")

# info = st.checkbox("Are you ready to get started?")
# message = "Thank you for opting in Welcome to the team"
# role = "Member"

# if info:
#     st.success(message)
#     st.badge(role)

import time

plans = [500,1000,2000,3000]
roles = ["Member", "Financial Member", "Gold Member", "Oga PataPata"]

payment = st.selectbox("Choose a payment plan", plans)

role = None

if payment == 500:
    role = roles[0]
elif payment == 1000:
    role = roles[1]
elif payment == 2000:
    role = roles[2]
elif payment > 2000:
    role = roles[3]
    
agree = st.checkbox("Are you ready to get started?")
message = f"Payment of {payment} naira confirmed Welcome to the team"
button = st.button("Pay")

if button and agree:
    st.success(message)
    st.badge(role)
    if payment == 2000:
        st.snow()
    elif payment > 2000:
        st.snow()
        time.sleep(3)
        st.balloons()
elif button and not agree:
    st.warning("Please agree to the terms and conditions to proceed with payment.")
else:
    st.info("Please select a payment plan and agree to the terms and conditions to proceed.")

# 30/4/2026

# st.latex()
# st.latex(r'''
#     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
#     \sum_{k=0}^{n-1} ar^k =
#     a \left(\frac{1-r^{n}}{1-r}\right)
#     ''')

# speed_of_light = "E = mc^2"
# st.latex(speed_of_light)
# st.latex("\int e^x dx = e^x + C")

# Exploring Sliders
# st.slider("Select a number", 0, 100, 50)
# number = st.slider("Select a number", 0, 100, 20)
# st.write(f"You selected: {number}")

# import pandas as pd
# import streamlit as st
# from numpy.random import default_rng as rng

# df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

# st.line_chart(df)

# Exploring file uploader
# st.file_uploader("Upload a file", 
#                  accept_multiple_files=True, 
#                  type=["csv", "txt", "xlsx"]
#                  )

# uploaded_file = st.file_uploader("Upload a file")
# # st.write(uploaded_file)
# if uploaded_file is not None:
#     st.success("File uploaded successfully!")
#     st.write(f"Filename: {uploaded_file.name}")
#     st.info(f"File type: {uploaded_file.type}")

## Exploring Color Picker  
# st.color_picker("Pick a color")
# color = st.color_picker("Pick a color")
# st.write(f"You selected: {color}")


# Exploring Date and Time Input
# st.date_input("Select a date")
# date = st.date_input("Select a date")
# st.write(f"You selected: {date}")

# Time input example
# st.time_input("Select a time")

# time = st.time_input("Select a time")
# # Access the .hour attribute for comparison

# if time.hour < 12:
#     st.info(f"You selected: {time}")
#     st.badge("Good Morning!", color="grey")
# elif 12 <= time.hour < 18:
#     st.info(f"You selected: {time}")
#     st.badge("Good Afternoon!", color="gray")
# else:
#     st.info(f"You selected: {time}")
#     st.badge("Good Evening!")


# # Streamlit app to calculate the area of a circle
# import math
# st.title("Circle Area Calculator")
# radius = st.number_input("Enter the radius of the circle", min_value=0.0)
# if st.button("Calculate Area"):
#     area = math.pi * radius ** 2
#     st.write(f"The area of the circle with radius {radius} is: {area:.2f}")


# camera should activste only by clicking not automatically when the page loads
# button = st.button("Take a picture")
# if button:
#     imaging = st.camera_input("Take a picture")
#     if imaging:
#         st.image(imaging)
#     # button to quit camera
#     quit_button = st.button("Quit Camera")
#     if quit_button:
#         st.stop()


# imaging = st.camera_input("Take a picture")
# if imaging:
#     st.image(imaging)
        
# snow_flakes = st.button("Show Snowflakes")
# if snow_flakes:
#     st.snow()


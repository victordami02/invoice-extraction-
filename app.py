from dotenv import load_dotenv

load_dotenv() # loads all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Sgemini pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text
# function to convert the uploaded image to bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    


# initialize st setup
st.set_page_config(page_title="Multi Language Invoice Extractor")

st.header("Invoice extractor")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button('tell me about the invioce')    

input_prompt= """
you are an expert in understanding invoices. we will upload an image as invoice and you will have to answer any questions based on the uploaded invoice image
"""

# if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    responce = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The responce is")
    st.write(responce)


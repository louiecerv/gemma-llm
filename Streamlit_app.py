import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import streamlit as st
import streamlit as st 
import cv2

generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.9,
    "top_p": 1,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

def app():
    image = cv2.imread('wvsu_logo.png')
    resized_image = cv2.resize(image, (120, 120))
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    vertexai.init(project="learn-vertex-ai-417510", location="asia-southeast1")
    model = GenerativeModel(
    #"gemini-1.0-pro-001",
    "gemini-1.5-pro-preview-0409",
    )


    chat = model.start_chat()

    # Initialize chat history
    chat_history = []

    # Create two columns
    col1, col2 = st.columns([1, 4])

    # Display the image in the left column
    with col1:
        st.image(resized_image)  # Adjust image size to fit column

    # Display the title in the right column
    with col2:
        st.title("A Teaching Co-pilot based on Google Gemini")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University"""
    st.text(text)

    # Text input for user message
    user_input = st.text_area("Your prompt:")

    # Button to submit message
    if st.button("Get Response"):
        # Add user message to chat history
        chat_history.append({"speaker": "User", "message": user_input})

        # Generate response from Gemma
        bot_response = chat.send_message(user_input,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        # Access the content section within the candidates dictionary
        bot_response = bot_response.text

        # Add bot response to chat history
        chat_history.append({"speaker": "Gemini", "message": bot_response})

        # Display chat history
        for message in chat_history:
            st.write(f"{message['speaker']}: {message['message']}")

#run the app
if __name__ == "__main__":
  app()

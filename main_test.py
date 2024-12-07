import streamlit as st
import time
import random  # To generate random query parameters
import requests
import json

from pipeline import full_pipeline

# Generator to fetch and yield chunks from a POST request response
def get_response_chunks(url, payload, headers, chunk_size=1024):
    """
    Generator to fetch and yield chunks from a POST request response.
    Args:
        url (str): The API endpoint.
        payload (dict): The JSON payload for the POST request.
        headers (dict): The headers to include in the request.
        chunk_size (int): The size of each chunk (in bytes) to read.
    
    Yields:
        dict: A parsed JSON chunk from the response.
    """
    # Send the POST request with streaming enabled
    response = requests.post(url, json=payload, headers=headers, stream=True)
    
    if response.status_code == 200:
        # Iterate over the response in chunks
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:  # Only process non-empty chunks
                try:
                    # Parse and yield the parsed chunk as a dictionary
                    parsed_chunk = json.loads(chunk.decode('utf-8'))
                    # parsed_chunk = parsed_chunk.get("message", {}).get("content", "")
                    yield parsed_chunk.get("message", {}).get("content", "")
                except json.JSONDecodeError:
                    print("Error decoding chunk")
                    continue
    else:
        print(f"Failed to get a valid response. Status code: {response.status_code}")
        print(response.text)

# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("[200 OK Team] Nornickel Hackathon Multi-Model RAG with Colpali")

# File uploader in the sidebar
with st.sidebar:
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Choose a PDF file", accept_multiple_files=True
    )

    new_set = set()
    for f in uploaded_files:
        new_set.add(f.file_id)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message:
            st.markdown(message["content"])  # Display the text part
            st.image(message["image"], caption=message.get("caption", ""))
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    random_query = random.randint(1, 10000)  # Random number to ensure a unique image URL
    img = f"https://cataas.com/cat?{random_query}"


    # Assistant response simulation
    with st.chat_message("assistant"):
        
        
        oollama_response_generator, pages_images_base64 = full_pipeline(prompt)

        for base64_image in pages_images_base64:
            image_url = f"data:image/jpeg;base64,{base64_image}"
            st.image(image_url)
      
        response = st.write_stream(oollama_response_generator)  


        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "image": 'test_img2.jpg',  # Example image URL (replace with actual image URL)
            "caption": "Результат поиска"
        })

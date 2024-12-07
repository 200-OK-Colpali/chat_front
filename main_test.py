import streamlit as st
import time
import random  # To generate random query parameters
import requests
import json

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

    # Assistant response simulation
    with st.chat_message("assistant"):
        response = "Поиск в процессе..."
        st.markdown(response)
        time.sleep(1)

        # URL for the Ollama API (or your specific model endpoint)
        url = "http://localhost:11434/api/chat"

        # Prepare payload with user input dynamically
        payload = {
            "model": "llama3.2-vision",  # Replace with the model name you want to use (e.g., Ollama)
            "messages": [
                {
                    "role": "user",
                    "content": prompt,  # Use the user input as the content
                    "images": [open('test_base64.txt').read()]  # Assuming this is the image data, adjust as needed
                }
            ]
        }

        # Headers to indicate we're sending JSON data
        headers = {
            "Content-Type": "application/json"
        }

        # Use the generator to get chunks from the response
        # response_text = ""
        # for parsed_chunk in get_response_chunks(url, payload, headers):
        #     message_content = parsed_chunk.get("message", {}).get("content", "")
        #     if message_content:
        #         response_text += message_content  # Append chunk content incrementally
        response = st.write_stream(get_response_chunks(url, payload, headers))  # Update the chat message with the content so far
                # time.sleep(0.5)  # Simulate typing delay for a more natural experience

        # Save the assistant's response to session state

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "image": "https://cataas.com/cat?random",  # Example image URL (replace with actual image URL)
            "caption": "Результат поиска"
        })

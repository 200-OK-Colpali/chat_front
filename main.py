import streamlit as st
import os
import random  # To generate random query parameters
import requests
import json
from pipeline import full_pipeline, RAG_with_index
import shutil
import tempfile
from PIL import Image
import subprocess
from os import listdir
from os.path import isfile, join

# Ensure ./docs folder exists
os.makedirs("./docs", exist_ok=True)


saved_filenames = set()
doc_ids_to_file_names_copy = RAG_with_index.get_doc_ids_to_file_names()
for key in doc_ids_to_file_names_copy:
    filename = doc_ids_to_file_names_copy[key]
    filename = filename.split("/")[-1]
    saved_filenames.add(filename)


# Utility functions for file conversion
def convert_to_pdf(input_path, original_filename, output_dir="./docs"):
    """
    Converts a file to PDF using appropriate methods based on file type.

    Args:
        input_path (str): Path to the input file.
        output_dir (str): Directory to save the converted PDF.

    Returns:
        str: Path to the converted PDF or None if conversion fails.
    """
    file_extension = os.path.splitext(input_path)[1].lower()
    output_path = os.path.join(
        output_dir, os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
    )

    original_filename = original_filename.split(".")
    original_filename = original_filename[0] + ".pdf"

    # try:
    if file_extension in [".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"]:
        if not shutil.which("libreoffice"):
            raise EnvironmentError("LibreOffice is not installed or not in PATH.")
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                input_path,
                "--outdir",
                output_dir,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        save_dir = output_dir + "/" + input_path.split("/")[-1]

        save_dir = save_dir.split(".")
        save_dir = "./" + save_dir[1] + ".pdf"
        new_name = output_dir + "/" + original_filename
        os.rename(save_dir, new_name)
        output_path = new_name

    elif file_extension in [".jpg", ".jpeg", ".png"]:
        image = Image.open(input_path)

        output_path = output_path.split("/")
        output_path[-1] = original_filename
        output_path = "/".join(output_path)


        image.save(output_path, "PDF")
        # os.rename(input_path, output_path)
        
    elif file_extension == ".pdf":

        output_path = output_path.split("/")
        output_path[-1] = original_filename
        output_path = "/".join(output_path)

        shutil.copy(input_path, output_path)
    else:
        return None
    return output_path if os.path.exists(output_path) else None



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
                    parsed_chunk = json.loads(chunk.decode("utf-8"))
                    # parsed_chunk = parsed_chunk.get("message", {}).get("content", "")
                    yield parsed_chunk.get("message", {}).get("content", "")
                except json.JSONDecodeError:
                    print("Error decoding chunk")
                    continue
    else:
        print(f"Failed to get a valid response. Status code: {response.status_code}")


# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("[200 OK Team] Nornickel Hackathon Multi-Model RAG with Colpali")

# File uploader in the sidebar
with st.sidebar:
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Upload Word, Excel, PowerPoint, Image, or PDF files",
        accept_multiple_files=True,
    )

    # Process uploaded files
    if uploaded_files:
        st.write("**Processing Files...**")
        for uploaded_file in uploaded_files:

            mypath = "./docs"
            onlyfiles_docs = [f for f in listdir(mypath) if isfile(join(mypath, f))]

            mypath = "./test_dataset"
            onlyfiles_test_dataset = [
                f for f in listdir(mypath) if isfile(join(mypath, f))
            ]

            onlyfiles_docs.extend(onlyfiles_test_dataset)

            if uploaded_file.name in saved_filenames:
                st.sidebar.success(f"File already in index: {uploaded_file.name} ")

                continue

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

            try:
                converted_file = convert_to_pdf(temp_path, uploaded_file.name)


                converted_file_name = converted_file.split('/')[-1]
                if converted_file_name in saved_filenames:
                    st.sidebar.success(f"File already in index: {converted_file} ")

                    continue
                
                st.sidebar.success(
                    f"Saved: {os.path.basename(converted_file)} to ./docs"
                )

            except Exception as e:
                st.sidebar.error(f"Failed to process: {uploaded_file.name} , {e}")

            RAG_with_index.add_to_index(
                input_item=converted_file, store_collection_with_index=False
            )
            st.sidebar.success(f"Indexed: {os.path.basename(converted_file)} ")


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

    random_query = random.randint(
        1, 10000
    )  # Random number to ensure a unique image URL
    img = f"https://cataas.com/cat?{random_query}"

    # Assistant response simulation
    with st.chat_message("assistant"):

        oollama_response_generator, pages_images_base64, doc_path, page_num = full_pipeline(prompt)

        for base64_image in pages_images_base64:
            image_url = f"data:image/jpeg;base64,{base64_image}"
            st.image(image_url)

        response = st.write_stream(oollama_response_generator)

        doc_name = doc_path.split('/')[-1]

        st.write(f"Информация из документа {doc_name} на странице {page_num}")
        # st.session_state.messages.append({
        #     "role": "assistant",
        #     "content": response,
        #     "image": 'test_img2.jpg',  # Example image URL (replace with actual image URL)
        #     "caption": "Результат поиска"
        # })

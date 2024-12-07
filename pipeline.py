import base64
import torch
import json
import requests

import os
from byaldi import RAGMultiModalModel
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from io import BytesIO
from PIL import Image  # Pillow library for image handling

from pdf2image import convert_from_path
from io import BytesIO


RAG_with_index = RAGMultiModalModel.from_index(
    index_path="./global_index",  # Путь к папке с индексом
    verbose=1,
    device="cuda",  # Укажите устройство, например "cuda" или "cpu"
)
doc_ids_to_file_names = RAG_with_index.get_doc_ids_to_file_names()


def query_index(query_text: str):
    results = RAG_with_index.search(query_text, k=1)

    parsed_results = []
    for result in results:
        parsed_results.append(
            {
                "doc_id": result.doc_id,
                "doc_path": doc_ids_to_file_names[result.doc_id],
                "page_num": result.page_num,
            }
        )

    return parsed_results


def get_page_image_base64(pdf_path: str, page_number: int):
    dpi = 300
    image_format = "JPEG"

    # Step 1: Extract the specific page into a temporary PDF
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Ensure the page number is valid
    if page_number < 1 or page_number > len(reader.pages):
        raise ValueError("Page number out of range!")

    # Add the page to a new PDF
    writer.add_page(reader.pages[page_number - 1])

    # Save the temporary PDF to memory
    temp_pdf_bytes = BytesIO()
    writer.write(temp_pdf_bytes)
    temp_pdf_bytes.seek(0)

    # Step 2: Convert the temporary PDF bytes to an image
    images = convert_from_bytes(temp_pdf_bytes.getvalue(), dpi=dpi)
    image_bytes = BytesIO()

    # Convert the first (and only) page image to bytes
    images[0].save(image_bytes, format=image_format)
    image_bytes.seek(0)

    # Step 3: Encode image bytes into base64
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

    return image_base64


def get_pages_images_base64_from_pages_by_query(pages_by_query: list):
    pages_images_bytes = []

    for page_data in pages_by_query:
        doc_path = page_data.get("doc_path")
        page_num = page_data.get("page_num")

        image_bytes = get_page_image_base64(doc_path, page_num)
        pages_images_bytes.append(image_bytes)

    return pages_images_bytes


def generate_oollama_response_generator(images_base64: list, query_text: str):
    def get_response_chunks(url, payload, headers, chunk_size=1024):

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
            print(
                f"Failed to get a valid response. Status code: {response.status_code}"
            )
            print(response.text)

    url = "http://87.236.31.60:3000/api/chat"

    # Prepare payload with user input dynamically
    payload = {
        "model": "llama3.2-vision",  # Replace with the model name you want to use (e.g., Ollama)
        "messages": [
            {
                "role": "user",
                "content": query_text,  # Use the user input as the content
                "images": images_base64,  # Assuming this is the image data, adjust as needed
            }
        ],
    }

    # Headers to indicate we're sending JSON data
    headers = {"Content-Type": "application/json"}

    return get_response_chunks(url, payload, headers)


def full_pipeline(query_text: str):
    pages_by_query = query_index(query_text)

    pages_images_base64 = get_pages_images_base64_from_pages_by_query(pages_by_query)

    oollama_response_generator = generate_oollama_response_generator(
        images_base64=pages_images_base64, query_text=query_text
    )

    return oollama_response_generator, pages_images_base64


# oollama_response_generator, pages_images_base64 = full_pipeline("как дела у нлмк?")

# for text in oollama_response_generator:
#     print(text, end='')

import base64
import torch

import os 
from byaldi import RAGMultiModalModel
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from io import BytesIO
from PIL import Image  # Pillow library for image handling

import ollama



from pdf2image import convert_from_path
from io import BytesIO




RAG_with_index = RAGMultiModalModel.from_index(
    index_path="./global_index",  # Путь к папке с индексом
    verbose=1,
    device="cuda"  # Укажите устройство, например "cuda" или "cpu"
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
    

def get_page_image_bytes(pdf_path: str, page_number: int):
    dpi=300
    image_format="JPEG"
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

    return image_bytes.getvalue()

def get_pages_images_bytes_from_pages_by_query(pages_by_query: list):
    pages_images_bytes = []

    for page_data in pages_by_query:
        doc_path = page_data.get("doc_path")
        page_num = page_data.get("page_num")

        image_bytes = get_page_image_bytes(doc_path, page_num)
        pages_images_bytes.append(image_bytes)

    return pages_images_bytes


def generate_oollama_response(images_bytes: list, query_text: str):
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': f'{query_text}',
            'images': images_bytes
        }]
        )

    return response


def full_pipeline(query_text: str):
    pages_by_query = query_index(query_text)
    
    pages_images_bytes = get_pages_images_bytes_from_pages_by_query(pages_by_query)
    
    oollama_response = generate_oollama_response(images_bytes=pages_images_bytes, query_text=query_text)
    
    return oollama_response


res = full_pipeline("Какая выручка за 2016 год у ММК?")
print(res)


import ollama


from pdf2image import convert_from_path
from io import BytesIO


def pdf_to_images_as_bytes(pdf_path, dpi=300, image_format="JPEG"):
    # Convert PDF to a list of PIL.Image objects
    images = convert_from_path(pdf_path, dpi=dpi)
    images_as_bytes = []

    for i, image in enumerate(images):
        # Create a BytesIO object to hold the image bytes
        image_bytes = BytesIO()
        # Save the image into the BytesIO object
        image.save(image_bytes, format=image_format)
        images_as_bytes.append(image_bytes.getvalue())

        print(f"Page {i + 1} converted to bytes.")

    return images_as_bytes


        
        
        
# Example usage
pdf_path = "extracted_page.pdf"          # Replace with your PDF file
output_folder = "."  # Replace with your output folder
images_bytes = (pdf_to_images_as_bytes(pdf_path))




response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'Перескажи первые 2 предложения в 20 словах.',
        'images': images_bytes
    }]
)

print(response.message.content)

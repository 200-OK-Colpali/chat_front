from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from io import BytesIO
from PIL import Image  # Pillow library for image handling



def extract_page_and_convert_to_image_bytes(pdf_path, page_number, dpi=300, image_format="JPEG"):
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

# Example usage
pdf_path = "docs/attention_is_all_you_need.pdf"  # Replace with your PDF file
page_number = 2  # Replace with the page number you want to extract

# try:

output_image_path = "extracted_page.jpg"  # Path to save the image

def save_image_from_bytes(image_bytes, output_path):
    # Load the bytes into a PIL image
    image = Image.open(BytesIO(image_bytes))
    # Save the image to the specified path
    image.save(output_path)
    print(f"Image saved at {output_path}")


image_bytes = extract_page_and_convert_to_image_bytes(pdf_path, page_number)
# print(f"Extracted page {page_number} as image bytes (first 100 bytes): {image_bytes[:100]}...")
save_image_from_bytes(image_bytes, output_image_path)

# except Exception as e:
#     print(f"Error: {e}")

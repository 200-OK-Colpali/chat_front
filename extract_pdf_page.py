from PyPDF2 import PdfReader, PdfWriter

def extract_page(input_pdf, output_pdf, page_number):
    reader = PdfReader(input_pdf)

    if page_number < 1 or page_number > len(reader.pages):
        print("Page number out of range!")
        return

    # Add the specific page to a new PDF
    writer.add_page(reader.pages[page_number - 1])

    # Write the new PDF to the output file
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Page {page_number} extracted to {output_pdf}!")

# Example usage
input_pdf_path = "docs/attention_is_all_you_need.pdf"  # Replace with your PDF file
output_pdf_path = "extracted_page.pdf"
page_to_extract = 2  # Replace with the page number you want to extract
extract_page(input_pdf_path, output_pdf_path, page_to_extract)

import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder='Non_Profit_images'):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    images_list = []

    # Iterate over each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Render the page as an image (pixmap)
        pix = page.get_pixmap()
        
        # Define the output image file name
        image_file_name = os.path.join(output_folder, f"page_{page_num + 1}.png")
        
        # Save the image to disk
        pix.save(image_file_name)
        
        # Append the image file name to the list
        images_list.append(image_file_name)

        # Log progress every 10 pages
        if (page_num + 1) % 10 == 0:
            print(f"Processed {page_num + 1} pages...")

    pdf_document.close()
    print(f"Total images extracted: {len(images_list)}")
    return images_list

# Example usage
pdf_path = '/home/alignminds/Desktop/Alignminds/Gemini_OCR_Vision/Heritage Foundation - Full Filing- Nonprofit Explorer - ProPublica.pdf'  # Replace with your PDF file path
extracted_image_file_names = extract_images_from_pdf(pdf_path)

# # Now you can use the extracted image file names for text extraction
# for img_file in extracted_image_file_names:
#     extract_text_from_image(img_file)  # Replace with your text extraction function

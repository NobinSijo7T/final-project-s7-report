import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_images_from_pdf(pdf_path, output_folder):
    """Extract all images from a PDF file."""
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    image_count = 0
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get list of images on the page
        image_list = page.get_images(full=True)
        
        # Extract each image
        for img_index, img in enumerate(image_list):
            xref = img[0]  # Get the XREF of the image
            
            # Extract the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_filename = f"image_page{page_num + 1}_{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)
            
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            
            image_count += 1
            print(f"Extracted: {image_filename}")
    
    pdf_document.close()
    print(f"\nTotal images extracted: {image_count}")

if __name__ == "__main__":
    pdf_path = "content.pdf"
    output_folder = "images"
    
    print(f"Extracting images from '{pdf_path}'...\n")
    extract_images_from_pdf(pdf_path, output_folder)
    print(f"\nAll images saved to '{output_folder}' folder.")

"""
PDF Image Extraction Script

This script scans all PDFs in the 'pdfs' folder (located in the same directory as the script),
extracts images larger than a specified size, and saves them into a structured 'extracted-images' directory.

Each PDF gets its own subfolder within 'extracted-images'. Filtering is applied to ignore small images 
(e.g., headers, footers, logos).

Dependencies:
- PyMuPDF (pip install pymupdf)
- OS (built-in)

Usage:
- Place PDF files in the 'pdfs' folder.
- Run the script to extract images.

Author: Nick Mirsepassi
Date: 22/02/2025
"""

import fitz
import os

# Get the script's directory dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths dynamically
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "extracted-images")

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define filtering parameters
MIN_WIDTH = 350  # Ignore images smaller than this width
MIN_HEIGHT = 350  # Ignore images smaller than this height


def extract_images_from_pdfs():
    """Extracts images from all PDFs in the 'pdfs' folder and saves them into structured folders."""
    for pdf_file in os.listdir(PDF_FOLDER):
        if pdf_file.endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(PDF_FOLDER, pdf_file)

            # Create a separate folder for each PDF file in extracted-images
            pdf_name = os.path.splitext(pdf_file)[0]  # Remove .pdf extension
            pdf_output_folder = os.path.join(OUTPUT_FOLDER, pdf_name)
            os.makedirs(pdf_output_folder, exist_ok=True)

            # Open the PDF file
            doc = fitz.open(pdf_path)
            print(f"Processing {pdf_file}...")

            # Loop through each page
            for page_number in range(len(doc)):
                page = doc[page_number]
                images = page.get_images(full=True)

                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    width = base_image["width"]
                    height = base_image["height"]

                    # Filter: Ignore small images (logos, footers, etc.)
                    if width < MIN_WIDTH or height < MIN_HEIGHT:
                        print(f"Skipping small image on page {page_number+1} ({width}x{height})")
                        continue

                    # Save the image in the corresponding PDF folder
                    image_filename = os.path.join(
                        pdf_output_folder, f"page_{page_number+1}_img_{img_index+1}.{image_ext}"
                    )
                    with open(image_filename, "wb") as img_file:
                        img_file.write(image_bytes)

                    print(f"Extracted: {image_filename} ({width}x{height})")

            print(f"Completed extraction for {pdf_file}\n")

    print("All PDF image extractions complete.")


if __name__ == "__main__":
    extract_images_from_pdfs()

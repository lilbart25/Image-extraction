import fitz
from PIL import Image
import io

def extract_images_with_footer(pdf_path):
    images_with_footer = []
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        footer = page.get_text("clip=footer")
        image_list = page.get_images()
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            try:
                image_stream = io.BytesIO(image_data)
                pil_image = Image.open(image_stream)
                images_with_footer.append((pil_image, footer))
            except (OSError, Image.DecompressionBombError):
                continue
    return images_with_footer

pdf_path = "path_to_your_pdf.pdf"
extracted_images_with_footer = extract_images_with_footer(pdf_path)

# Save the images with footer
for i, (image, footer) in enumerate(extracted_images_with_footer):
    image.save(f"image_{i+1}.png")
    print(f"Image {i+1} saved with footer: {footer}")

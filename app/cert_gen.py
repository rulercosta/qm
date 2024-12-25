import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
from PIL import ImageFont

def generate_certificate_image(name, qr_data, template_path, workshop, instructor, date):    
    # Get the current working directory (equivalent to pwd)
    current_working_directory = os.getcwd()

    # Font paths using the current working directory
    name_font_path = os.path.join(current_working_directory, 'static/fonts', 'Tinos-Bold.ttf')
    text_font_path = os.path.join(current_working_directory, 'static/fonts', 'Poppins-BoldItalic.ttf')
    date_font_path = os.path.join(current_working_directory, 'static/fonts', 'OpenSans-Regular.ttf')

    # Open the certificate template
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)

    # Load the name font and set size
    font = ImageFont.truetype(name_font_path, size=80)
    font_color = "#DDAC00"  # Gold color

    # Define the vertical position for the name
    name_position_y = 500  # Fixed vertical position

    # Calculate text width using textbbox to center horizontally for name
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    certificate_width = template.width
    name_position_x = (certificate_width - text_width) // 2

    # Draw the name centered
    draw.text((name_position_x, name_position_y), name, fill=font_color, font=font)

    # Load the font for workshop and instructor (or use another font for consistency)
    text_font = ImageFont.truetype(text_font_path, size=40)
    date_font = ImageFont.truetype(date_font_path, size=22)

    # Calculate text width for workshop and instructor
    # Workshop position
    workshop_position_y = 655
    text_bbox = draw.textbbox((0, 0), workshop, font=text_font)
    text_width = text_bbox[2] - text_bbox[0]
    workshop_position_x = (certificate_width - text_width) // 2
    draw.text((workshop_position_x, workshop_position_y), workshop, fill="black", font=text_font)

    # Instructor position
    instructor_position_y = 820
    text_bbox = draw.textbbox((0, 0), instructor, font=text_font)
    text_width = text_bbox[2] - text_bbox[0]
    instructor_position_x = (certificate_width - text_width) // 2
    draw.text((instructor_position_x, instructor_position_y), instructor, fill="black", font=text_font)

    # Date position
    date_position = (1722, 1384)  # Adjust coordinates as needed
    draw.text(date_position, date, fill="black", font=date_font)

    # Generate QR code with custom colors
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image for the QR code with the custom background color
    qr_image = qr.make_image(fill='black', back_color='#f2f2f2')  # Set the background color

    # Resize the QR code image to match the required size
    qr_image = qr_image.resize((124, 124))  # Adjust size as needed

    # Define the position for the QR code
    qr_position = (947, 1248)  # Adjust based on your template

    # Paste QR code on the certificate
    template.paste(qr_image, qr_position)

    return template


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def generate_certificate_pdf(certificate_image):
    buffer = BytesIO()

    # Get the dimensions of the certificate image
    img_width, img_height = certificate_image.size

    # Create a PDF canvas with the size of the certificate image
    pdf_canvas = canvas.Canvas(buffer, pagesize=(img_width, img_height))

    # Convert the PIL image to an ImageReader object
    img_buffer = BytesIO()
    certificate_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    image_reader = ImageReader(img_buffer)

    # Draw the image on the PDF with the correct dimensions
    pdf_canvas.drawImage(image_reader, 0, 0, width=img_width, height=img_height)
    pdf_canvas.showPage()
    pdf_canvas.save()

    buffer.seek(0)
    return buffer

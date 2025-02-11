import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from flask import current_app

def generate_certificate_image(name, qr_data, template_path, workshop, instructor, date):
    template = None
    try:
        if not os.path.isfile(template_path):
            current_app.logger.error(f"Template file not found or not a file: {template_path}")
            raise FileNotFoundError(f"Certificate template not found at {template_path}")

        # Check template file size
        template_size = os.path.getsize(template_path)
        if (template_size > 10 * 1024 * 1024):  # 10MB limit
            raise ValueError("Certificate template file is too large")

        template = Image.open(template_path)
        
        # Convert template to RGB if it's in RGBA mode
        if template.mode == 'RGBA':
            template = template.convert('RGB')

        # Update fonts directory path to use parent directory
        fonts_dir = os.path.join(os.path.dirname(current_app.root_path), 'static/fonts')
        
        for font_file in ['Tinos-Bold.ttf', 'Poppins-BoldItalic.ttf', 'OpenSans-Regular.ttf']:
            if not os.path.exists(os.path.join(fonts_dir, font_file)):
                raise FileNotFoundError(f"Font file {font_file} not found in {fonts_dir}")

        name_font_path = os.path.join(fonts_dir, 'Tinos-Bold.ttf')
        text_font_path = os.path.join(fonts_dir, 'Poppins-BoldItalic.ttf')
        date_font_path = os.path.join(fonts_dir, 'OpenSans-Regular.ttf')

        draw = ImageDraw.Draw(template)

        font = ImageFont.truetype(name_font_path, size=80)
        font_color = "#DDAC00"  

        name_position_y = 500  

        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        certificate_width = template.width
        name_position_x = (certificate_width - text_width) // 2

        draw.text((name_position_x, name_position_y), name, fill=font_color, font=font)

        text_font = ImageFont.truetype(text_font_path, size=40)
        date_font = ImageFont.truetype(date_font_path, size=22)

        workshop_position_y = 655
        text_bbox = draw.textbbox((0, 0), workshop, font=text_font)
        text_width = text_bbox[2] - text_bbox[0]
        workshop_position_x = (certificate_width - text_width) // 2
        draw.text((workshop_position_x, workshop_position_y), workshop, fill="black", font=text_font)

        instructor_position_y = 820
        text_bbox = draw.textbbox((0, 0), instructor, font=text_font)
        text_width = text_bbox[2] - text_bbox[0]
        instructor_position_x = (certificate_width - text_width) // 2
        draw.text((instructor_position_x, instructor_position_y), instructor, fill="black", font=text_font)

        date_position = (1722, 1384)  
        draw.text(date_position, date, fill="black", font=date_font)

        # Optimize QR code generation
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,  # Reduced from 10
            border=2,    # Reduced from 4
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill='black', back_color='#f2f2f2') 

        qr_image = qr_image.resize((124, 124))  

        qr_position = (947, 1248)  

        template.paste(qr_image, qr_position)

        return template

    except Exception as e:
        current_app.logger.error(f"Certificate generation error: {str(e)}", exc_info=True)
        if template:
            template.close()
        raise

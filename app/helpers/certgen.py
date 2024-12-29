import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

def generate_certificate_image(name, qr_data, template_path, workshop, instructor, date):    
    current_working_directory = os.getcwd()

    name_font_path = os.path.join(current_working_directory, 'static/fonts', 'Tinos-Bold.ttf')
    text_font_path = os.path.join(current_working_directory, 'static/fonts', 'Poppins-BoldItalic.ttf')
    date_font_path = os.path.join(current_working_directory, 'static/fonts', 'OpenSans-Regular.ttf')

    template = Image.open(template_path)
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

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill='black', back_color='#f2f2f2') 

    qr_image = qr_image.resize((124, 124))  

    qr_position = (947, 1248)  

    template.paste(qr_image, qr_position)

    return template

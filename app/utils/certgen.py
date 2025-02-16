import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

class CertificateGenerator:
    def __init__(self, app):
        self.app = app
        self.fonts_dir = os.path.join('static', 'fonts')
        self.templates_dir = os.path.join('static', 'images')
        
    def _load_fonts(self):
        fonts = {
            'name': ('Tinos-Bold.ttf', 80),
            'text': ('Poppins-BoldItalic.ttf', 40),
            'date': ('OpenSans-Regular.ttf', 22)
        }
        
        return {
            name: ImageFont.truetype(os.path.join(self.fonts_dir, filename), size)
            for name, (filename, size) in fonts.items()
        }

    def generate_certificate(self, name, qr_data, workshop, instructor, date):
        template_path = os.path.join(self.templates_dir, 'certificate_template.png')
        
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"Certificate template not found at {template_path}")

        try:
            with Image.open(template_path) as template:
                if template.mode == 'RGBA':
                    template = template.convert('RGB')
                
                fonts = self._load_fonts()
                draw = ImageDraw.Draw(template)
                
                self._draw_text(draw, name, fonts['name'], y=500, color="#DDAC00")
                
                self._draw_text(draw, workshop, fonts['text'], y=655)
                
                self._draw_text(draw, instructor, fonts['text'], y=820)
                
                draw.text((1722, 1384), date, fill="black", font=fonts['date'])
                
                qr_image = self._generate_qr(qr_data)
                template.paste(qr_image, (947, 1248))
                
                return template.copy()

        except Exception as e:
            self.app.logger.error(f"Certificate generation error: {str(e)}", exc_info=True)
            raise

    def _draw_text(self, draw, text, font, y, color="black"):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        image_width = draw._image.width
        x = (image_width - text_width) // 2
        draw.text((x, y), text, fill=color, font=font)

    def _generate_qr(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='#f2f2f2')
        return qr_image.resize((124, 124))

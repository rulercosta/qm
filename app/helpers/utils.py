def format_date_with_ordinal(date):
    day = date.day
    month = date.strftime('%B')
    year = date.strftime('%Y')

    # Determine the ordinal suffix
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    return f"{day}{suffix} {month}, {year}"

from PIL import Image

def resize_image(image, target_width):
    """
    Resizes the given image to the target width while maintaining the aspect ratio.
    Ensures the image has a transparent background (RGBA mode).

    :param image: The PIL Image to resize.
    :param target_width: The width to resize the image to.
    :return: The resized PIL Image.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    aspect_ratio = target_width / float(image.width)
    new_height = int(float(image.height) * aspect_ratio)
    
    resized_image = image.resize((target_width, new_height), Image.Resampling.LANCZOS)
    
    return resized_image
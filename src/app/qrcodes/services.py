import qrcode
from PIL import Image
import io
from typing import Optional
from werkzeug.datastructures import FileStorage

def generate_qr_code(
    url: str,
    title: str,
    foreground_color: str = "#000000",
    background_color: str = "#ffffff",
    logo: Optional[FileStorage] = None,
) -> io.BytesIO:
    """Generates a QR code image.

    Args:
        url: The URL to encode in the QR code.
        title: The title of QR code.
        foreground_color: The foreground color of the QR code.
        background_color: The background color of the QR code.
        logo: An optional logo image to be added to the center of the QR code.

    Returns:
        A BytesIO stream containing the QR code image data.
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=foreground_color, back_color=background_color)

    # Add logo to the QR code if provided
    if logo:
        logo_img = Image.open(logo)
        logo_width = img.size[0] // 5  #  logo width should be 1/5 of the QR code width
        logo_height = img.size[1] // 5 #  logo height should be 1/5 of the QR code height
        
        logo_img = logo_img.resize((logo_width, logo_height))
        img.paste(
            logo_img,
            (
                (img.size[0] - logo_img.size[0]) // 2,
                (img.size[1] - logo_img.size[1]) // 2,
            ),
            logo_img if logo_img.mode == 'RGBA' else None
        )

    # Save the image to a BytesIO stream
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
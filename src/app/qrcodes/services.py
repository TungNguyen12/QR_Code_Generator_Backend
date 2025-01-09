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
        url: The URL to encode in the QR code (string).
        title: The title of QR code (string).
        foreground_color: The foreground color of the QR code (string, default is "#000000").
        background_color: The background color of the QR code (string, default is "#ffffff").
        logo: An optional logo image to be added to the center of the QR code (FileStorage, optional).

    Returns:
        A BytesIO stream containing the QR code image data.
    """
    # Initialize QR code generator with version 1, box size 10 and border 5
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    # Add data (URL) to the QR code generator
    qr.add_data(url)
    # Generate the QR code
    qr.make(fit=True)

    # Create the QR code image with the specified colors
    img = qr.make_image(fill_color=foreground_color, back_color=background_color)

    # Check if a logo is provided
    if logo:
        # Open the logo image
        logo_img = Image.open(logo)
        # Calculate logo dimensions to fit in the middle of the QR code
        logo_width = img.size[0] // 5
        logo_height = img.size[1] // 5
        
        # Resize the logo image
        logo_img = logo_img.resize((logo_width, logo_height))
        # Paste the resized logo in the middle of the QR code image
        img.paste(
            logo_img,
            (
                (img.size[0] - logo_img.size[0]) // 2,
                (img.size[1] - logo_img.size[1]) // 2,
            ),
             # Use logo as a mask if it has an alpha channel
            logo_img if logo_img.mode == 'RGBA' else None
        )

    # Create a BytesIO stream to store the image
    img_io = io.BytesIO()
    # Save the QR code image to the BytesIO stream
    img.save(img_io, 'PNG')
    # Set the stream position to the beginning to be read later
    img_io.seek(0)
    # Return the BytesIO stream
    return img_io
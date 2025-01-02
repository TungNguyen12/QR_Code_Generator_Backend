import qrcode
from PIL import Image
import io

def generate_qr_code(url, foreground_color="#000000", background_color="#ffffff", logo=None):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill=foreground_color, back_color=background_color)

    # Add logo to the QR code if provided
    if logo:
        logo_img = Image.open(logo)
        logo_img = logo_img.resize((50, 50))  # Resize the logo
        img.paste(logo_img, ((img.size[0] - logo_img.size[0]) // 2, (img.size[1] - logo_img.size[1]) // 2), logo_img)

    # Save the image to a BytesIO stream
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
